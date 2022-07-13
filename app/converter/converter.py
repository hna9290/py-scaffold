"""Business Logic which actually converts CSV to JSON"""

import csv
import re
from io import StringIO
from typing import Dict, Set, Union, TextIO, List

from app.constants import BaseConfig as config
from app.converter.model import MorrisonsMenu
from app.converter.logger import log_info, log_debug


@log_debug
def _get_row_levels(row: Dict) -> List:
    """
    It checks how many levels are there in a row of the csv data file.
    :param row: Respective row of the csv file.
    :return: A list indicating the number of levels.
    """
    levels: List = []
    for column in row:
        level_obj = re.search(config.LEVEL_REGEX, column)
        level = level_obj.group() if level_obj else None
        if level and row[config.LEVEL + level + config.URL]:
            if level not in levels:
                levels.append(level)
    return levels


def is_valid():
    """Place holder for future use"""


@log_debug
def _create_child_item(row: Dict, level: str) -> MorrisonsMenu:
    """
    Convert the row from CSV into MorrisonsMenu format.
    :param row: Respective child item to be converted.
    :param level: Level from row to be converted to required format.
    :return: MorrisonsMenu
    """
    node: MorrisonsMenu = dict(label=row[config.LEVEL + level + config.NAME],
                               id=row[config.LEVEL + level + config.LEVEL_ID],
                               link=row[config.LEVEL + level + config.URL],
                               children=[]
                               )
    return node


@log_debug
def _add_child_to_tree(row: MorrisonsMenu, tree: List[MorrisonsMenu], parent_levels: List) -> None:
    """
    Recursively finds parent node and adds child to it.
    :param row: Respective child item to be added.
    :param tree: Tree in which the child needs to be added.
    :param parent_levels: Ordered list of parent ids.
    :return: None
    """
    if not parent_levels:
        tree.append(row)
        return
    for node in tree:
        if node['id'] == parent_levels[0]:
            _add_child_to_tree(row, node['children'], parent_levels[1:])


@log_info
def convert(csv_contents: Union[str, TextIO]) -> Union[List[MorrisonsMenu], List]:
    """
    Converts input file like object or string CSV to JSON Menu. Empty rows will be ignored.
    :param csv_contents: CSV file as Sting or text file like object.
    :return: Converted JSON Menu
    """
    if not csv_contents:
        raise TypeError('Invalid CSV file. Please check')
    item_tree: List[MorrisonsMenu] = []
    ids_tracker: Set = set()
    if isinstance(csv_contents, str):
        csv_contents = StringIO(csv_contents)
    for row in csv.DictReader(csv_contents):
        parent_ids: List = list()
        for level in _get_row_levels(row):
            child: MorrisonsMenu = _create_child_item(row, level)
            if child['id'] in ids_tracker:
                parent_ids.append(child['id'])
                continue
            ids_tracker.add(child['id'])
            _add_child_to_tree(child, item_tree, parent_ids)
            parent_ids.append(child['id'])
    return item_tree
