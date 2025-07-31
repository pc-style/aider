from .config import get_config
from .logger import init_logging, get_logger
from .mcp_adapter import MCPAdapter, get_default_adapter
from .error_handling import install_global_exception_hook

# Initialize config, logging, and global exception handling at import
config = get_config()
init_logging(config)
logger = get_logger(__name__)
install_global_exception_hook(logger)

__all__ = [
    "get_config",
    "get_logger",
    "MCPAdapter",
    "get_default_adapter",
]