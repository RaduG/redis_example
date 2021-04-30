__all__ = ["logger", "r"]

from magic_logger import logger
from redis import Redis

r = Redis("redis")

logger.dict_config(
    {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "standard": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
        },
        "handlers": {
            "default": {
                "level": "INFO",
                "formatter": "standard",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "": {
                "handlers": ["default"],
                "level": "WARNING",
                "propagate": False,
            },
            "redis_example": {
                "handlers": ["default"],
                "level": "INFO",
                "propagate": False,
            },
            "__main__": {
                "handlers": ["default"],
                "level": "DEBUG",
                "propagate": False,
            },
        },
    }
)
