import numpy as np


def check(grid, row, col, num):
    for x in range(9):
        if grid[row][x] == num:
            return False
    for x in range(9):
        if grid[x][col] == num:
            return False
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if grid[i + start_row][j + start_col] == num:
                return False
    return True


def solve_sudoku(grid, row, col):
    n = 9
    if row == n - 1 and col == n:
        return True
    if col == n:
        row += 1
        col = 0
    if grid[row][col] > 0:
        return solve_sudoku(grid, row, col + 1)
    for num in range(1, n + 1, 1):
        if check(grid, row, col, num):
            grid[row][col] = num
            if solve_sudoku(grid, row, col + 1):
                return True
        grid[row][col] = 0
    return False


def main(grid):
    if solve_sudoku(grid, 0, 0):
        return np.array(grid)
    else:
        return False
