import pytest
from patterns.singleton_pattern import Config

def test_singleton_instance():
    cfg1 = Config()
    cfg2 = Config()
    assert cfg1 is cfg2, "Config is not a Singleton"

def test_settings_loaded():
    cfg = Config()
    assert hasattr(cfg, "settings"), "Config has no 'settings' attribute"

    config_dict = cfg.settings['config']   
    for key in ["log_level", "data_path", "report_path", "default_strategy"]:
        assert key in config_dict, f"Key '{key}' is missing in settings"
