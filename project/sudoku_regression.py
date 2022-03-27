import numpy as np
import sudoku

N = 10

def main():
    for difficulty in np.logspace(0, 0.5, num=20):
        tot = 0
        for _ in range(N):
            tot += sudoku.Grid.New(difficulty, nsims=100).Count()
        print(f'Difficulty {difficulty} average: {tot/N}')

if __name__ == "__main__":
    main()
