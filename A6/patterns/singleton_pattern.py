import json
import os
from threading import Lock

class Config(object):
    _instance = None   # class-variable : unique object of Config class
    _lock = Lock()     # ensure single-ton        

    def __new__(cls, config_path: str = None):         # cls : Config class itself
        with cls._lock:
            if cls._instance is None:
                cls._instance = object.__new__(cls)    # set unique object 
                cls._instance._initialized = False
        return cls._instance

    def __init__(self, config_path: str = None):
        if self._initialized:
            return
        
        # default path to A6/config/config.json
        if config_path is None:
            config_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),  # patterns/ -> A6/
                "config",
                "config.json"
            )

        with open(config_path, "r") as f:
            self.settings = json.load(f)

        self._initialized = True
