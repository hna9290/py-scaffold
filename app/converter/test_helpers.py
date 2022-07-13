import io
from typing import BinaryIO

import pytest

from app.converter.helpers import create_file, _files, get_converted_file, delete_file


@pytest.fixture
def setup():
    bin_input_csv: BinaryIO = io.BytesIO(b"""Base URL,Level 1 - Name,Level 1 - ID,Level 1 - URL,Level 2 - Name,Level 2 - ID,Level 2 - URL,Level 3 - Name,Level 3 - ID,Level 3 - URL
    https://groceries.morrisons.com/browse,THE BEST,178974,https://groceries.morrisons.com/browse/178974,FRESH,178969,https://groceries.morrisons.com/browse/178974/178969,,,
    https://groceries.morrisons.com/browse,THE BEST,178974,https://groceries.morrisons.com/browse/178974,,,,,,""")

    text_csv: str = bin_input_csv.read().decode()
    bin_input_csv.seek(0)

    converted_content = [
        {'label': 'THE BEST', 'id': '178974', 'link': 'https://groceries.morrisons.com/browse/178974', 'children': [
            {'label': 'FRESH', 'id': '178969', 'link': 'https://groceries.morrisons.com/browse/178974/178969',
             'children': []}]}]
    yield bin_input_csv, text_csv, converted_content
    _files.clear()


def test_create_file(setup):
    bin_input_csv, text_csv, converted_content = setup
    message, status = create_file(bin_input_csv)
    file = _files.get(message['FileId'])
    assert status == 201
    assert file is not None
    assert file.content == text_csv
    assert file.converted_content == converted_content


def test_create_file_invalid():
    empty_file: BinaryIO = io.BytesIO(b"")
    _, status = create_file(empty_file)
    assert status == 400


def test_get_converted_file(setup):
    bin_input_csv, text_csv, converted_content = setup
    message, _ = create_file(bin_input_csv)
    file = message['FileId']
    message, status = get_converted_file(file)
    message['content'] = converted_content
    assert status == 200


def test_get_converted_file_not_found():
    _, status = get_converted_file('13213')
    assert status == 404


def test_delete_file(setup):
    bin_input_csv, text_csv, converted_content = setup
    message, _ = create_file(bin_input_csv)
    file = message['FileId']
    message, status = delete_file(file)
    assert status == 200
    assert _files.get(file) is None
