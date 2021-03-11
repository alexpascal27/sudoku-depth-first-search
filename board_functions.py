import numpy as np
from typing import Tuple, List
import copy


class BoardFunctions:
    """
    Class that contains common board functions, such as:
    * checking if a position is valid
    * propagating the effect of the value of a cell
    * dealing with cells that have a single option for values to pick
    """

    def _find_box_range(self, i: int) -> List[int]:
        """
        Given an index find neighbours for that index

        :param i: either the index of a column or row (irrelevant as board is n x n)
        :return: list of neighbours around that index
        """
        if 0 <= i < 3:
            return [0, 1, 2]
        if 3 <= i < 6:
            return [3, 4, 5]
        else:
            return [6, 7, 8]

    def _in_box(self, board: np.array, pos: Tuple[int, int], n: int) -> bool:
        """
        Given a position find the box that the position is in and use the input value to see if there is a cell within the box that has that value.

        :param board: numpy array of a n x n int board or grid in range [1..9]
        :param pos: tuple in form ({row}, {column})
        :param n: int that represents what value we should check for
        :return: boolean representing if the value is in the box (ignore the current the position when checking the box)
        """

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
        """
        Given a position check the rows for the position's column for the value.

        :param board: numpy array of a n x n int board or grid in range [1..9]
        :param pos: tuple in form ({row}, {column})
        :param n: int that represents what value we should check for
        :return: boolean representing if the value is in any row given the column (ignore the current position's row)
        """

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
        """
        Given a position check the columns for the position's row for the value.

        :param board: numpy array of a n x n int board or grid in range [1..9]
        :param pos: tuple in form ({row}, {column})
        :param n: int that represents what value we should check for
        :return: boolean representing if the value is in any column given the row (ignore the current position's column)
        """

        r, c = pos
        # Search entire column
        for row in range(9):
            if row == r:
                continue
            # Number is in this column
            if board[row][c] == n:
                return True
        return False

    def is_valid_pos(self, board: np.array, pos: Tuple[int, int], n: int) -> bool:
        """
        If we enter the value at the specified position, return whether it would be a valid move.
        This means the value shouldn't be in the vertical or horizontal direction, or in the position's box.

        :param board: numpy array of a n x n int board or grid in range [1..9]
        :param pos: tuple in form ({row}, {column})
        :param n: int that represents what value we should check for
        :return: boolean representing if the value at the position is valid
        """

        # We first check if value is in vertical direction, if it is means the position is not valid and we do not need to check other directions
        in_vertical = self._in_vertical(board, pos, n)
        if in_vertical:
            return False

        #  We first check if value is in horizontal direction, if it is means the position is not valid and we do not need to check other directions
        in_horizontal = self._in_horizontal(board, pos, n)
        if in_horizontal:
            return False

        # If we reached this point it means its not in vertical or horizontal so just check box-wise
        return not self._in_box(board, pos, n)

    def _propagate_horizontally(self, board: np.array, possible_actions_board: list, pos: Tuple[int, int], n: int) -> Tuple[np.array, list]:
        """
        Given a current board and possible actions board, we propagate the effect of assigning the value of n to the specified position, in the horizontal direction.

        :param board: numpy array of a n x n int board or grid in range [1..9]
        :param possible_actions_board: a 3D list such that for each possible_actions_board[{row}][{column}] we get a list of numbers we can input on the board at that position
        :param pos: tuple in form ({row}, {column})
        :param n: value at the given position
        :return: a tuple containing the changed board and possible_actions_board, given after propagating in the vertical direction
        """

        new_board = copy.copy(board)
        new_possible_actions_board = copy.copy(possible_actions_board)
        # Get the row and column of the position
        r, c = pos
        indexes_to_check = [*range(9)]
        # Check all columns for the given row
        for i in indexes_to_check:
            try:
                # If we find n in the array of possible actions, remove it
                index_of_n = new_possible_actions_board[r][i].index(n)
                new_possible_actions_board[r][i].pop(index_of_n)
            # If couldn't find n we dont need to do anything
            except ValueError:
                pass

        # Propagate in vertical direction next
        return self._propagate_vertically(new_board, new_possible_actions_board, pos, n)

    def _propagate_vertically(self, board: np.array, possible_actions_board: list, pos: Tuple[int, int], n: int) -> Tuple[np.array, list]:
        """
        Given a current board and possible actions board, we propagate the effect of assigning the value of n to the specified position, in the vertical direction.

        :param board: numpy array of a n x n int board or grid in range [1..9]
        :param possible_actions_board: a 3D list such that for each possible_actions_board[{row}][{column}] we get a list of numbers we can input on the board at that position
        :param pos: tuple in form ({row}, {column})
        :param n: value at the given position
        :return: a tuple containing the changed board and possible_actions_board, given after propagating box-wise
        """

        new_board = copy.copy(board)
        new_possible_actions_board = copy.copy(possible_actions_board)

        # Get the row and column of the position
        r, c = pos
        indexes_to_check = [*range(9)]
        for i in indexes_to_check:
            try:
                # If we find n in the array of possible actions, remove it
                index_of_n = new_possible_actions_board[i][c].index(n)
                new_possible_actions_board[i][c].pop(index_of_n)

            # If couldn't find n we dont need to do anything
            except ValueError:
                pass

        # Propagate in box-wise next
        return self._propagate_box_wise(new_board, new_possible_actions_board, pos, n)

    def _propagate_box_wise(self, board: np.array, possible_actions_board: list, pos: Tuple[int, int], n: int) -> Tuple[np.array, list]:
        """
        Given a current board and possible actions board, we propagate the effect of assigning the value of n to the specified position, box-wise.
        We first find what box the position is in and then propagate the effect of the assignment on all cells in the box.

        :param board: numpy array of a n x n int board or grid in range [1..9]
        :param possible_actions_board: a 3D list such that for each possible_actions_board[{row}][{column}] we get a list of numbers we can input on the board at that position
        :param pos: tuple in form ({row}, {column})
        :param n: value at the given position
        :return: a tuple containing the changed board and possible_actions_board
        """

        new_board = copy.copy(board)
        new_possible_actions_board = copy.copy(possible_actions_board)

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
        """
        Given a current board and possible actions board, we propagate the effect of assigning the value.
        We first propagate in the horizontal direction then the vertical direction and finally box-wise.

        :param board: numpy array of a n x n int board or grid in range [1..9]
        :param possible_actions_board: a 3D list such that for each possible_actions_board[{row}][{column}] we get a list of numbers we can input on the board at that position
        :param pos: tuple in form ({row}, {column})
        :param n: value at the given position
        :return: a tuple containing the propagated board and possible_actions_board
        """

        return self._propagate_horizontally(board, possible_actions_board, pos, n)

    def deal_with_1_picks(self, board: np.array, possible_actions_board: list):
        """
        Given a current board and possible actions board, check if any cells in the board only have one option for the cell assignment value.
        If only one possible value for that cell assign the value to that cell.

        :param board: numpy array of a n x n int board or grid in range [1..9]
        :param possible_actions_board: a 3D list such that for each possible_actions_board[{row}][{column}] we get a list of numbers we can input on the board at that position
        :return: a tuple containing the changed board and possible_actions_board
        """

        new_board = copy.copy(board)
        new_possible_actions_board = copy.copy(possible_actions_board)

        # Check entire board (i.e. all rows and columns)
        for row in range(len(new_board)):
            for column in range(len(new_board[0])):
                # If only one option for an unassigned cell
                if (new_board[row][column] == 0) and (len(new_possible_actions_board[row][column]) == 1):
                    # Get the option for that cell and empty the options for that cell
                    n = new_possible_actions_board[row][column][0]
                    new_possible_actions_board[row][column] = []
                    # If assigning the only remaining value is valid then perform the assignment and propagate the effect of the assignment
                    if self.is_valid_pos(new_board, (row, column), n):
                        new_board[row][column] = n
                        new_board, new_possible_actions_board = self.propagate(new_board, new_possible_actions_board, (row, column), n)

        return new_board, new_possible_actions_board
