import numpy as np
from typing import Tuple, List


class SudokuBoardState:

    def __init__(self, board: np.array, possible_actions_board: list, parent_board: np.array = None, parent_possible_actions_board: list = None):
        self.board = board
        self.possible_actions_board = possible_actions_board
        self.parent_board = parent_board
        self.parent_possible_actions_board = parent_possible_actions_board

    def next_state(self, pos: Tuple[int, int], n: int):
        row, column = pos

        new_board = np.copy(self.board)
        new_possible_actions_board = list.copy(self.possible_actions_board)

        # Assign the cell we are exploring to the value
        new_board[row][column] = n
        new_possible_actions_board[row][column].pop(0)

        # Propagate the effect of the assignment
        new_board, new_possible_actions_board = self._propagate(new_board, new_possible_actions_board, (row, column), n)
        return SudokuBoardState(board=new_board, possible_actions_board=new_possible_actions_board, parent_board=self.board, parent_possible_actions_board=self.possible_actions_board)

    def is_goal_state(self) -> bool:
        for row in range(len(self.board)):
            for column in range(len(self.board[0])):
                # if free cell, that is the next cell to explore
                if self.board[row][column] == 0:
                    return False
        return True

    def possible_actions(self, pos: Tuple[int, int]) -> list:
        r, c = pos
        return self.possible_actions_board[r][c]

    def _in_box(self, board: np.array, pos: Tuple[int, int], n: int) -> bool:
        r, c = pos
        range_r = self._find_box_range(r)
        range_c = self._find_box_range(c)

        for row in range_r:
            for column in range_c:
                if row == r and column == c:
                    continue

                if board[row][column] == n:
                    return True
        return False

    def _in_horizontal(self, board: np.array, pos: Tuple[int, int], n: int) -> bool:
        r, c = pos
        # Search entire row
        for column in range(9):
            if column == c:
                continue
            # Number is in this row
            if board[r][column] == n:
                return True
        return False

    def _in_vertical(self, board: np.array, pos: Tuple[int, int], n: int) -> bool:
        r, c = pos
        # Search entire column
        for row in range(9):
            if row == r:
                continue
            # Number is in this column
            if board[row][c] == n:
                return True
        return False

    def _is_valid_pos(self, board: np.array, pos: Tuple[int, int], n: int) -> bool:
        return not self._in_box(board, pos, n) and not self._in_horizontal(board, pos, n) and not self._in_vertical(board, pos, n)

    def _deal_with_1_possible_action(self, board: np.array, possible_actions_board: list, pos: Tuple[int, int]) -> Tuple[np.array, list]:
        new_board = np.copy(board)
        new_possible_actions_board = list.copy(possible_actions_board)

        r, c = pos
        only_remaining_option = new_possible_actions_board[r][c][0]

        # If the only remaining option is valid, then pick it, otherwise return an unchanged board and empty possible action board
        if self._is_valid_pos(new_board, pos, only_remaining_option):
            new_board[r][c] = only_remaining_option
            new_possible_actions_board[r][c] = []
            # Propagate the effect of the assignment
            return self._propagate(new_board, new_possible_actions_board, (r, c), only_remaining_option)
        # Position is not valid
        else:
            new_possible_actions_board[r][c] = []
            return new_board, new_possible_actions_board

    def _propagate_horizontally(self, board: np.array, possible_actions_board: list, pos: Tuple[int, int], n: int) -> Tuple[np.array, list]:
        new_board = np.copy(board)
        new_possible_actions_board = list.copy(possible_actions_board)
        # Get the row and column of the position
        r, c = pos
        indexes_to_check = [*range(9)]
        indexes_to_check.pop(c)

        for i in indexes_to_check:
            try:
                # If we find n in the array of possible actions, remove it
                index_of_n = new_possible_actions_board[r][i].index(n)
                new_possible_actions_board[r][i].pop(index_of_n)
                # If we only have an option for an action, pick that action
                if len(new_possible_actions_board[r][i]) == 1:
                    new_board, new_possible_actions_board = self._deal_with_1_possible_action(new_board, new_possible_actions_board, (r, i))

            # If couldn't find n we dont need to do anything
            except ValueError:
                pass

        return new_board, new_possible_actions_board

    def _propagate_vertically(self, board: np.array, possible_actions_board: list, pos: Tuple[int, int], n: int) -> Tuple[np.array, list]:
        new_board = np.copy(board)
        new_possible_actions_board = list.copy(possible_actions_board)

        # Get the row and column of the position
        r, c = pos
        indexes_to_check = [*range(9)]
        indexes_to_check.pop(r)
        for i in indexes_to_check:
            try:
                # If we find n in the array of possible actions, remove it
                new_possible_actions_board[i][c].pop(new_possible_actions_board[i][c].index(n))
                # If we only have an option for an action, pick that action
                if len(new_possible_actions_board[i][c]) == 1:
                    new_board, new_possible_actions_board = self._deal_with_1_possible_action(new_board, new_possible_actions_board, (i, c))

            # If couldn't find n we dont need to do anything
            except ValueError:
                pass

        return new_board, new_possible_actions_board

    def _find_box_range(self, i: int) -> List[int]:
        if 0 <= i < 3:
            return [0, 1, 2]
        if 3 <= i < 6:
            return [3, 4, 5]
        else:
            return [6, 7, 8]

    def _propagate_box_wise(self, board: np.array, possible_actions_board: list, pos: Tuple[int, int], n: int) -> Tuple[np.array, list]:
        new_board = np.copy(board)
        new_possible_actions_board = list.copy(possible_actions_board)

        r, c = pos
        range_r = self._find_box_range(r)
        range_c = self._find_box_range(c)

        for row in range_r:
            for column in range_c:
                if row == r and column == c:
                    continue
                try:
                    # If we find n in the array of possible actions, remove it
                    new_possible_actions_board[row][column].pop(new_possible_actions_board[row][column].index(n))
                    # If we only have an option for an action, pick that action
                    if len(new_possible_actions_board[row][column]) == 1:
                        new_board, possible_actions_board = self._deal_with_1_possible_action(new_board, new_possible_actions_board, (row, column))

                    break

                # If couldn't find n we dont need to do anything
                except ValueError:
                    pass
        return new_board, new_possible_actions_board

    def _propagate(self, board: np.array, possible_actions_board: list, pos: Tuple[int, int], n: int) -> Tuple[np.array, list]:
        board, possible_actions_board = self._propagate_horizontally(board, possible_actions_board, pos, n)
        board, possible_actions_board = self._propagate_vertically(board, possible_actions_board, pos, n)
        board, possible_actions_board = self._propagate_box_wise(board, possible_actions_board, pos, n)
        return board, possible_actions_board
