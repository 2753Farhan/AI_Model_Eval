
# src/finetuning/dataset_preparer.py
"""
Prepares training datasets for fine-tuning based on failure patterns
Uses existing DatasetLoader
"""

from typing import List, Dict, Any, Optional
import random
from pathlib import Path
import json
import logging

from ..loaders import DatasetLoader
from ..entities import Problem, EvaluationResult

logger = logging.getLogger(__name__)

class DatasetPreparer:
    """Prepares training datasets for fine-tuning based on failure patterns"""
    
    def __init__(self, output_dir: str = "data/finetuning"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def find_similar_problems(
        self, 
        failures: List[EvaluationResult],
        candidate_dataset: DatasetLoader,
        max_problems: int = 100
    ) -> List[Problem]:
        """Find problems similar to failures in candidate dataset"""
        
        similar_problems = []
        
        # Extract keywords from failures
        failure_keywords = self._extract_keywords(failures)
        
        # Score each problem in candidate dataset
        scored_problems = []
        for problem in candidate_dataset.problems:
            score = self._calculate_similarity_score(problem, failure_keywords)
            if score > 0:
                scored_problems.append((score, problem))
        
        # Sort by similarity score
        scored_problems.sort(reverse=True, key=lambda x: x[0])
        
        # Take top problems
        similar_problems = [p for _, p in scored_problems[:max_problems]]
        
        logger.info(f"Found {len(similar_problems)} similar problems")
        return similar_problems
    
    def _extract_keywords(self, failures: List[EvaluationResult]) -> Dict[str, float]:
        """Extract keywords from failures with weights"""
        keywords = {}
        
        for failure in failures:
            # Extract from problem description if available
            if hasattr(failure, 'metadata') and 'prompt' in failure.metadata:
                words = failure.metadata['prompt'].lower().split()
                for word in words:
                    if len(word) > 3:  # Skip small words
                        keywords[word] = keywords.get(word, 0) + 1
            
            # Extract from error messages
            for error in failure.errors:
                error_msg = error.get('error_message', '').lower()
                error_words = error_msg.split()
                for word in error_words:
                    if len(word) > 3:
                        keywords[word] = keywords.get(word, 0) + 2  # Higher weight for error words
        
        # Normalize
        total = sum(keywords.values())
        if total > 0:
            keywords = {k: v/total for k, v in keywords.items()}
        
        return keywords
    
    def _calculate_similarity_score(self, problem: Problem, keywords: Dict[str, float]) -> float:
        """Calculate similarity score between problem and keywords"""
        score = 0.0
        
        # Check problem prompt
        prompt_lower = problem.prompt.lower()
        for keyword, weight in keywords.items():
            if keyword in prompt_lower:
                score += weight
        
        # Check problem categories/tags
        for category in problem.categories:
            category_lower = category.lower()
            for keyword, weight in keywords.items():
                if keyword in category_lower:
                    score += weight * 0.5
        
        return score
    
    def create_training_data(
        self,
        failures: List[EvaluationResult],
        similar_problems: List[Problem],
        output_file: str = "training_data.jsonl"
    ) -> str:
        """Create training data in JSONL format for fine-tuning"""
        
        training_examples = []
        
        # Add failure examples as negative examples
        for failure in failures[:50]:  # Limit to 50 failures
            example = self._create_training_example(failure, is_failure=True)
            if example:
                training_examples.append(example)
        
        # Add similar problems as positive examples
        for problem in similar_problems:
            example = self._create_problem_example(problem)
            if example:
                training_examples.append(example)
        
        # Save to file
        output_path = self.output_dir / output_file
        with open(output_path, 'w', encoding='utf-8') as f:
            for example in training_examples:
                f.write(json.dumps(example) + '\n')
        
        logger.info(f"Created {len(training_examples)} training examples in {output_path}")
        return str(output_path)
    
    def _create_training_example(self, failure: EvaluationResult, is_failure: bool) -> Optional[Dict]:
        """Create training example from a failure"""
        try:
            # Get problem info
            problem_id = failure.problem_id
            
            example = {
                "instruction": "Write a Python function that solves the following problem:",
                "input": failure.metadata.get('prompt', 'Unknown problem'),
                "output": failure.generated_code or "",
                "is_failure": is_failure,
                "error_type": failure.errors[0].get('error_type') if failure.errors else None
            }
            return example
        except Exception as e:
            logger.error(f"Error creating training example: {e}")
            return None
    
    def _create_problem_example(self, problem: Problem) -> Optional[Dict]:
        """Create training example from a problem"""
        try:
            example = {
                "instruction": "Write a Python function that solves the following problem:",
                "input": problem.prompt,
                "output": problem.canonical_solution or "",
                "entry_point": problem.entry_point,
                "test": problem.test,
                "difficulty": problem.difficulty
            }
            return example
        except Exception as e:
            logger.error(f"Error creating problem example: {e}")
            return None