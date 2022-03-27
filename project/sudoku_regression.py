import numpy as np
import sudoku
from tqdm import tqdm

N = 1000
CNT = 30
TYPE = 'FILTER_GEN'

def main():
    if TYPE == 'DIFF':
        for difficulty in np.logspace(0, 0.5, num=20):
            tot = 0
            for _ in range(N):
                tot += sudoku.Grid.New(difficulty, nsims=100).Count()
            print(f'Difficulty {difficulty} average: {tot/N}')
    elif TYPE == 'FILTER_GEN':
        for _ in tqdm(range(N)):
            grid = sudoku.Grid.New(-1)
            cnt = grid.Count()
            if cnt <= CNT:
                print(f'count: {cnt}')
                grid.Print()

if __name__ == "__main__":
    main()
