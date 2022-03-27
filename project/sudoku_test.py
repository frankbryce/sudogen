from parameterized import parameterized
import sudoku
import unittest

class TestSudokuMethods(unittest.TestCase):

    def testRow(self):
        grid = sudoku.Grid.From([
            [1,2,0,4,5,6,7,8,9],
            [2,3,4,5,6,7,8,9,1],
            [3,4,5,6,7,8,9,1,2],
            [4,5,6,7,8,9,1,2,3],
            [5,6,7,8,9,1,2,3,4],
            [6,7,8,9,1,2,3,4,5],
            [7,8,9,1,2,3,4,5,6],
            [8,9,1,2,3,4,5,6,7],
            [9,1,2,3,4,5,6,7,8]])
        self.assertEqual(
            [cell.val for cell in grid.Row(2)],
            [3,4,5,6,7,8,9,1,2])
        self.assertEqual(
            [cell.row for cell in grid.Row(5)],
            [5,5,5,5,5,5,5,5,5])
        self.assertEqual(
            [cell.col for cell in grid.Row(0)],
            [0,1,2,3,4,5,6,7,8])

    def testCol(self):
        grid = sudoku.Grid.From([
            [1,2,3,4,5,6,7,8,9],
            [2,3,4,5,6,7,8,9,1],
            [0,4,5,6,7,8,9,1,2],
            [4,5,6,7,8,9,1,2,3],
            [5,6,7,8,9,1,2,3,4],
            [6,7,8,9,1,2,3,4,5],
            [7,8,9,1,2,3,4,5,6],
            [8,9,1,2,3,4,5,6,7],
            [9,1,2,3,4,5,6,7,8]])
        self.assertEqual(
            [cell.val for cell in grid.Col(2)],
            [3,4,5,6,7,8,9,1,2])
        self.assertEqual(
            [cell.col for cell in grid.Col(5)],
            [5,5,5,5,5,5,5,5,5])
        self.assertEqual(
            [cell.row for cell in grid.Col(0)],
            [0,1,2,3,4,5,6,7,8])

    def testBox(self):
        grid = sudoku.Grid.From([
            [1,2,3,4,5,6,7,8,9],
            [2,3,4,5,6,7,8,9,0],
            [3,4,5,6,7,8,9,1,2],
            [4,5,6,7,8,9,1,2,3],
            [5,6,7,8,9,1,2,3,4],
            [6,7,8,9,1,2,3,4,5],
            [7,8,9,1,2,3,4,5,6],
            [8,9,1,2,3,4,5,6,7],
            [9,1,2,3,4,5,6,7,8]])
        self.assertEqual(
            [cell.val for cell in grid.Box(2)],
            [7,8,9,8,9,0,9,1,2])
        self.assertEqual(
            [cell.col for cell in grid.Box(5)],
            [6,7,8,6,7,8,6,7,8])
        self.assertEqual(
            [cell.row for cell in grid.Box(0)],
            [0,0,0,1,1,1,2,2,2])

    @parameterized.expand([
        ['test01', True, [[1,2,3,4,5,6,7,8,9,],
                          [0,0,0,0,0,0,0,0,0,],
                          [0,0,0,0,0,0,0,0,0,],
                          [0,0,0,0,0,0,0,0,0,],
                          [0,0,0,0,0,0,0,0,0,],
                          [0,0,0,0,0,0,0,0,0,],
                          [0,0,0,0,0,0,0,0,0,],
                          [0,0,0,0,0,0,0,0,0,],
                          [0,0,0,0,0,0,0,0,0,],], 0, 0],
        ['test02', False, [[1,2,3,4,5,6,7,8,9,],
                           [0,0,0,0,0,0,0,0,0,],
                           [0,0,0,0,0,0,0,0,0,],
                           [0,0,0,0,0,0,0,0,0,],
                           [0,0,0,0,8,0,0,0,0,],
                           [0,0,0,0,0,0,0,0,0,],
                           [0,0,0,0,0,0,0,0,0,],
                           [0,0,0,0,0,0,0,0,0,],
                           [0,0,0,0,0,0,0,0,0,],], 4, 4],
    ])
    def testLogickable(self, name, exp, vals, r, c):
        grid = sudoku.Grid.From(vals)
        cell = grid.Cell(r, c)
        self.assertEqual(grid.Logickable(cell), exp)

if __name__ == '__main__':
    unittest.main()
