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
        self.box = (row//3) + 3*(col//3)
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

    def Row(self, row) -> list[int]:
        return [self.cells[row][i] for i in range(9)]

    def Col(self, col) -> list[int]:
        return [self.cells[i][col] for i in range(9)]

    def Box(self, box) -> list[int]:
        rst = (box//3)*3
        cst = (box%3)*3
        return [self.cells[rst+r][cst+c] for r in range(3) for c in range(3)]

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
        ret.solved = [[ret.cells[r][c].val for c in range(9)] for r in range(9)]
        return ret

    def From(ints: list[list[int]]) -> Grid:
        ret = Grid()
        ret.cells = [
            [Cell(grid=ret, row=row, col=col, val=ints[row][col]) for col in range(9)]
            for row in range(9)
        ]
        return ret

    @staticmethod
    def New(difficulty: int, nsims: int=10) -> Grid:
        ret = Grid.Full()
        success = True
        rclist = [(r,c) for r in range(9) for c in range(9)]
        while success:
            success = False
            random.shuffle(rclist)
            for rc in list(rclist):
                cell = ret.cells[rc[0]][rc[1]]
                if cell.row != rc[0] or cell.col != rc[1]:
                    print("Houston, we have a problem")
                if cell.val == 0:
                    continue

                # check that this location can be logicked back in
                logickable = False
                # only place for num in Row, Col or Box?
                for loc in [ret.Row(cell.row), ret.Col(cell.col), ret.Box(cell.box)]:
                    found = False
                    for _cell in loc:
                        if _cell is cell:
                            continue
                        can_be_here = True
                        for _other_cell in (ret.Row(_cell.row)+ret.Col(_cell.col)+ret.Box(_cell.box)):
                            if _other_cell is _cell:
                                continue
                            if _other_cell.val == cell.val:
                                can_be_here = False
                                break
                        if can_be_here:
                            found = True
                            break
                    if not found:
                        logickable = True
                        break

                # only num for Cell?
                if not logickable: # yet
                    sees = set()
                    for _cell in (ret.Row(cell.row)+ret.Col(cell.col)+ret.Box(cell.box)):
                        if _cell is cell:
                            continue
                        sees.add(_cell.val)
                    sees.discard(0)
                    if cell.val in sees:
                        print("We have a problem, Houston")
                    if len(sees) == 8:
                        logickable = True

                # we are removing a cell we can't logic back
                if not logickable:
                    continue

                orig_val = cell.val
                cell.val = 0
                tot_tries = 0
                isim = 0
                while isim<nsims and tot_tries <= nsims*difficulty:
                    isim += 1
                    tries = 0
                    cell_added = False
                    while not cell_added and tries<2*difficulty:
                        tries += 1
                        tot_tries += 1
                        if random.choice([1,2]) == 1:
                            good_choice = False
                            while not good_choice:
                                idx = random.choice(list(range(9)))
                                loc = random.choice([ret.Row, ret.Col, ret.Box])
                                for _cell in loc(idx):
                                    if _cell.val == 0:
                                        good_choice = True
                                        break
                            for _cell in loc(idx):
                                if _cell.val == 0:
                                    vals = set(nums)
                                    for v in _cell.Row():
                                        vals.discard(v)
                                    for v in _cell.Col():
                                        vals.discard(v)
                                    for v in _cell.Box():
                                        vals.discard(v)
                                    if len(vals) == 1:
                                        cell_added = True
                                        break
                        else:
                            good_choice = False
                            while not good_choice:
                                rc = random.choice(rclist)
                                num = ret.cells[rc[0]][rc[1]].val
                                if num == 0:
                                    continue
                                loc = random.choice([ret.Row, ret.Col, ret.Box])
                                idx = random.choice(list(range(9)))
                                good_choice = True
                                for _cell in loc(idx):
                                    if _cell.val == num:
                                        good_choice = False
                                        break
                            num_pos = 0
                            for _cell in loc(idx):
                                if _cell.val != 0:
                                    continue
                                if _cell.val == num:
                                    print("Houston, we have a problem")
                                if (num not in _cell.Row() and
                                    num not in _cell.Col() and
                                    num not in _cell.Box()):
                                    num_pos += 1
                            cell_added = (num_pos == 1)
                if tot_tries <= nsims*difficulty:
                    success = True
                    break
                else:
                    print("added value back")
                    cell.val = orig_val
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


