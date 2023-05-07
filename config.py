from enum import Enum, unique
from types import DynamicClassAttribute
from pathlib import Path as p


@unique
class FilePaths(Enum):
    WORD_OF_THE_DAY_DATA = p.cwd() / 'data_files/word_of_the_day_data.txt'

    @DynamicClassAttribute
    def path(self):
        return {
            self.WORD_OF_THE_DAY_DATA: self.WORD_OF_THE_DAY_DATA.value,
        }[self]


class Color(Enum):
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
