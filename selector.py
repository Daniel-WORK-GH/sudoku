import random
from enum import Enum

#boards taken from https://www.printable-sudoku-puzzles.com/wfiles/

class Difficuly(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3

class Selector:
    files = {
        Difficuly.EASY : 'boards\\easy.txt',
        Difficuly.MEDIUM : 'boards\\medium.txt',
        Difficuly.HARD : 'boards\\hard.txt',
    } 

    def __init__(self, difficulty = Difficuly.EASY) -> None:
        self.difficulty = difficulty
        self.boards_file = Selector.files[difficulty]
        self.used_boards = []

    def get_unused_id(self) -> int:
        """returns a uniqe id for board for currnt difficuly"""
        while True:
            board_id = random.randint(0, 10000)
            if board_id not in self.used_boards:
                self.used_boards.append(board_id)
                return board_id

    def get_board(self) -> str:
        """returns a uniqe board from file"""
        with open(self.boards_file) as file:
            board_id = self.get_unused_id()
            file.seek(board_id * (81 + 2))
            line = file.readline()
        return line
