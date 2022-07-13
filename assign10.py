"""
Hasana Parker, Joe Cookson
CS51A: Assignment 10
April 11th, 2022
                                                       Sudoku
"""

import copy
import time

# ________________________________________________
# Experiments response
""""
Experiment 1:

The get_most_constrained function was more efficient than the get_any_available_cell for all test problems.
For problem 1, get_most_constrained took 0.25 compared to get_any_available_cell's time of 0.71 secs.
For Problem 2, get_most_constrained took 0.25 sec compared to get_any_available_cell's time of  8.08 secs.
For heart problem, get_most_constrained took 10.37 secs compared to  get_any_available_cell's time 79.76 secs.

get_any_available_cell is less efficient than get_most_constrained as get_any_available_cell is not making use of 
informed search. It's just performing depth first search on the first entry it comes across instead of finding the most
constrained one, which is the best method for solving sudoku.

get_most_constrained is just a linear scan through the function, a loop through to find the shortest possible value 
list but since it is working to find the most_constrained_cell it is more efficient at solving the game as it has a 
strategy.
 

Experiment 2:

Propagate made the function super efficient taking almost no time to complete. Problem one took 0.0 secs, problem 2 took 
0.06 second, and heart took 3.35 seconds. Propagate made the function the most efficient out of just having best first 
search or depth first search.

Propagate is a depth first search as well but it only goes deep on a promising path, instead of iterating through all 
the possible options.Propagate is a more efficient depth first search than get available cell as it is informed, and has
the heuristics which checks if the entry it is on is constrained.
"""


class SudokuState:
    """
    SudokuState Class
    """
    def __init__(self):
        """
        Constructor Function
        """
        self.size = 9  # the board is 9 x 9
        self.num_placed = 0  # start at zero because no numbers placed yet
        self.board = []

        for i in range(self.size):
            row = []  # this makes the list inside the list that is self.board, making a row list for the size of the
            # board
            for j in range(self.size):
                row.append(SudokuEntry())  # append SudokuEntry nine times in this list, making one row of the matrix
            self.board.append(row)  # append all nine rows to the main list

    def remove_conflict(self, row, col, num):
        """
        This function is called when a number has been placed in the same row, column, or subgrid as the num parameter
        and will remove that number as a possibility.

        :param row: (int) row in the matrix
        :param col: (int) Column in the matrix
        :param num: (int) A number from 1-9
        :return: none
        """
        self.board[row][col].eliminate(num)  # calls the eliminate method from SudokuEntry Class, which
        # removes the num from the possible set of valid values that could be placed at this entry.

    def remove_all_conflicts(self, row, col, num):
        """
        Updates all the unfixed/ unfilled entries that are in the same row, col, subgrid as the number that has just
        been fixed, so that the number is no longer an option for those entries.

        :param row: (int) row in the matrix
        :param col: (int) col in the matrix
        :param num: (int) number that is being fixed
        :return: none
        """
        current_subgrid = self.get_subgrid_number(row, col)
        for r in range(self.size):
            for c in range(len(self.board[r])):
                if not (r == row and c == col):
                    if r == row or c == col or self.get_subgrid_number(r, c) == current_subgrid:
                        self.remove_conflict(r, c, num)

    def add_number(self, row, col, num):
        """
        This functions adds/fixes a number onto the board, and updates the count of the numbers placed. After a number
        is fixed all conflicts in the same row, col, and subgrid are then removed.

        :param row: (int) row of the board
        :param col: (int) col of the board
        :param num: (int) number
        :return: none
        """
        self.board[row][col].fix(num)
        self.num_placed += 1  # increasing the count
        self.remove_all_conflicts(row, col, num)

    def get_most_constrained_cell(self):
        """
        This function returns the column and row of the most constrained entry on the board, one that is yet to be fixed
        and has the fewest possible options remaining to be filled with.

        :return: (tup) a tuple with the col and row of the most constrained entry
        """
        least_entry_candidates = self.size + 1  # starting the width of the board at 10
        constrained_cell = None  # initializing the tuple

        for r in range(self.size):
            for c in range(len(self.board[r])):  # iterating over the entirety of the board, each row and col

                # width tells you how-many candidates there are for an entry, and if the number of candidates is less
                # than the initialized entry candidates make that the new number of candidates keep looking for the
                # row/ col with the least amount of candidates

                if not self.board[r][c].is_fixed() and self.board[r][c].width() < least_entry_candidates:
                    least_entry_candidates = self.board[r][c].width()
                    constrained_cell = (r, c)

        return constrained_cell

    def solution_is_possible(self):
        """
        This function returns true if all entries on the board have at least one possible value they can take.

        :return:(bol)
        """
        for r in range(self.size):
            for c in range(len(self.board[r])):
                if self.board[r][c].has_conflict():
                    return False
        return True

    def next_states(self):
        """
        This function creates a list of next states that can be reached from the current state by placing a number in
        the most constrained cell.

        :return: (list) viable states list, where the solution is still possible
        """
        solution_states = []
        (row, col) = self.get_any_available_cell()  # returns a tuple (row, col)

        for value in self.board[row][col].values():
            new_board_states = copy.deepcopy(self)  # making a copy of the current board
            new_board_states.add_number(row, col, value)  # adding a number onto the new board, a new number is added
            # and new board is created each time through the loop

            if new_board_states.solution_is_possible():  # checking is the board is a possible solution
                solution_states.append(new_board_states)

        return solution_states

    def is_goal(self):
        """
        This function checks to see if a state is a goal state or not

        :return: (bol)
        """
        return self.num_placed == self.size * self.size

    def get_subgrid_number(self, row, col):
        """
        Returns a number between 1 and 9 representing the subgrid
        that this row, col is in.  The top left subgrid is 1, then
        2 to the right, then 3 in the upper right, etc.
        """
        row_q = int(row / 3)
        col_q = int(col / 3)
        return row_q * 3 + col_q + 1

    def get_any_available_cell(self):
        """
        An uninformed cell finding variant.  If you use
        this instead of find_most_constrained_cell
        the search will perform a depth first search.
        """
        for r in range(self.size):
            for c in range(self.size):
                if not self.board[r][c].is_fixed():
                    return (r, c)
        return None

    def propagate(self):
        for ri in range(self.size):
            for ci in range(self.size):
                if not self.board[ri][ci].is_fixed() and \
                   self.board[ri][ci].width() == 1:
                    self.add_number(ri, ci, self.board[ri][ci].values()[0])
                    if self.solution_is_possible():
                        self.propagate()
                        return

    def get_raw_string(self):
        board_str = ""

        for r in self.board:
            board_str += str(r) + "\n"

        return "num placed: " + str(self.num_placed) + "\n" + board_str

    def __str__(self):
        """
        prints all numbers assigned to cells.  Unassigned cells (i.e.
        those with a list of options remaining are printed as blanks
        """
        board_string = ""

        for r in range(self.size):
            if r % 3 == 0:
                board_string += " " + "-" * (self.size * 2 + 5) + "\n"

            for c in range(self.size):
                entry = self.board[r][c]

                if c % 3 == 0:
                    board_string += "| "

                board_string += str(entry) + " "

            board_string += "|\n"

        board_string += " " + "-" * (self.size * 2 + 5) + "\n"

        return "num placed: " + str(self.num_placed) + "\n" + board_string


# -----------------------------------------------------------------------
# Make all of your changes to the SudokuState class above.
# only when you're running the last experiments will
# you need to change anything below here and then only
# the different problem inputs

class SudokuEntry:
    def __init__(self):
        self.fixed = False
        self.domain = list(range(1, 10))

    def is_fixed(self):
        """
        Returns true if a number has been placed in this entry or False if it's still open.
        :return:
        """
        return self.fixed

    def width(self):
        """
        Tells you how many candidates there are
        :return:
        """
        return len(self.domain)

    def values(self):
        """
        Returns a list of the numbers that are still available to be placed in this entry.
        :return:
        """
        return self.domain

    def has_conflict(self):
        """
        Check whether there is a conflict cell.
        :return:
        """
        return len(self.domain) == 0

    def __str__(self):
        if self.fixed:
            return str(self.domain[0])
        return "_"

    def __repr__(self):
        if self.fixed:
            return str(self.domain[0])
        return str(self.domain)

    def fix(self, n):
        """
        Puts the number n at this entry
        :param n:
        :return:
        """
        assert n in self.domain
        self.domain = [n]
        self.fixed = True

    def eliminate(self, n):
        """
        Remove n from the possible set of valid values that could be placed at this entry.
        :param n:
        :return:
        """
        if n in self.domain:
            assert not self.fixed
            self.domain.remove(n)

# -----------------------------------
# Even though this is the same DFS code
# that we used last time, our next_states
# function is making an "informed" decision
# so this algorithm performs similarly to
# the best first search.


def dfs(state):
    """
    Recursive depth first search implementation

    Input:
    Takes as input a state.  The state class MUST have the following
    methods implemented:
    - is_goal(): returns True if the state is a goal state, False otherwise
    - next_states(): returns a list of the VALID states that can be
    reached from the current state

    Output:
    Returns a list of ALL states that are solutions (i.e. is_goal
    returned True) that can be reached from the input state.
    """
    # if the current state is a goal state, then return it in a list
    if state.is_goal():
        return [state]
    else:
        # make a list to accumulate the solutions in
        result = []

        for s in state.next_states():
            result += dfs(s)

        return result

# ------------------------------------
# three different board configurations:
# - problem1
# - problem2
# - heart (example from class notes)


def problem1():
    b = SudokuState()
    b.add_number(0, 1, 7)
    b.add_number(0, 7, 1)
    b.add_number(1, 2, 9)
    b.add_number(1, 3, 7)
    b.add_number(1, 5, 4)
    b.add_number(1, 6, 2)
    b.add_number(2, 2, 8)
    b.add_number(2, 3, 9)
    b.add_number(2, 6, 3)
    b.add_number(3, 1, 4)
    b.add_number(3, 2, 3)
    b.add_number(3, 4, 6)
    b.add_number(4, 1, 9)
    b.add_number(4, 3, 1)
    b.add_number(4, 5, 8)
    b.add_number(4, 7, 7)
    b.add_number(5, 4, 2)
    b.add_number(5, 6, 1)
    b.add_number(5, 7, 5)
    b.add_number(6, 2, 4)
    b.add_number(6, 5, 5)
    b.add_number(6, 6, 7)
    b.add_number(7, 2, 7)
    b.add_number(7, 3, 4)
    b.add_number(7, 5, 1)
    b.add_number(7, 6, 9)
    b.add_number(8, 1, 3)
    b.add_number(8, 7, 8)
    return b


def problem2():
    b = SudokuState()
    b.add_number(0, 1, 2)
    b.add_number(0, 3, 3)
    b.add_number(0, 5, 5)
    b.add_number(0, 7, 4)
    b.add_number(1, 6, 9)
    b.add_number(2, 1, 7)
    b.add_number(2, 4, 4)
    b.add_number(2, 7, 8)
    b.add_number(3, 0, 1)
    b.add_number(3, 2, 7)
    b.add_number(3, 5, 9)
    b.add_number(3, 8, 2)
    b.add_number(4, 1, 9)
    b.add_number(4, 4, 3)
    b.add_number(4, 7, 6)
    b.add_number(5, 0, 6)
    b.add_number(5, 3, 7)
    b.add_number(5, 6, 5)
    b.add_number(5, 8, 8)
    b.add_number(6, 1, 1)
    b.add_number(6, 4, 9)
    b.add_number(6, 7, 2)
    b.add_number(7, 2, 6)
    b.add_number(8, 1, 4)
    b.add_number(8, 3, 8)
    b.add_number(8, 5, 7)
    b.add_number(8, 7, 5)
    return b


def heart():
    b = SudokuState()
    b.add_number(1, 1, 4)
    b.add_number(1, 2, 3)
    b.add_number(1, 6, 6)
    b.add_number(1, 7, 7)
    b.add_number(2, 0, 5)
    b.add_number(2, 3, 4)
    b.add_number(2, 5, 2)
    b.add_number(2, 8, 8)
    b.add_number(3, 0, 8)
    b.add_number(3, 4, 6)
    b.add_number(3, 8, 1)
    b.add_number(4, 0, 2)
    b.add_number(4, 8, 5)
    b.add_number(5, 1, 5)
    b.add_number(5, 7, 4)
    b.add_number(6, 2, 6)
    b.add_number(6, 6, 7)
    b.add_number(7, 3, 5)
    b.add_number(7, 5, 1)
    b.add_number(8, 4, 8)
    return b


# --------------------------------
# Code that actual runs a sudoku problem, times it
# and prints out the solution.
# You can vary which problem you're running on between
# problem1(), problem2() and heart() by changing the line
# below
#
# Uncomment this code when you have everything implemented, and you
# want to solve some sample problems!

problem = problem1()
print("Starting board:")
print(problem)

start_time = time.time()
solutions = dfs(problem)
search_time = time.time()-start_time

print("Search took " + str(round(search_time, 2)) + " seconds")
print("There was " + str(len(solutions)) + " solution.\n\n")
if len(solutions) > 0:
    print(solutions[0])
