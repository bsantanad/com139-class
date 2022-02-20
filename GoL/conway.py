#! /usr/bin/env python3
"""
conway.py
A simple Python/matplotlib implementation of Conway's Game of Life.
"""

import sys, argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

ON = 255
OFF = 0
vals = [ON, OFF]

def randomGrid(N):
    """returns a grid of NxN random values"""
    return np.random.choice(vals, N*N, p=[0.2, 0.8]).reshape(N, N)

def main():
    # Command line args are in sys.argv[1], sys.argv[2] ..
    # sys.argv[0] is the script name itself and can be ignored
    # parse arguments
    parser = argparse.ArgumentParser(
        description = "Runs Conway's Game of Life system.py."
    )

    parser.add_argument('-s', '--size', dest = 'N', required = False)
    parser.add_argument('-i', '--iterations', dest = 'iter', required = False)
    args = parser.parse_args()

    # set grid size
    N = 100
    if args.N:
        if int(args.N) < 8:
            raise argparse.ArgumentTypeError('min grid is 8x8')
        N = int(args.N)

    iterations = None
    if args.iter:
        if int(args.iter) < 0:
            raise argparse.ArgumentTypeError('cannot have negative iterations')
        iterations = int(args.iter)


    # set animation update interval
    update_interval = 50

    # declare grid
    grid = np.array([])
    # populate grid with random on/off - more off than on
    grid = randomGrid(N)

    # set up animation
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation = 'nearest')
    ani = anim_c(
        fig, img, grid, N,
        update_interval,
        max_iterations = iterations
    )

    plt.show()

class anim_c:
    max_iterations = 200
    def __init__(self, fig, img, grid, N,
                 update_interval = 50, max_iterations = None):

        if max_iterations:
            self.max_iterations = max_iterations
        self.iterations = 0

        self.ani = animation.FuncAnimation(
            fig, self.update, fargs = (img, grid, N),
            frames = 50,
            interval = update_interval,
            save_count = 50,
        )

    def update(self, frameNum, img, grid, N):

        # check iterations, if limit
        self.iterations += 1
        if self.iterations > self.max_iterations:
            print(self.iterations)
            self.ani.event_source.stop()

        # copy grid since we require 8 neighbors for calculation
        # and we go line by line
        new_grid = grid.copy()
        for i in range(N):
            for j in range(N):

                # we have to calc the total amount of `ON` neighbors, we check them
                # by index, using the `%N` for it to continue on the next side of
                # the board when we reached a side. (like the snake game when
                # reaching the walls). Then we have to divide by 255, this is
                # because the values in the grid are 0 or 255, and we are looking
                # how many neighbors the cell has, so we want to change that 255 to
                # 1
                total =int(
                    (
                        grid[i, (j-1)%N] + grid[i, (j+1)%N] + # up/down neigh
                        grid[(i-1)%N, j] + grid[(i+1)%N, j] + # left/right neigh
                        grid[(i-1)%N, (j-1)%N] + grid[(i-1)%N, (j+1)%N] + #diagonal
                        grid[(i+1)%N, (j-1)%N] + grid[(i+1)%N, (j+1)%N]
                    )
                    /255
                )

                # if less than 2 or more than 3, die
                if grid[i, j]  == ON:
                    if (total < 2) or (total > 3):
                        new_grid[i, j] = OFF
                else:
                    if total == 3:
                        new_grid[i, j] = ON

        # update data
        img.set_data(new_grid)
        grid[:] = new_grid[:]
        return img,



# call main
if __name__ == '__main__':
    main()
