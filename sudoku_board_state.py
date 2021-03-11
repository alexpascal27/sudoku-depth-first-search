import numpy as np
from typing import Tuple
from board_functions import BoardFunctions
import copy


class SudokuBoardState:

    def __init__(self, current_pos: Tuple[int, int], board: np.array, possible_actions_board: list):
        """
        Sets the local values according to the inputted parameters

        :param current_pos: tuple in form ({row}, {column})
        :param board: numpy array of a n x n int board or grid in range [1..9]
        :param possible_actions_board: a 3D list such that for each possible_actions_board[{row}][{column}] we get a list of numbers we can input on the board at that position
        """
        self.current_pos = current_pos
        self.board = board
        self.possible_actions_board = possible_actions_board
        self.board_functions = BoardFunctions()

    def get_board(self):
        return self.board

    def next_state(self, pos: Tuple[int, int], n: int):
        """
        Take current state, assign a value to a cell and generate a new state

        :param pos: tuple in form ({row}, {column})
        :param n: int that represents what value we should put in the cell at the specified position
        :return: new SudokuBoardState that represents the board and possible_actions_board after our cell assignment
        """
        row, column = pos

        # As python is pass by reference we need to copy arrays when we make changes to them so that the original arrays are not changed when the copied arrays are changed
        new_board = copy.copy(self.board)
        # As possible_actions_board is 3D we need a deep copy for it not to change the original array it copied from
        new_possible_actions_board = copy.deepcopy(self.possible_actions_board)

        # Assign the cell we are exploring to the value and make sure we can't pick any other values for that cell anymore
        new_board[row][column] = n
        new_possible_actions_board[row][column] = []

        # Propagate the effect of the assignment
        new_board, new_possible_actions_board = self.board_functions.propagate(new_board, new_possible_actions_board, (row, column), n)

        # Check for only 1 possible remaining options (if there is only one option for a cell - pick that option)
        new_board, new_possible_actions_board = self.board_functions.deal_with_1_picks(new_board, new_possible_actions_board)

        return SudokuBoardState(current_pos=pos, board=new_board, possible_actions_board=new_possible_actions_board)


    def is_goal_state(self) -> bool:
        """
        Looks for empty cells beyond our current location.
        Could check the entire board but more efficient to just find the next pos - if returns None then we are goal state

        :return: boolean confirming if the board is in the goal state
        """
        return self._find_next_pos() is None

    def _find_next_pos(self) -> Tuple[int, int]:
        """
        Look for an empty unassigned cell beyond our current location.
        Could check the entire board but instead check from current position since we wont have unassigned cells before current position

        :return: tuple in form ({row}, {column})
        """

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
            for r in range(how_many_rows_left):
                for c in range(len(self.board[0])):
                    if self.board[r+row][c] == 0:
                        return r+row, c

        return None

    def possible_actions(self) -> Tuple[Tuple[int, int], list]:
        """
        Find the next unassigned cell in the board and then get the possible actions at that position

        :return: an action i.e. tuple in form (({row}, {column}), {possible n values for that cell})
        """

        next_pos = self._find_next_pos()
        # If couldn't find a next position then return none as there are no possible actions left
        if next_pos is None:
            return None

        r, c = next_pos
        return (r, c), self.possible_actions_board[r][c]
