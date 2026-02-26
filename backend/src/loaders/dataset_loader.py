
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Iterator
import hashlib
import json
import logging
from datetime import datetime

from ..entities import Problem

logger = logging.getLogger(__name__)


class DatasetLoader(ABC):
    """Abstract base class for all dataset loaders"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.dataset_id = self._generate_dataset_id()
        self.name = config.get('name', 'unknown')
        self.description = config.get('description', '')
        self.file_path = config.get('file_path')
        self.cache_enabled = config.get('cache_enabled', True)
        self.cache: Dict[str, Any] = {}
        self.metadata: Dict[str, Any] = {}
        self.loaded_at: Optional[datetime] = None
        self.problems: List[Problem] = []
        
        logger.info(f"Initialized dataset loader: {self.name}")

    def _generate_dataset_id(self) -> str:
        """Generate a unique dataset ID"""
        import secrets
        return f"dataset_{secrets.token_hex(8)}"

    @abstractmethod
    def load_dataset(self) -> List[Problem]:
        """Load the dataset"""
        pass

    @abstractmethod
    def validate_dataset(self) -> bool:
        """Validate dataset structure"""
        pass

    def get_problem(self, problem_id: str) -> Optional[Problem]:
        """Get a specific problem by ID"""
        for problem in self.problems:
            if problem.problem_id == problem_id:
                return problem
        return None

    def get_problems(self, indices: Optional[List[int]] = None) -> List[Problem]:
        """Get problems by indices"""
        if indices is None:
            return self.problems
        
        return [self.problems[i] for i in indices if 0 <= i < len(self.problems)]

    def get_random_problems(self, count: int) -> List[Problem]:
        """Get random problems"""
        import random
        if count >= len(self.problems):
            return self.problems.copy()
        
        indices = random.sample(range(len(self.problems)), count)
        return [self.problems[i] for i in indices]

    def get_statistics(self) -> Dict[str, Any]:
        """Get dataset statistics"""
        if not self.problems:
            return {}
        
        stats = {
            'total_problems': len(self.problems),
            'languages': {},
            'difficulties': {},
            'categories': {},
            'avg_complexity': 0,
            'total_tests': 0
        }
        
        total_complexity = 0
        total_tests = 0
        
        for problem in self.problems:
            # Count languages
            lang = problem.metadata.get('language', 'python')
            stats['languages'][lang] = stats['languages'].get(lang, 0) + 1
            
            # Count difficulties
            diff = problem.difficulty
            stats['difficulties'][diff] = stats['difficulties'].get(diff, 0) + 1
            
            # Count categories
            for cat in problem.categories:
                stats['categories'][cat] = stats['categories'].get(cat, 0) + 1
            
            # Sum complexity
            if problem.stats:
                total_complexity += problem.stats.get('cyclomatic_complexity', 0)
            
            total_tests += len(problem.test_cases)
        
        stats['avg_complexity'] = total_complexity / len(self.problems) if self.problems else 0
        stats['total_tests'] = total_tests
        stats['avg_tests_per_problem'] = total_tests / len(self.problems) if self.problems else 0
        
        return stats

    def split_dataset(
        self,
        train_ratio: float = 0.7,
        val_ratio: float = 0.15,
        test_ratio: float = 0.15,
        seed: Optional[int] = None
    ) -> Dict[str, List[Problem]]:
        """Split dataset into train/val/test sets"""
        if abs(train_ratio + val_ratio + test_ratio - 1.0) > 1e-6:
            raise ValueError("Ratios must sum to 1.0")
        
        import random
        if seed is not None:
            random.seed(seed)
        
        problems = self.problems.copy()
        random.shuffle(problems)
        
        total = len(problems)
        train_end = int(total * train_ratio)
        val_end = train_end + int(total * val_ratio)
        
        return {
            'train': problems[:train_end],
            'validation': problems[train_end:val_end],
            'test': problems[val_end:]
        }

    def export_dataset(self, format: str = 'json') -> str:
        """Export dataset to specified format"""
        data = [p.to_dict() for p in self.problems]
        
        if format == 'json':
            return json.dumps(data, indent=2, default=str)
        elif format == 'jsonl':
            return '\n'.join(json.dumps(p, default=str) for p in data)
        else:
            raise ValueError(f"Unsupported export format: {format}")

    def get_metadata(self) -> Dict[str, Any]:
        """Get dataset metadata"""
        return {
            'dataset_id': self.dataset_id,
            'name': self.name,
            'description': self.description,
            'file_path': self.file_path,
            'loaded_at': self.loaded_at.isoformat() if self.loaded_at else None,
            'problem_count': len(self.problems),
            'metadata': self.metadata,
            'statistics': self.get_statistics()
        }

    def clear_cache(self) -> None:
        """Clear the cache"""
        self.cache.clear()
        logger.info("Cache cleared")

    def __len__(self) -> int:
        return len(self.problems)

    def __getitem__(self, idx: int) -> Problem:
        return self.problems[idx]

    def __iter__(self) -> Iterator[Problem]:
        return iter(self.problems)