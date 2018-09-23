from typing import List

import numpy as np

from constants import *
from walker import Walker


def is_good_structure(structure):
    good_values = np.all(np.isin(structure, POSSIBLE_VALUES))
    good_shape = len(structure.shape) == 2
    return good_values and good_shape


def get_indices_of(array, item):
    indices = np.where(array == item)
    return indices[0][0], indices[1][0]


class Maze:
    structure = np.zeros(0)
    start = (0, 0)
    end = (0, 0)

    def __init__(self, structure: List[List[int]]):
        self.structure = np.array(structure)

        if not is_good_structure(self.structure):
            raise ValueError('Structure not valid')

        self.start = get_indices_of(self.structure, START)
        self.end = get_indices_of(self.structure, END)

    def make_a_try(self, moves: List[str]):
        """
        Try to solve the maze
        :param moves: list of actions. d=down, u=up, l=left, r=right
        :return: (if made it to the end (last row visited, last column visited))
        """

        walker = Walker(*self.start)

        def cant_go_there() -> bool:
            outside = len(self.structure) < walker.row < 0
            in_a_wall = self.structure[walker.row][walker.col] == WALL

            return outside or in_a_wall

        move_count = 0
        for move in moves:
            walker.move(move)
            move_count += 1

            if cant_go_there():
                walker.go_back()
                move_count -= 1
                return False, walker.position, move_count

            if self.structure[walker.row][walker.col] == END:
                return True, walker.position, move_count

        return self.structure[walker.row][walker.col] == END, walker.position, move_count

    @staticmethod
    def flying_distance(point_1, point_2) -> int:
        """
        Calculate distance between point to end
        :return: distance
        """
        return abs(point_1[0] - point_2[0]) + abs(point_1[1] - point_2[1])
