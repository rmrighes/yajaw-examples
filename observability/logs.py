from contextvars import ContextVar
import gzip
import json
import logging
import logging.config
import logging.handlers
import os
import re
import uuid


context_id: ContextVar[uuid.UUID] = ContextVar(
    "context_id", default=uuid.UUID("00000000-0000-0000-0000-000000000000")
)

# Define your ContextFilter class
class ContextFilter(logging.Filter):
    def filter(self, record):
        record.context_id = str(context_id.get())
        return True
    
# Replace double quotes for single quotes in log message
class QuotesFilter(logging.Filter):
    def filter(self, record):
        record.msg = record.msg.replace('\"', '\'')
        return record


# Define your PIIFilter class
class PIIFilter(logging.Filter):
    pii_pattern = re.compile(r"(email|password|ssn):\s*\S+", re.IGNORECASE)

    def filter(self, record):
        if self.pii_pattern.search(record.getMessage()):
            record.msg = self.pii_pattern.sub(r"\1: [REDACTED]", record.msg)
        return True


# Define your JsonFormatter class
class JsonFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt="%Y-%m-%dT%H:%M:%SZ", style="%"):
        super().__init__(fmt=fmt, datefmt=datefmt, style=style)

    def format(self, record):
        log_record = {
            "asctime": self.formatTime(record, self.datefmt),
            "name": record.name,
            "levelname": record.levelname,
            "funcname": record.funcName,
            "context_id": getattr(record, "context_id", "no_context"),
            "message": record.getMessage(),
        }
        if record.exc_info:
            log_record["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(log_record)


# Define your rotator function
def rotator(source, dest):
    with open(source, "rb") as fs, gzip.open(dest, "wb") as fd:
        fd.writelines(fs)
    os.remove(source)


# Define your namer function
def namer(name):
    return name + ".gz"


# Define a function to create a default configuration file
def create_default_config(file_path):
    default_config = {
        "version": 1,
        "formatters": {"json": {"()": "observability.logs.JsonFormatter"}},
        "filters": {
            "context": {"()": "observability.logs.ContextFilter"},
            "piifilter": {"()": "observability.logs.PIIFilter"},
            "quotes":{"()": "observability.logs.QuotesFilter"}
        },
        "handlers": {
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "DEBUG",
                "formatter": "json",
                "filters": ["context", "piifilter", "quotes"],
                "filename": "logs/example.log",
                "maxBytes": 10485760,
                "backupCount": 10,
            }
        },
        "loggers": {
            "yajaw": {"handlers": ["file"], "level": "INFO", "propagate": True},
            "example": {"handlers": ["file"], "level": "INFO", "propagate": True},
            "httpx": {"handlers": ["file"], "level": "INFO", "propagate": True},
        },
    }

    with open(file_path, "w") as config_file:
        json.dump(default_config, config_file, indent=4)


# Define your setup_logging function
def setup_logging():
    # Ensure logs directory exists
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__package__)), "logs")
    os.makedirs(log_dir, exist_ok=True)

    config_file_path = "config/logging.json"  # Specify the path to your config file

    # Check if the configuration file exists; if not, create it with default settings
    if not os.path.exists(config_file_path):
        create_default_config(config_file_path)

    # Now that we're sure the file exists, read the configuration JSON file
    with open(config_file_path) as config_file:
        config_dict = json.load(config_file)

    # Apply the configuration
    logging.config.dictConfig(config_dict)

    # Add compression to RotatingFileHandler
    logger = logging.getLogger("yajaw")
    for handler in logger.handlers:
        if isinstance(handler, logging.handlers.RotatingFileHandler):
            handler.rotator = rotator
            handler.namer = namer
