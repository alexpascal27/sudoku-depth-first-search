import numpy as np
from typing import Tuple, List
from board_functions import BoardFunctions
import copy


class SudokuBoardState:

    def __init__(self, current_pos: Tuple[int, int], board: np.array, possible_actions_board: list,
                 parent=None,
                 action: Tuple[Tuple[int, int], int] = None):
        print("-------------")
        print(current_pos)
        print()
        self.print_2d_list(board)
        print()
        self.print_2d_list(possible_actions_board)
        print("-------------")

        self.current_pos = current_pos
        self.board = copy.deepcopy(board)
        self.possible_actions_board = copy.deepcopy(possible_actions_board)
        self.parent = parent
        self.action = action
        self.board_functions = BoardFunctions()


    def get_possible_actions_board(self):
        return self.possible_actions_board

    def get_current_pos(self):
        return self.current_pos

    def get_board(self):
        return self.board

    def get_parent(self):
        return self.parent

    def print_2d_list(self, collection: list):
        print("[")
        for i in range(len(collection)):
            print(collection[i])
        print("]")

    def next_state(self, pos: Tuple[int, int], n: int):
        row, column = pos

        new_board = copy.deepcopy(self.board)
        new_possible_actions_board = copy.deepcopy(self.possible_actions_board)

        # Assign the cell we are exploring to the value
        new_board[row][column] = n
        new_possible_actions_board[row][column] = []

        # Propagate the effect of the assignment
        new_board, new_possible_actions_board = self.board_functions.propagate(new_board, new_possible_actions_board, (row, column), n)

        # Check for only 1 possible remaining option
        new_board, new_possible_actions_board = self.board_functions.deal_with_1_picks(new_board, new_possible_actions_board)

        return SudokuBoardState(current_pos=pos, board=new_board, possible_actions_board=new_possible_actions_board,
                                parent=self)

    def is_goal_state(self) -> bool:
        for row in range(len(self.board)):
            for column in range(len(self.board[0])):
                # if free cell, that is the next cell to explore
                if self.board[row][column] == 0:
                    return False
        return True

    def _find_next_pos(self) -> Tuple[int, int]:
        # Given our current position, find the next unassigned position (i.e. board[r][c] == 0)
        row, column = self.current_pos

        # Search normally on the remaining rows
        how_many_rows_left = len(self.board) - row
        if how_many_rows_left > 0:
            for r in range(row, len(self.board)):
                for c in range(len(self.board[0])):
                    if self.board[r][c] == 0:
                        return r, c

        return None

    def possible_actions(self) -> Tuple[Tuple[int, int], list]:
        next_pos = self._find_next_pos()
        # If couldn't find a next position then return none as there are no possible actions left
        if next_pos is None:
            return None

        r, c = next_pos
        return (r, c), self.possible_actions_board[r][c]
