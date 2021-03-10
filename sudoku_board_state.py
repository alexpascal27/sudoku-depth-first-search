import numpy as np
from typing import Tuple
from board_functions import BoardFunctions
import copy


class SudokuBoardState:

    def __init__(self, current_pos: Tuple[int, int], board: np.array, possible_actions_board: list):
        self.current_pos = current_pos
        self.board = board
        self.possible_actions_board = possible_actions_board
        self.board_functions = BoardFunctions()

    def get_board(self):
        return self.board

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

        return SudokuBoardState(current_pos=pos, board=new_board, possible_actions_board=new_possible_actions_board)

    # Could check the entire board or just find the next pos - if returns None then we are goal state
    def is_goal_state(self) -> bool:
        return self._find_next_pos() is None

    # Could check the entire board but instead check from current position since we wont have unassigned cells before current position
    def _find_next_pos(self) -> Tuple[int, int]:
        # Given our current position, find the next unassigned position (i.e. board[r][c] == 0)
        row, column = self.current_pos

        # Check columns left in current row
        how_many_columns_left = len(self.board[0]) - column
        for c in range(how_many_columns_left):
            if self.board[row][c+column] == 0:
                return row, c+column

        # We already searched current row so search normally on the remaining rows
        how_many_rows_left = len(self.board) - row - 1

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
