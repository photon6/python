import json
import yaml
from pathlib import Path

class ConfigLoader:
    def __init__(self):
        self.path = Path(path)
        self.config = self._load()

    def _load(self):
        suffix = self.path.suffix.lower()
        with open(self.path, "r", encording="utf-8") as f:
            if suffix in [".json"]:
                return json.load(f)
            elif suffix in [".yaml", ".yml"]:
                return yaml.safe_load(f)
            else:
                raise ValueError(f"Unsupported config format: {suffix}")
            
    def get(self, key, default=None):
        return self.config.get(key, default)
    
    def __getitem__(self, key):
        return self.config(key)