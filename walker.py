from constants import *


class Walker:
    row = 0
    col = 0
    last_move = None

    def __init__(self, row: int, col: int):
        self.col = col
        self.row = row

    @property
    def position(self):
        """
        The position of the walker
        :return: (row, col)
        """
        return self.row, self.col

    def move(self, move: str) -> None:
        """
        Move the walker
        :param move: what move
        :return: None
        """
        self.last_move = move
        if move == DOWN:
            self.row += 1
        elif move == UP:
            self.row -= 1
        elif move == LEFT:
            self.col -= 1
        elif move == RIGHT:
            self.col += 1

    def go_back(self) -> None:
        """
        Move the walker back
        :param move: what move
        :return: None
        """
        if self.last_move == DOWN:
            self.row -= 1
        elif self.last_move == UP:
            self.row += 1
        elif self.last_move == LEFT:
            self.col += 1
        elif self.last_move == RIGHT:
            self.col -= 1
