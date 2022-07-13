"""Logger decorator indicates start and end of functions. Also logs exceptions."""

import logging

from app.constants import BaseConfig

LOG_FORMAT = '{"Time Stamp":"%(asctime)s","Logging Level":"%(levelname)s","Info":%(message)s , %(name)s}'
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logging.basicConfig(level=BaseConfig.LOGGING_LEVEL, datefmt=DATE_FORMAT, format=LOG_FORMAT)
log = logging.getLogger('MenuConverter')


def log_info(func):
    """Info logs for functions"""
    def wrapper(*args, **kwargs):
        try:
            log.info(f'{func.__name__} Started')
            output = func(*args, **kwargs)
            log.info(f'{func.__name__} Ended')
            return output
        except Exception as e:
            error_msg = f"Error has occurred at /{func.__name__}"
            log.error(error_msg)
            raise e
    return wrapper


def log_debug(func):
    """Debug logs for functions"""
    def wrapper(*args, **kwargs):
        try:
            log.debug(f'{func.__name__} Started')
            output = func(*args, **kwargs)
            log.debug(f'{func.__name__} Ended')
            return output
        except Exception as e:
            error_msg = f"Error has occurred at /{func.__name__}"
            log.error(error_msg)
            raise e
    return wrapper
