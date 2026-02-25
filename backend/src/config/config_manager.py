import os
import yaml
from pathlib import Path
from typing import Any, Dict, Optional


class ConfigManager:
    """Configuration manager for AI_ModelEval"""
    
    def __init__(self, config_path: str = "config/settings.yaml"):
        self.config_path = config_path
        self.config = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        config_file = Path(self.config_path)
        
        if not config_file.exists():
            # Return default config if file doesn't exist
            return self._get_default_config()
        
        with open(config_file, 'r') as f:
            return yaml.safe_load(f)
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Return default configuration"""
        return {
            'paths': {
                'data_dir': 'data',
                'results_dir': 'results',
                'cache_dir': 'cache',
                'logs_dir': 'logs',
                'repo_url': 'https://github.com/openai/human-eval'
            },
            'models': {
                'default_models': ['codellama:7b']
            },
            'evaluation': {
                'timeout_seconds': 30,
                'max_memory_mb': 512,
                'num_samples_per_task': 5,
                'prompt_strategies': ['zero_shot'],
                'resource_limits': {
                    'max_concurrent': 4
                }
            },
            'dashboard': {
                'host': '0.0.0.0',
                'port': 5000,
                'debug': False
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get config value using dot notation (e.g., 'paths.data_dir')"""
        keys = key.split('.')
        value = self.config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def ensure_dirs(self):
        """Create necessary directories if they don't exist"""
        paths = self.get('paths', {})
        for key, path in paths.items():
            if isinstance(path, str) and not path.startswith(('http', 'https')):
                Path(path).mkdir(parents=True, exist_ok=True)