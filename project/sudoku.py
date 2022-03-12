#!/usr/bin/python3

from __future__ import annotations

from pprint import pprint
import random

nums = [x+1 for x in range(9)]

class Cell:

    grid: Grid  # grid this cell is in
    row: int  # 0-indexed
    col: int  # 0-indexed
    val: int = 0  # 0 indicates cell is empty. valid values are 1-9

    def __init__(self, grid, row, col):
        self.grid = grid
        self.row = row
        self.col = col

    def Box(self) -> list(int):
        rst = (self.row//3)*3
        cst = (self.col//3)*3
        return [self.grid.cells[rst+r][cst+c].val for r in range(3) for c in range(3)]

    def Row(self) -> list(int):
        return [self.grid.cells[self.row][i].val for i in range(9)]

    def Col(self) -> list(int):
        return [self.grid.cells[i][self.col].val for i in range(9)]

class Grid:

    cells: list[list[Cell]]
    
    def __init__(self) -> Grid:
        self.cells = [[Cell(grid=self, row=row, col=col) for col in range(9)] for row in range(9)]

    @staticmethod
    def Full() -> Grid:
        ret = Grid()
        while not ret._valid():
            ret = Grid()
            for row in ret.cells:
                for cell in row:
                    random.shuffle(nums)
                    for num in nums:
                        if (num not in cell.Box() and
                            num not in cell.Row() and
                            num not in cell.Col()):
                            cell.val = num
                            break
        return ret

    @staticmethod
    def New(difficulty) -> Grid:
        ret = Full()
        ret._fill()
        # difficulty = 5  # 5 tries before successfully putting in a square
        # while success:
        #   permute all valued cells
        #   success = False
        #   for all cells in the permutation
        #     remove cell
        #     tot_tries = 0
        #     nsims = 1000
        #     isim = 0
        #     while isim<nsims and tot_tries <= nsims*difficulty:
        #       tries = 0
        #       until a cell is added, max 2*diff tries
        #         tries += 1
        #         pick random strategy
        #         if strategy adds a value to cell
        #           tot_tries += tries
        #           break
        #     if tot_tries <= nsims*difficulty:
        #       success = True
        #     else:
        #       add cell back to grid
        return ret
        
    def Print(self):
        for r in self.cells:
            for c in r:
                print(c.val, end=' ')
            print()

    # check that sudoku is completed and valid
    def _valid(self) -> bool:
        for row in self.cells:
            for cell in row:
                chk = set()
                _box = cell.Box()
                _row = cell.Row()
                _col = cell.Col()
                if len(_box) != 9:
                    return False
                if len(_row) != 9:
                    return False
                if len(_col) != 9:
                    return False
                for chkList in [_box, _row, _col]:
                    chk = set()
                    for v in chkList:
                        if v == 0:
                            return False
                        chk.add(v)
                    if len(chk) != 9:
                        return False
        return True


