from agent.config import get_config
from typing import List, Dict, Any

try:
    import litellm
except ImportError:
    litellm = None  # For type-checking; actual usage expects litellm to be installed.

class MCPAdapter:
    def __init__(self, provider_name: str):
        self.config = get_config()
        if provider_name not in self.config.llm.providers:
            raise ValueError(f"Provider {provider_name} not in config.llm.providers")
        self.provider_name = provider_name

    def complete(self, messages: List[Dict[str, Any]], **kwargs):
        if not litellm:
            raise ImportError("litellm is required for MCPAdapter")
        provider = self.provider_name
        api_key = self.config.llm.keys.get(provider)
        model = kwargs.pop("model", None)
        # Normalize input for litellm (assumes OpenAI/Anthropic chat)
        call_kwargs = {
            "messages": messages,
            "model": model or "gpt-3.5-turbo",
            "api_key": api_key,
            "provider": provider,
        }
        call_kwargs.update(self._build_kwargs_from_config())
        call_kwargs.update(kwargs)
        return litellm.completion(**call_kwargs)

    def swap_provider(self, new_provider_name: str):
        if new_provider_name not in self.config.llm.providers:
            raise ValueError(f"Provider {new_provider_name} not in config.llm.providers")
        self.provider_name = new_provider_name

    def _build_kwargs_from_config(self):
        # Extend this as needed for per-provider settings in config
        return {}

def get_default_adapter():
    config = get_config()
    first = config.llm.priority[0]
    return MCPAdapter(first)