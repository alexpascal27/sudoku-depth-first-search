import numpy as np
from typing import Tuple, List
from board_functions import BoardFunctions
import copy

class InitialBoardSetup:

    def __init__(self, board: np.array):
        self.board = board

        # Initialise the board functions object so we can call is_valid_pos and propagate functions
        self.board_functions = BoardFunctions()

    def get_changed_boards(self) -> Tuple[np.array, list]:
        if not self._is_board_valid():
            return None

        possible_actions_board = self._init_possible_actions_board()

        return self._initial_propagation(self.board, possible_actions_board)

    def _is_board_valid(self) -> bool:
        for row in range(len(self.board[0])):
            for column in range(len(self.board[0])):
                # if found a cell that is above 0, we have to check if its position is valid
                cell_value = self.board[row][column]
                if cell_value > 0:
                    if not self.board_functions.is_valid_pos(self.board, (row, column), cell_value, check_current_pos=False):
                        return False
        return True

    def _init_possible_actions_board(self) -> list:
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
        new_board = np.copy(board)
        new_possible_actions_board = list.copy(possible_actions_board)
        for row in range(len(new_board)):
            for column in range(len(new_board[0])):
                # If defined
                temp_value = new_board[row][column]
                if temp_value != 0:
                    new_board, new_possible_actions_board = self.board_functions.propagate(new_board, new_possible_actions_board, (row, column), temp_value)
        return new_board, new_possible_actions_board

