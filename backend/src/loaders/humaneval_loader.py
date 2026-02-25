
from typing import List, Dict, Any, Optional
import os
import json
import gzip
from git import Repo
from tqdm import tqdm
import logging
from datetime import datetime  


from .dataset_loader import DatasetLoader
from ..entities import Problem

logger = logging.getLogger(__name__)


class HumanEvalLoader(DatasetLoader):
    """Loader for the HumanEval dataset"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.repo_url = config.get('repo_url', 'https://github.com/openai/human-eval.git')
        self.data_dir = config.get('data_dir', 'data/human_eval')
        self.dataset_path = os.path.join(
            self.data_dir,
            'data',
            'HumanEval.jsonl.gz'
        )
        self.metadata = {
            'source': 'OpenAI',
            'paper': 'Evaluating Large Language Models Trained on Code',
            'year': 2021,
            'tasks': 164,
            'languages': ['python']
        }

    def fetch_repo(self) -> bool:
        """Clone the repository if not exists"""
        if not os.path.exists(os.path.join(self.data_dir, '.git')):
            try:
                logger.info(f"Cloning HumanEval repository from {self.repo_url}")
                Repo.clone_from(self.repo_url, self.data_dir)
                return True
            except Exception as e:
                logger.error(f"Failed to clone repository: {e}")
                return False
        else:
            logger.info("Repository already exists")
            return True

    def load_dataset(self) -> List[Problem]:
        """Load the HumanEval dataset"""
        if not self.fetch_repo():
            raise RuntimeError("Failed to fetch repository")
        
        if not os.path.exists(self.dataset_path):
            raise FileNotFoundError(f"Dataset not found at {self.dataset_path}")
        
        logger.info(f"Loading HumanEval dataset from {self.dataset_path}")
        
        problems = []
        with gzip.open(self.dataset_path, 'rt', encoding='utf-8') as f:
            for line in tqdm(f, desc="Loading problems"):
                data = json.loads(line)
                
                # Create Problem entity
                problem = Problem(
                    task_id=data['task_id'],
                    prompt=data['prompt'],
                    dataset_id=self.dataset_id
                )
                
                # Set canonical solution
                problem.set_canonical_solution(data['canonical_solution'])
                
                # Set test cases
                test_code = data['test']
                problem.set_test_cases(test_code)
                
                # Set entry point
                problem.entry_point = data['entry_point']
                
                # Set metadata
                problem.metadata = {
                    'signature': data.get('signature', ''),
                    'docstring': data.get('docstring', ''),
                    'language': 'python',
                    'source': 'humaneval'
                }
                
                # Calculate initial stats
                problem.stats = problem.calculate_complexity()
                
                problems.append(problem)
        
        self.problems = problems
        self.loaded_at = datetime.now()
        
        logger.info(f"Loaded {len(problems)} problems from HumanEval")
        
        return problems

    def validate_dataset(self) -> bool:
        """Validate the dataset structure"""
        if not self.problems:
            return False
        
        required_fields = ['task_id', 'prompt', 'canonical_solution', 'test', 'entry_point']
        
        for problem in self.problems:
            # Check if we can access all required data
            if not problem.task_id:
                return False
            if not problem.prompt:
                return False
            if not problem.canonical_solution:
                return False
            if not problem.test_cases:
                return False
            if not problem.entry_point:
                return False
        
        logger.info("Dataset validation passed")
        return True

    def get_problem_by_name(self, function_name: str) -> Optional[Problem]:
        """Get a problem by function name"""
        for problem in self.problems:
            if problem.entry_point == function_name:
                return problem
        return None

    def get_problems_by_difficulty(self, difficulty: str) -> List[Problem]:
        """Get problems by difficulty level"""
        # HumanEval doesn't have built-in difficulty, so we estimate
        problems_with_complexity = []
        for problem in self.problems:
            if problem.stats:
                complexity = problem.stats.get('cyclomatic_complexity', 0)
                
                # Estimate difficulty based on complexity
                if difficulty == 'easy' and complexity <= 3:
                    problems_with_complexity.append(problem)
                elif difficulty == 'medium' and 3 < complexity <= 7:
                    problems_with_complexity.append(problem)
                elif difficulty == 'hard' and complexity > 7:
                    problems_with_complexity.append(problem)
        
        return problems_with_complexity