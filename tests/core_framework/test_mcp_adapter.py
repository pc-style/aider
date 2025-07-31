import pytest
from agent.mcp_adapter import MCPAdapter

class DummyConfig:
    class llm:
        providers = ["foo", "bar"]
        keys = {"foo": "FOOKEY", "bar": "BARKEY"}
        priority = ["foo", "bar"]

def test_mcp_adapter_instantiation(monkeypatch):
    monkeypatch.setattr("agent.mcp_adapter.get_config", lambda: DummyConfig)
    adapter = MCPAdapter("foo")
    assert adapter.provider_name == "foo"
    adapter.swap_provider("bar")
    assert adapter.provider_name == "bar"
    with pytest.raises(ValueError):
        adapter.swap_provider("baz")