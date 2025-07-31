import logging
import sys
from datetime import datetime
from typing import Any, Dict

try:
    import orjson as _jsonlib
    def dumps(obj): return _jsonlib.dumps(obj).decode("utf-8")
except ImportError:
    import json as _jsonlib
    def dumps(obj): return _jsonlib.dumps(obj, separators=(",", ":"))

class JsonLogFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "message": record.getMessage(),
        }
        if hasattr(record, "extra") and isinstance(record.extra, dict):
            log_record.update(record.extra)
        else:
            # Add extra non-standard attributes if any
            for k, v in record.__dict__.items():
                if k not in ("name", "msg", "args", "levelname", "levelno", "pathname", "filename", "module", "exc_info", "exc_text", "stack_info", "lineno", "funcName", "created", "msecs", "relativeCreated", "thread", "threadName", "processName", "process"):
                    log_record[k] = v
        return dumps(log_record)

def init_logging(config):
    root = logging.getLogger()
    root.handlers.clear()
    level = getattr(logging, getattr(config, "log_level", "INFO").upper(), logging.INFO)
    root.setLevel(level)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonLogFormatter())
    root.addHandler(handler)

def get_logger(name):
    return logging.getLogger(name)