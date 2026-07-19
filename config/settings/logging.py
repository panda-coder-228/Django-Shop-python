from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True,  exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers":  False,

    "formatters":{
        "verbose":{
            "()": "apps.core.telegram.telegram_handler.EmojiFormatter",
            "format": "{emoji} |{asctime} | {levelname:<8} | {name} | {module}:{lineno} | {message} | {request_id}",
            "style": "{",
            "datefmt": "%Y-%m-%d | %H-%M-%S"
        },
        "console": {
            "format": "{asctime} | {levelname:<8} | {message}",
            "style": "{",
        },
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s  %(levelname)s %(name)s %(module)s %(lineno)d %(message)s %(request_id)s",
        },
    },
    "filters":{
            "request_id":{
                "()": "apps.core.middleware.filters.RequestIdFilter",
            },
            # "require_debug_false":{
            #     "()": "django.utils.log.RequireDebugFalse"
            # }
        },
    "handlers":{
        "console":{
            "class": "logging.StreamHandler",
            "formatter": "console",
            "level": "INFO",
            "filters": ["request_id"],
        },
        "telegram":{
            "()": "apps.core.telegram.telegram_handler.SimpleTelegramHandler",
            "formatter": "verbose",
            "level": "ERROR",
            "filters": ["request_id"],
        },
        "json": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": str(LOG_DIR / "json.logs"),
            "maxBytes": 5 * 1024 * 1024,
            "backupCount": 7,
            "formatter": "json",
            "level": "INFO",
            "encoding": "utf-8",
            "filters": ['request_id'],
        },
        "users_file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": str(LOG_DIR / "users.logs"),
            "when": "midnight",
            "interval": 1,
            "level": "INFO",
            "backupCount": 6,
            "encoding": "utf-8",
            "filters": ['request_id'],
        },
        "errors_file":{
            "class": "logging.handlers.RotatingFileHandler",
            "filename": str(LOG_DIR / "errors.logs"),
            "formatter": "verbose",
            "maxBytes": 5 * 1024 * 1024,
            "backupCount": 7,
            "level": "ERROR",
            "encoding": "utf-8",
            "filters": ["request_id"],
        }
    },
    "loggers":{
        "django.request":{
            "handlers": ["errors_file", "telegram"],
            "level": "ERROR",
            "propagate": False,
        },
        "django":{
            "handlers": ["console", "json"],
            "level": "INFO",
            "propagate": False,
        },
        "apps.users":{
            "handlers":["users_file", "errors_file"],
            "level":"INFO",
            "propagate": False,
        }
    },
    "root":{
        "handlers": ["errors_file", "telegram", "json", "console"],
        "level": "ERROR",
    }
}