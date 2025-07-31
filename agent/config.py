import os
import re
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
import yaml
from threading import Lock

_ENV_VAR_PATTERN = re.compile(r"\$\{([^}]+)\}")

def _substitute_env_vars(value):
    if isinstance(value, str):
        def repl(match):
            var_name = match.group(1)
            return os.environ.get(var_name, "")
        return _ENV_VAR_PATTERN.sub(repl, value)
    elif isinstance(value, dict):
        return {k: _substitute_env_vars(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [_substitute_env_vars(i) for i in value]
    else:
        return value

class LLMConfig(BaseModel):
    providers: List[str]
    keys: Dict[str, str]
    priority: List[str]

class ToolsConfig(BaseModel):
    auto_install: bool

class SafetyConfig(BaseModel):
    boundary_regex: List[str] = Field(default_factory=list)

class RLConfig(BaseModel):
    reward_weights: Dict[str, float]

class AppConfig(BaseModel):
    llm: LLMConfig
    tools: ToolsConfig
    safety: SafetyConfig
    rl: RLConfig
    log_level: Optional[str] = "INFO"

_CONFIG_SINGLETON = None
_CONFIG_LOCK = Lock()

def load_yaml_config(path: str = "config.yaml") -> dict:
    with open(path, "r") as f:
        raw = yaml.safe_load(f)
    return _substitute_env_vars(raw)

def get_config(path: Optional[str] = None) -> AppConfig:
    global _CONFIG_SINGLETON
    with _CONFIG_LOCK:
        if _CONFIG_SINGLETON is not None:
            return _CONFIG_SINGLETON
        config_path = path or os.environ.get("CONFIG_FILE", "config.yaml")
        dct = load_yaml_config(config_path)
        _CONFIG_SINGLETON = AppConfig(**dct)
        return _CONFIG_SINGLETON