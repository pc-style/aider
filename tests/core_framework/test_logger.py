import logging
from agent.logger import init_logging, get_logger
from agent.config import AppConfig, LLMConfig, ToolsConfig, SafetyConfig, RLConfig

def test_json_logging_output(capsys):
    # Minimal config object
    config = AppConfig(
        llm=LLMConfig(providers=["foo"], keys={"foo": "bar"}, priority=["foo"]),
        tools=ToolsConfig(auto_install=True),
        safety=SafetyConfig(boundary_regex=[]),
        rl=RLConfig(reward_weights={"token_efficiency": 0.5, "user_satisfaction": 0.5}),
        log_level="INFO",
    )
    init_logging(config)
    logger = get_logger("test_logger")
    logger.info("hello world", extra={"context": "test"})
    out = capsys.readouterr().out
    assert '"message":"hello world"' in out
    assert '"context":"test"' in out
    assert '"level":"INFO"' in out