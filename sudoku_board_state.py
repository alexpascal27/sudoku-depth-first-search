import numpy as np
from typing import Tuple, List
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

    def get_possible_actions_board(self):
        return self.possible_actions_board

    def get_current_pos(self):
        return self.current_pos

    def get_board(self):
        return self.board

    def get_parent(self):
        return self.parent

    def pop_from_possible_actions_board(self):
        if self.action is None:
            return
        pos, n = self.action
        self.possible_actions_board[pos[0]][pos[1]].pop()

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
        new_possible_actions_board[row][column].pop()

        # Propagate the effect of the assignment
        new_board, new_possible_actions_board = self._propagate(new_board, new_possible_actions_board, (row, column), n)
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
        return not self._in_box(board, pos, n) and not self._in_horizontal(board, pos, n) and not self._in_vertical(
            board, pos, n)

    def _deal_with_1_possible_action(self, board: np.array, possible_actions_board: list, pos: Tuple[int, int]) -> Tuple[np.array, list]:
        new_board = copy.deepcopy(board)
        new_possible_actions_board = copy.deepcopy(possible_actions_board)

        r, c = pos
        only_remaining_option = new_possible_actions_board[r][c][0]

        # If the 1 possible action is on already assigned cell, dont assign it
        if new_board[r][c] != 0:
            return new_board, new_possible_actions_board

        # If the only remaining option is valid, then pick it, otherwise return an unchanged board and empty possible action board
        if self._is_valid_pos(new_board, pos, only_remaining_option):
            new_board[r][c] = only_remaining_option
            new_possible_actions_board[r][c] = []
            # Propagate the effect of the assignment
            return self._propagate(new_board, new_possible_actions_board, (r, c), only_remaining_option)
        # Position is not valid
        else:
            return new_board, new_possible_actions_board

    def _propagate_horizontally(self, board: np.array, possible_actions_board: list, pos: Tuple[int, int], n: int) -> \
    Tuple[np.array, list]:
        new_board = copy.deepcopy(board)
        new_possible_actions_board = copy.deepcopy(possible_actions_board)
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
                    new_board, new_possible_actions_board = self._deal_with_1_possible_action(new_board,
                                                                                              new_possible_actions_board,
                                                                                              (r, i))

            # If couldn't find n we dont need to do anything
            except ValueError:
                pass

            except IndexError:
                pass

        return new_board, new_possible_actions_board

    def _propagate_vertically(self, board: np.array, possible_actions_board: list, pos: Tuple[int, int], n: int) -> \
    Tuple[np.array, list]:
        new_board = copy.deepcopy(board)
        new_possible_actions_board = copy.deepcopy(possible_actions_board)

        # Get the row and column of the position
        r, c = pos
        indexes_to_check = [*range(9)]
        indexes_to_check.pop(r)
        for i in indexes_to_check:
            try:
                # If we find n in the array of possible actions, remove it
                index_of_n = new_possible_actions_board[i][c].index(n)
                #print("Index of " + str(n) + " at position[" + str(pos[0]) + "][" + str(pos[1]) + "]: " + str(index_of_n))
                new_possible_actions_board[i][c].pop(index_of_n)
                # If we only have an option for an action, pick that action
                if len(new_possible_actions_board[i][c]) == 1:
                    new_board, new_possible_actions_board = self._deal_with_1_possible_action(new_board,
                                                                                              new_possible_actions_board,
                                                                                              (i, c))

            # If couldn't find n we dont need to do anything
            except ValueError:
                pass

            except IndexError:
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
        new_board = copy.deepcopy(board)
        new_possible_actions_board = copy.deepcopy(possible_actions_board)

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
                        new_board, possible_actions_board = self._deal_with_1_possible_action(new_board,
                                                                                              new_possible_actions_board,
                                                                                              (row, column))

                    break

                # If couldn't find n we dont need to do anything
                except ValueError:
                    pass

                except IndexError:
                    pass
        return new_board, new_possible_actions_board

    def _propagate(self, board: np.array, possible_actions_board: list, pos: Tuple[int, int], n: int) -> Tuple[np.array, list]:
        # print("Propagate")
        # self.print_2d_list(possible_actions_board)
        new_board, new_possible_actions_board = self._propagate_horizontally(board, possible_actions_board, pos, n)
        new_board, new_possible_actions_board = self._propagate_vertically(new_board, new_possible_actions_board, pos, n)
        new_board, new_possible_actions_board = self._propagate_box_wise(new_board, new_possible_actions_board, pos, n)
        return new_board, new_possible_actions_board
