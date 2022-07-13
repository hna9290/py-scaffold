import pytest

from app.converter.converter import convert


def test_convert_non_sequential():
    """Test data when the sequence of parent and children is reversed"""
    input_csv: str = """Base URL,Level 1 - Name,Level 1 - ID,Level 1 - URL,Level 2 - Name,Level 2 - ID,Level 2 - URL,Level 3 - Name,Level 3 - ID,Level 3 - URL
https://groceries.morrisons.com/browse,THE BEST,178974,https://groceries.morrisons.com/browse/178974,FRESH,178969,https://groceries.morrisons.com/browse/178974/178969,,,
https://groceries.morrisons.com/browse,THE BEST,178974,https://groceries.morrisons.com/browse/178974,,,,,,"""
    assert convert(input_csv) == [
        {'label': 'THE BEST', 'id': '178974', 'link': 'https://groceries.morrisons.com/browse/178974', 'children': [
            {'label': 'FRESH', 'id': '178969', 'link': 'https://groceries.morrisons.com/browse/178974/178969',
             'children': []}]}]


def test_convert_sequential():
    """Normal test case sequential data"""
    input_csv: str = """Base URL,Level 1 - Name,Level 1 - ID,Level 1 - URL,Level 2 - Name,Level 2 - ID,Level 2 - URL,Level 3 - Name,Level 3 - ID,Level 3 - URL
https://groceries.morrisons.com/browse,THE BEST,178974,https://groceries.morrisons.com/browse/178974,,,,,,
https://groceries.morrisons.com/browse,THE BEST,178974,https://groceries.morrisons.com/browse/178974,FRESH,178969,https://groceries.morrisons.com/browse/178974/178969,,,"""
    assert convert(input_csv) == [
        {'label': 'THE BEST', 'id': '178974', 'link': 'https://groceries.morrisons.com/browse/178974', 'children': [
            {'label': 'FRESH', 'id': '178969', 'link': 'https://groceries.morrisons.com/browse/178974/178969',
             'children': []}]}]


def test_convert_empty_rows():
    """Test with blamnk rows in file"""
    input_csv: str = """Base URL,Level 1 - Name,Level 1 - ID,Level 1 - URL,Level 2 - Name,Level 2 - ID,Level 2 - URL,Level 3 - Name,Level 3 - ID,Level 3 - URL
https://groceries.morrisons.com/browse,THE BEST,178974,https://groceries.morrisons.com/browse/178974,,,,,,
,,,,,,,,,
https://groceries.morrisons.com/browse,THE BEST,178974,https://groceries.morrisons.com/browse/178974,FRESH,178969,https://groceries.morrisons.com/browse/178974/178969,,,"""
    assert convert(input_csv) == [
        {'label': 'THE BEST', 'id': '178974', 'link': 'https://groceries.morrisons.com/browse/178974', 'children': [
            {'label': 'FRESH', 'id': '178969', 'link': 'https://groceries.morrisons.com/browse/178974/178969',
             'children': []}]}]


def test_convert_multi_level():
    """Test for more levels of menu"""
    input_csv: str = """Base URL,Level 1 - Name,Level 1 - ID,Level 1 - URL,Level 2 - Name,Level 2 - ID,Level 2 - URL,Level 3 - Name,Level 3 - ID,Level 3 - URL,Level 4 - Name,Level 4 - ID,Level 4 - URL
https://groceries.morrisons.com/browse,THE BEST,178974,https://groceries.morrisons.com/browse/178974,,,,,,,,,
https://groceries.morrisons.com/browse,THE BEST,178974,https://groceries.morrisons.com/browse/178974,FRESH,178969,https://groceries.morrisons.com/browse/178974/178969,,,,,,
https://groceries.morrisons.com/browse,THE BEST,178974,https://groceries.morrisons.com/browse/178974,FRESH,178969,https://groceries.morrisons.com/browse/178974/178969,CHEESE,178975,https://groceries.morrisons.com/browse/178974/178969/178975,,,
https://groceries.morrisons.com/browse,THE BEST,178974,https://groceries.morrisons.com/browse/178974,FRESH,178969,https://groceries.morrisons.com/browse/178974/178969,CHEESE,178975,https://groceries.morrisons.com/browse/178974/178969/178975,BLUE-CHEESE,178976,https://groceries.morrisons.com/browse/178974/178969/178975/178976"""
    assert convert(input_csv) == [
        {'label': 'THE BEST', 'id': '178974', 'link': 'https://groceries.morrisons.com/browse/178974', 'children': [
            {'label': 'FRESH', 'id': '178969', 'link': 'https://groceries.morrisons.com/browse/178974/178969',
             'children': [{'label': 'CHEESE', 'id': '178975',
                           'link': 'https://groceries.morrisons.com/browse/178974/178969/178975', 'children': [
                     {'label': 'BLUE-CHEESE', 'id': '178976',
                      'link': 'https://groceries.morrisons.com/browse/178974/178969/178975/178976',
                      'children': []}]}]}]}]


def test_convert_empty_csv():
    """Test empty csv should raise Exception"""
    input_csv: str = ""
    with pytest.raises(TypeError):
        convert(input_csv)
