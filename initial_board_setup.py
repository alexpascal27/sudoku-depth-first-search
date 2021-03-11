import numpy as np
from typing import Tuple
from board_functions import BoardFunctions


class InitialBoardSetup:

    def __init__(self, board: np.array):
        self.board = board

        # Initialise the board functions object so we can call is_valid_pos, propagate and deal_with_1_picks functions
        self.board_functions = BoardFunctions()

    def get_changed_boards(self) -> Tuple[np.array, list]:
        """
        First check if the board is valid, it isn't return None to indicate that this board is invalid and therefore has no solution.
        Secondly, initialise the possible actions board so that we know what options we have instead of trying all numbers from 0 to 9.
        Lastly, propagate the effects of already assigned cells in hope of making life easier for us

        :return: a tuple containing the propagated board and possible_actions_board, or None if board is invalid
        """

        if not self._is_board_valid():
            return None

        possible_actions_board = self._init_possible_actions_board()

        return self._initial_propagation(self.board, possible_actions_board)

    def _is_board_valid(self) -> bool:
        """
        Check that every initially defined cell has a valid value.
        Check if the value of the cell doesn't occur vertically, horizontally or in the position's box

        :return: boolean saying whether all assigned positions are valid
        """

        for row in range(len(self.board)):
            for column in range(len(self.board[0])):
                # if found a cell that is not 0 (i.e. an assigned cell), we have to check if its position is valid
                cell_value = self.board[row][column]
                if cell_value > 0:
                    if not self.board_functions.is_valid_pos(self.board, (row, column), cell_value):
                        return False
        return True

    def _init_possible_actions_board(self) -> list:
        """
        Create a 3D array such that for each possible_actions_board[{row}][{column}] we get a list of numbers we can input on the board at that position

        :return: 3D array
        """

        possible_actions_board = []
        for row in range(len(self.board[0])):
            column_list = []
            for column in range(len(self.board[0])):
                if self.board[row][column] == 0:
                    column_list.append([1, 2, 3, 4, 5, 6, 7, 8, 9])
                else:
                    column_list.append([])
            possible_actions_board.append(column_list)
        return possible_actions_board

    def _initial_propagation(self, board: np.array, possible_actions_board: list) -> Tuple[np.array, list]:
        """
        For every initially assigned cell propagate the effects of that cell being assigned the value that it has
        e.g. if we have a 1 at position (0,0) remove the possibility of putting a 1 in unassigned cells, in the first row and the first column, as well as the cells in the box that (0,0) is part of
        Additionally, if at any point we find that we have only one option for a cell assign the value to the cell.

        :param board: numpy array of a n x n int board or grid in range [1..9]
        :param possible_actions_board: a 3D list such that for each possible_actions_board[{row}][{column}] we get a list of numbers we can input on the board at that position
        :return: a tuple containing the propagated board and possible_actions_board
        """

        new_board = np.copy(board)
        new_possible_actions_board = list.copy(possible_actions_board)
        for row in range(len(new_board)):
            for column in range(len(new_board[0])):
                # If defined
                temp_value = new_board[row][column]
                if temp_value != 0:
                    new_board, new_possible_actions_board = self.board_functions.propagate(new_board,
                                                                                           new_possible_actions_board,
                                                                                           (row, column), temp_value)
                    new_board, new_possible_actions_board = self.board_functions.deal_with_1_picks(new_board,
                                                                                                   new_possible_actions_board)
        return new_board, new_possible_actions_board
