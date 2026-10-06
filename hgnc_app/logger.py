# logger.py
"""
This module sets up logging for the application using a dictionary-based configuration.
It defines a function to apply the logging configuration, which should be called once at application startup.
This ensures that logging is globally configured, allowing all modules to use logging.getLogger()
and enabling hierarchical inheritance of loggers.
The logging configuration is defined in the LOGGING_CONFIG dictionary, which specifies loggers, handlers, formatters, and other logging settings.
"""

import logging.config

from hgnc_app.settings import LOGGING_CONFIG


# --------------------------------------------------
# LOGGING ACTIVATION FUNCTION
# --------------------------------------------------
def setup_logging():
    """
    Apply the logging configuration.

    This should be called ONCE at application startup.

    After this:
    ✔ Logging is globally configured
    ✔ All modules can use logging.getLogger()
    ✔ Hierarchical inheritance works automatically
    """

    logging.config.dictConfig(LOGGING_CONFIG)