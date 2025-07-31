import os
import tempfile
import textwrap
from agent.config import get_config, load_yaml_config

def test_env_substitution(monkeypatch):
    with tempfile.NamedTemporaryFile("w+", suffix=".yaml", delete=False) as f:
        f.write(textwrap.dedent("""
        llm:
          providers: ["foo"]
          keys: {foo: "${MY_FOO_KEY}"}
          priority: ["foo"]
        tools: {auto_install: true}
        safety: {boundary_regex: []}
        rl: {reward_weights: {token_efficiency: 0.5, user_satisfaction: 0.5}}
        log_level: INFO
        """))
        f.flush()
        monkeypatch.setenv("MY_FOO_KEY", "abc123")
        config = get_config(f.name)
        assert config.llm.keys["foo"] == "abc123"