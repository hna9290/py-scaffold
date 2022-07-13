"""All data structures are here"""

from dataclasses import dataclass
from typing import TypedDict, List


@dataclass
class UploadedFiles():
    """DataStructure for storing uploaded files in memory"""

    def __init__(self):
        self.content: str = ''
        self.hash: str = ''
        self.converted_content = ''


class MorrisonsMenu(TypedDict):
    """Model for static type checking nodes of JSON menu"""
    label: str
    id: str
    link: str
    children: List
