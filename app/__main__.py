#!/usr/bin/env python3

"""File to execute the converter using command line pattern"""
import fire
import json
import logging

from app.converter.converter import convert
from app.constants import BaseConfig


LOG_FORMAT = '{"Time Stamp":"%(asctime)s","Logging Level":"%(levelname)s","Info":%(message)s , %(name)s}'
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logging.basicConfig(level=BaseConfig.LOGGING_LEVEL, datefmt=DATE_FORMAT, format=LOG_FORMAT)
log = logging.getLogger('MenuConverter')


def convert_it(csv_file: str, json_file: str) -> None:
    """
    Function to convert csv to json
    :param csv_file: Path of input csv file
    :param json_file: Path of output json file
    """
    try:
        with open(csv_file, mode='r') as csv_in:
            json_out = json.dumps(convert(csv_in), indent=4)
            with open(json_file, mode='w') as json_write:
                json_write.write(json_out)
    except TypeError:
        log.error(f'{csv_file} not valid. Please check.')
    except FileNotFoundError:
        log.error(f'{csv_file} not found, please check.')
    except PermissionError:
        log.error(f'Not enough permissions to read or right file.')
    except Exception:
        logging.exception('Unkown Exception occured. Please check.')


if __name__ == "__main__":
    fire.Fire(convert_it)
