"""Configuration module."""
import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional


class Config:
    """Configuration manager for the application."""
    
    _instance = None
    _config: Dict[str, Any] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize configuration from settings.yaml."""
        if not self._config:
            self.load()
    
    def load(self, config_path: Optional[str] = None):
        """Load configuration from YAML file."""
        if config_path is None:
            config_path = Path(__file__).parent / 'settings.yaml'
        
        try:
            with open(config_path, 'r') as f:
                self._config = yaml.safe_load(f) or {}
        except FileNotFoundError:
            self._config = self._get_default_config()
    
    @staticmethod
    def _get_default_config() -> Dict[str, Any]:
        """Get default configuration."""
        return {
            'models': [],
            'datasets': [],
            'evaluation': {
                'timeout': 30,
                'memory_limit': '4GB',
                'num_workers': 4
            },
            'output': {
                'results_dir': 'results',
                'export_formats': ['json', 'csv', 'html', 'pdf']
            },
            'logging': {
                'level': 'INFO',
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key."""
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value by key."""
        keys = key.split('.')
        config = self._config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def __getitem__(self, key: str) -> Any:
        """Dictionary-style access."""
        return self.get(key)
    
    def __setitem__(self, key: str, value: Any) -> None:
        """Dictionary-style setting."""
        self.set(key, value)


# Global configuration instance
config = Config()