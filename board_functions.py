import numpy as np
from typing import Tuple, List
import copy


class BoardFunctions:

    def _find_box_range(self, i: int) -> List[int]:
        if 0 <= i < 3:
            return [0, 1, 2]
        if 3 <= i < 6:
            return [3, 4, 5]
        else:
            return [6, 7, 8]

    def _in_box(self, board: np.array, pos: Tuple[int, int], n: int, check_current_pos: bool) -> bool:
        r, c = pos
        range_r = self._find_box_range(r)
        range_c = self._find_box_range(c)

        for row in range_r:
            for column in range_c:
                if not check_current_pos:
                    continue

                if board[row][column] == n:
                    return True
        return False

    def _in_horizontal(self, board: np.array, pos: Tuple[int, int], n: int, check_current_pos: bool) -> bool:
        r, c = pos
        # Search entire row
        for column in range(9):
            if not check_current_pos:
                continue
            # Number is in this row
            if board[r][column] == n:
                return True
        return False

    def _in_vertical(self, board: np.array, pos: Tuple[int, int], n: int, check_current_pos: bool) -> bool:
        r, c = pos
        # Search entire column
        for row in range(9):
            if not check_current_pos:
                continue
            # Number is in this column
            if board[row][c] == n:
                return True
        return False

    def is_valid_pos(self, board: np.array, pos: Tuple[int, int], n: int, check_current_pos: bool) -> bool:
        return not self._in_box(board, pos, n, check_current_pos) and not self._in_horizontal(board, pos, n, check_current_pos) and not self._in_vertical(
            board, pos, n, check_current_pos)

    def _propagate_horizontally(self, board: np.array, possible_actions_board: list, pos: Tuple[int, int], n: int) -> Tuple[np.array, list]:
        new_board = copy.deepcopy(board)
        new_possible_actions_board = copy.deepcopy(possible_actions_board)
        # Get the row and column of the position
        r, c = pos
        indexes_to_check = [*range(9)]

        for i in indexes_to_check:
            try:
                # If we find n in the array of possible actions, remove it
                index_of_n = new_possible_actions_board[r][i].index(n)
                new_possible_actions_board[r][i].pop(index_of_n)
            # If couldn't find n we dont need to do anything
            except ValueError:
                pass

        return self._propagate_vertically(new_board, new_possible_actions_board, pos, n)

    def _propagate_vertically(self, board: np.array, possible_actions_board: list, pos: Tuple[int, int], n: int) -> Tuple[np.array, list]:
        new_board = copy.deepcopy(board)
        new_possible_actions_board = copy.deepcopy(possible_actions_board)

        # Get the row and column of the position
        r, c = pos
        indexes_to_check = [*range(9)]
        for i in indexes_to_check:
            try:
                # If we find n in the array of possible actions, remove it
                index_of_n = new_possible_actions_board[i][c].index(n)
                # print("Index of " + str(n) + " at position[" + str(pos[0]) + "][" + str(pos[1]) + "]: " + str(index_of_n))
                new_possible_actions_board[i][c].pop(index_of_n)

            # If couldn't find n we dont need to do anything
            except ValueError:
                pass

        return self._propagate_box_wise(new_board, new_possible_actions_board, pos, n)

    def _propagate_box_wise(self, board: np.array, possible_actions_board: list, pos: Tuple[int, int], n: int) -> Tuple[np.array, list]:
        new_board = copy.deepcopy(board)
        new_possible_actions_board = copy.deepcopy(possible_actions_board)

        r, c = pos
        range_r = self._find_box_range(r)
        range_c = self._find_box_range(c)

        for row in range_r:
            for column in range_c:
                try:
                    # If we find n in the array of possible actions, remove it
                    new_possible_actions_board[row][column].pop(new_possible_actions_board[row][column].index(n))

                # If couldn't find n we dont need to do anything
                except ValueError:
                    pass

        return new_board, new_possible_actions_board

    def propagate(self, board: np.array, possible_actions_board: list, pos: Tuple[int, int], n: int) -> Tuple[np.array, list]:
        # print("Propagate")
        # self.print_2d_list(possible_actions_board)
        return self._propagate_horizontally(board, possible_actions_board, pos, n)

    def print_2d_list(self, collection: list):
        print("[")
        for i in range(len(collection)):
            print(collection[i])
        print("]")
