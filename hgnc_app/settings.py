# settings.py
"""
LOGGING CONFIGURATION (DEFENSIVE VERSION)
"""

import os
from pathlib import Path

# --------------------------------------------------
# STEP 1: Define default log file (hidden, home directory)
# --------------------------------------------------
home_dir = os.path.expanduser("~")
DEFAULT_LOG = os.path.join(home_dir, ".hgnc_app.log")

LOG_FILE = DEFAULT_LOG


# --------------------------------------------------
# STEP 2: NORMALISE the path (defensive step)
# --------------------------------------------------
LOG_FILE = os.path.abspath(os.path.expanduser(LOG_FILE))


# --------------------------------------------------
# STEP 3: Ensure directory exists
# --------------------------------------------------
log_dir = os.path.dirname(LOG_FILE)
if log_dir:
    os.makedirs(log_dir, exist_ok=True)


# --------------------------------------------------
# STEP 4: Logging configuration
# --------------------------------------------------
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,

    # --------------------------------------------------
    # FORMATTERS
    # --------------------------------------------------
    "formatters": {
        "standard": {
            "format": (
                "%(asctime)s | %(levelname)s | %(name)s | "
                "%(filename)s:%(lineno)d | %(message)s"
            )
        }
    },

    # --------------------------------------------------
    # HANDLERS
    # --------------------------------------------------
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "standard",
        },
        "file": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "standard",
            "filename": LOG_FILE,
        },
    },

    "loggers": {
        "hgnc_app": {
            "level": "DEBUG",
            "handlers": ["console", "file"],
            "propagate": False
        },
    },

    # --------------------------------------------------
    # ROOT LOGGER
    # --------------------------------------------------
    "root": {
        "level": "DEBUG",
        "handlers": ["console", "file"],
    }
}

# Setup data directory path
DATA_DIR = Path(__file__).resolve().parent.parent / "data"

# Setup data file
DATA_FILE = DATA_DIR / "hgnc_complete_set.txt"