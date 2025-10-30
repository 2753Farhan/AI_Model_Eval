import yaml
import os

class ConfigManager:
    def __init__(self, config_path: str):
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)

    def get(self, key: str, default=None):
        parts = key.split(".")
        value = self.config
        for part in parts:
            value = value.get(part, {})
        return value or default

    def ensure_dirs(self):
        data_dir = self.get("paths.data_dir")
        results_dir = self.get("paths.results_dir")
        os.makedirs(data_dir, exist_ok=True)
        os.makedirs(results_dir, exist_ok=True)
