import json
import os
from threading import Lock

class Config(object):

    _instance = None
    _lock = Lock()

    def __new__(cls, config_path: str = None):
        with cls._lock:
            if cls._instance is None:
                cls._instance = object.__new__(cls)
                cls._instance._initialized = False
        return cls._instance

    def __init__(self, config_path: str = None):
        if self._initialized:
            return

        base_dir = os.path.dirname(os.path.dirname(__file__))
        config_dir = os.path.join(base_dir, "config")

        # Load multiple configs
        self.settings = {}
        for filename in ["config.json", "strategy_params.json"]:
            path = os.path.join(config_dir, filename)
            with open(path, "r") as f:
                self.settings[filename.replace(".json", "")] = json.load(f)

        self._initialized = True
