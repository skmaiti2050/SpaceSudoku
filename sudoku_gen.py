import copy
import time
import random
import numpy as np


class cell:

    def __init__(self, pos):
        self.pos = pos
        self.possible_ans = list(range(1, 10))
        self.ans = None
        self.solved = False

    def set_ans(self, num):
        if num in list(range(0, 10)):
            self.possible_ans = [num]
            self.ans = num
            self.solved = True

    def remove(self, num):
        if num in self.possible_ans and self.solved is False:
            self.possible_ans.remove(num)
            if len(self.possible_ans) == 1:
                self.ans = self.possible_ans[0]
                self.solved = True
        elif num in self.possible_ans and self.solved is True:
            self.ans = 0

    def reset(self):
        self.possible_ans = list(range(1, 10))
        self.ans = None
        self.solved = False

    def ret_pos(self):
        return self.pos

    def ret_possible_ans(self):
        return self.possible_ans

    def len_possible_ans(self):
        return len(self.possible_ans)

    def cell_solved(self):
        return self.solved

    def ret_solved(self):
        if self.solved is True:
            return self.possible_ans[0]
        else:
            return '0'


def empty_sudoku():
    ans = []
    for x in range(1, 10):
        if x in range(7, 10):
            temp_z = 7
            z = 7
        elif x in list(range(4, 7)):
            temp_z = 4
            z = 4
        elif x in list(range(1, 4)):
            temp_z = 1
            z = 1
        for y in list(range(1, 10)):
            z = temp_z
            if y in list(range(7, 10)):
                z += 2
            elif y in list(range(4, 7)):
                z += 1
            elif y in list(range(1, 4)):
                z += 0
            c = cell((x, y, z))
            ans.append(c)
    return ans


def display_sudoku(s):
    (row1, row2, row3) = ([], [], [])
    (row4, row5, row6) = ([], [], [])
    (row7, row8, row9) = ([], [], [])
    for i in range(81):
        if i in range(0, 9):
            row1.append(s[i].ret_solved())
        if i in range(9, 18):
            row2.append(s[i].ret_solved())
        if i in range(18, 27):
            row3.append(s[i].ret_solved())
        if i in range(27, 36):
            row4.append(s[i].ret_solved())
        if i in range(36, 45):
            row5.append(s[i].ret_solved())
        if i in range(45, 54):
            row6.append(s[i].ret_solved())
        if i in range(54, 63):
            row7.append(s[i].ret_solved())
        if i in range(63, 72):
            row8.append(s[i].ret_solved())
        if i in range(72, 81):
            row9.append(s[i].ret_solved())
    return np.array([row1, row2, row3, row4, row5, row6, row7, row8, row9])


def gen_sudoku():
    cells = [i for i in range(81)]
    s = empty_sudoku()
    while len(cells) != 0:
        (lowest_num, lowest) = ([], [])
        for i in cells:
            lowest_num.append(s[i].len_possible_ans())
        m = min(lowest_num)
        for i in cells:
            if s[i].len_possible_ans() == m:
                lowest.append(s[i])
        c_element = random.choice(lowest)
        c_index = s.index(c_element)
        cells.remove(c_index)
        pos1 = c_element.ret_pos()
        if c_element.cell_solved() is False:
            p_val = c_element.ret_possible_ans()
            f_val = random.choice(p_val)
            c_element.set_ans(f_val)
            for i in cells:
                pos2 = s[i].ret_pos()
                if pos1[0] == pos2[0]:
                    s[i].remove(f_val)
                elif pos1[1] == pos2[1]:
                    s[i].remove(f_val)
                elif pos1[2] == pos2[2]:
                    s[i].remove(f_val)
        else:
            f_val = c_element.ret_solved()
            for i in cells:
                pos2 = s[i].ret_pos()
                if pos1[0] == pos2[0]:
                    s[i].remove(f_val)
                elif pos1[1] == pos2[1]:
                    s[i].remove(f_val)
                elif pos1[2] == pos2[2]:
                    s[i].remove(f_val)
    return s


def check_sudoku(s):
    for i in range(len(s)):
        for n in range(len(s)):
            if i != n:
                pos1 = s[i].ret_pos()
                pos2 = s[n].ret_pos()
                if pos1[0] == pos2[0] or pos1[1] == pos2[1] or pos1[2] \
                        == pos2[2]:
                    n1 = s[i].ret_solved()
                    n2 = s[n].ret_solved()
                    if n1 == n2:
                        return False
    return True


def comp_sudoku():
    result = False
    while result is False:
        s = gen_sudoku()
        result = check_sudoku(s)
    return s


def solver(s, f=0):
    if f > 900:
        return False
    guesses = 0
    s_copy = copy.deepcopy(s)
    cells = [i for i in range(81)]
    s_cells = []
    for i in cells:
        if s_copy[i].len_possible_ans() == 1:
            s_cells.append(i)
    while s_cells != []:
        for n in s_cells:
            cell = s_copy[n]
            pos1 = cell.ret_pos()
            f_val = s_copy[n].ret_solved()
            for i in cells:
                pos2 = s_copy[i].ret_pos()
                if pos1[0] == pos2[0]:
                    s_copy[i].remove(f_val)
                if pos1[1] == pos2[1]:
                    s_copy[i].remove(f_val)
                if pos1[2] == pos2[2]:
                    s_copy[i].remove(f_val)
                if s_copy[i].len_possible_ans() == 1 and i \
                        not in s_cells and i in cells:
                    s_cells.append(i)
            s_cells.remove(n)
            cells.remove(n)
        if cells != [] and s_cells == []:
            (lowest_num, lowest) = ([], [])
            for i in cells:
                lowest_num.append(s_copy[i].len_possible_ans())
            m = min(lowest_num)
            for i in cells:
                if s_copy[i].len_possible_ans() == m:
                    lowest.append(s_copy[i])
            r_choice = random.choice(lowest)
            r_cell = s_copy.index(r_choice)
            r_guess = random.choice(s_copy[r_cell].ret_possible_ans())
            s_copy[r_cell].set_ans(r_guess)
            s_cells.append(r_cell)
            guesses += 1
    if check_sudoku(s_copy):
        if guesses == 0:
            level = 'Easy'
        elif guesses <= 2:
            level = 'Medium'
        elif guesses <= 7:
            level = 'Hard'
        return (s_copy, guesses, level)
    else:
        return solver(s, f + 1)


def solve(s, n=0):
    if n < 30:
        s = solver(s)
        if s is not False:
            return s
        else:
            solve(s, n + 1)
    else:
        return False


def gen_puzzle(s):
    cells = [i for i in range(81)]
    while cells != []:
        s_copy = copy.deepcopy(s)
        r_index = random.choice(cells)
        cells.remove(r_index)
        s_copy[r_index].reset()
        ss = solve(s_copy)
        if ss[0] is False:
            f = solve(s)
            return display_sudoku(s)
        elif check_puzzle(ss[0], solve(s_copy)[0]):
            if check_puzzle(ss[0], solve(s_copy)[0]):
                s[r_index].reset()
        else:
            f = solve(s)
            return (s, f[1], f[2])


def check_puzzle(s1, s2):
    for i in range(len(s1)):
        if s1[i].ret_solved() != s2[i].ret_solved():
            return False
    return True


def main(level):
    t1 = time.time()
    n = 0
    if level == 'Easy':
        p = comp_sudoku()
        s = gen_puzzle(p)
        if s[2] != 'Easy':
            return main(level)
        t2 = time.time()
        t3 = t2 - t1
        return display_sudoku(s[0])
    elif level == 'Medium':
        p = comp_sudoku()
        s = gen_puzzle(p)
        while s[2] == 'Easy':
            n += 1
            s = gen_puzzle(p)
            if n > 50:
                return main(level)
        if s[2] != 'Medium':
            return main(level)
        t2 = time.time()
        t3 = t2 - t1
        return display_sudoku(s[0])
    elif level == 'Hard':
        p = comp_sudoku()
        s = gen_puzzle(p)
        while s[2] == 'Easy':
            n += 1
            s = gen_puzzle(p)
            if n > 50:
                return main(level)
        while s[2] == 'Medium':
            n += 1
            s = gen_puzzle(p)
            if n > 50:
                return main(level)
        if s[2] != 'Hard':
            return main(level)
        t2 = time.time()
        t3 = t2 - t1
        return display_sudoku(s[0])
    else:
        raise ValueError
