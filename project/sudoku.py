#!/usr/bin/python3

from __future__ import annotations

from pprint import pprint
import random

nums = [x+1 for x in range(9)]

class Cell:

    grid: Grid  # grid this cell is in
    row: int  # 0-indexed
    col: int  # 0-indexed
    box: int  # 0-indexed
    val: int  # 0 indicates cell is empty. valid values are 1-9

    def __init__(self, grid, row, col, val=0):
        self.grid = grid
        self.row = row
        self.col = col
        self.box = 3*(row//3) + (col//3)
        self.val = val

    def Box(self) -> list[int]:
        rst = (self.row//3)*3
        cst = (self.col//3)*3
        return [self.grid.cells[rst+r][cst+c].val for r in range(3) for c in range(3)]

    def Row(self) -> list[int]:
        return [self.grid.cells[self.row][i].val for i in range(9)]

    def Col(self) -> list[int]:
        return [self.grid.cells[i][self.col].val for i in range(9)]

class Grid:

    cells: list[list[Cell]]
    
    def __init__(self) -> Grid:
        self.cells = [[Cell(grid=self, row=row, col=col) for col in range(9)] for row in range(9)]

    def Row(self: Grid, row: int) -> list[int]:
        return [self.cells[row][i] for i in range(9)]

    def Col(self: Grid, col: int) -> list[int]:
        return [self.cells[i][col] for i in range(9)]

    def Box(self: Grid, box: int) -> list[int]:
        rst = (box//3)*3
        cst = (box%3)*3
        return [self.cells[rst+r][cst+c] for r in range(3) for c in range(3)]

    def Cell(self: Grid, row: int, col: int) -> Cell:
        return self.cells[row][col]

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
        ret.solution = [[ret.cells[r][c].val for c in range(9)] for r in range(9)]
        return ret

    @staticmethod
    def From(ints: list[list[int]]) -> Grid:
        ret = Grid()
        ret.cells = [
            [Cell(grid=ret, row=row, col=col, val=ints[row][col]) for col in range(9)]
            for row in range(9)
        ]
        return ret

    def Count(self: Grid) -> int:
        cnt = 0
        for row in self.cells:
            for cell in row:
                if cell.val != 0:
                    cnt += 1
        return cnt

    def Logickable(self: Grid, cell: Cell) -> bool:
        if cell.val == 0:
            print("Houston, you've called a problem")
            return False

        # only place for num in Row, Col or Box?
        for loc in [self.Row(cell.row), self.Col(cell.col), self.Box(cell.box)]:
            found = False
            for _cell in loc:
                if _cell.row == cell.row and _cell.col == cell.col:
                    continue
                if _cell.val != 0:
                    continue
                can_be_here = True
                for _other_cell in (self.Row(_cell.row)+self.Col(_cell.col)+self.Box(_cell.box)):
                    if _other_cell.row == cell.row and _other_cell.col == cell.col:
                        continue
                    if _other_cell.val == cell.val:
                        can_be_here = False
                        break
                if can_be_here:
                    found = True
                    break
            if not found:
                return True

        # only num for Cell?
        sees = set()
        for _cell in (self.Row(cell.row)+self.Col(cell.col)+self.Box(cell.box)):
            if _cell.row == cell.row and _cell.col == cell.col:
                continue
            sees.add(_cell.val)
        sees.discard(0)
        if cell.val in sees:
            print(f"We have a problem, Houston")
        if len(sees) == 8:
            return True

        return False


    @staticmethod
    def New(difficulty: int, nsims: int=10) -> Grid:
        ret = Grid.Full()
        success = True
        rclist = [(r,c) for r in range(9) for c in range(9)]
        while success:
            success = True

            random.shuffle(rclist)
            for rc in list(rclist):
                cell = ret.cells[rc[0]][rc[1]]
                if cell.row != rc[0] or cell.col != rc[1]:
                    print("Houston, we have a problem")

                if cell.val == 0:
                    continue

                # check that this location can be logicked back in
                if not ret.Logickable(cell):
                    success = False
                    continue

                cell.val = 0
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


