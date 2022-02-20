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

def random_grid(N):
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
    parser.add_argument('-f', '--config-file',
                        dest = 'filename', required = False)
    args = parser.parse_args()

    # set grid size
    N = 100
    if args.N:
        if int(args.N) < 8:
            raise argparse.ArgumentTypeError('min grid is 8x8')
        N = int(args.N)



    # read file and parse the info
    coords = []
    if args.filename:
        filename = args.filename
        with open(filename, 'r') as f:
            lines = f.readlines()
            # FIXME make the width and height do something
            (width, height), iterations, coords = parse_lines(lines)

    grid = np.zeros((width, height))

    if len(coords) < 0:
        grid = random_grid(N)

    for x, y in coords:
        grid[x][y] = ON

    iterations = None
    if args.iter:
        if int(args.iter) < 0:
            raise argparse.ArgumentTypeError('cannot have negative iterations')
        iterations = int(args.iter)

    # set animation update interval
    update_interval = 50

    # set up animation
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation = 'nearest')
    ani = anim_c(
        fig, img, grid, width, height,
        update_interval,
        max_iterations = iterations
    )

    plt.show()

def parse_lines(lines):
    '''
    parse text file lines, we have to go to add all the if's becuase
    the user might want to add comments to the file. But at the end of
    the day we just care for three things:

    :returns tuple: (width, height)
    :returns generations: int
    :returns list: tuple list width coord x and y

    So at the end it will return something like this
    return ((width, height), generations, [(1, 3), (4, 4)])
    '''
    # get width and height
    if '#' in lines[0]:
        width, height, _ = lines[0].split(' ', 2)
    else:
        width, height = lines[0].split(' ', 1)

    # get generations
    if '#' in lines[1]:
        generations, _ = lines[1].split(' ', 1)
    else:
        generations = lines[1]

    try:
        width = int(width)
        height = int(height)
        generations = int(generations)
    except ValueError:
        raise RuntimeError('bad config file, please refer to config to check'
                           ' how to fix it')

    coords = []
    for i, line in enumerate(lines):
        if len(line) < 2:
            continue
        if i < 2:
            continue
        line = line.strip()
        try:
            if '#' in line:
                x, y, _ = line.split(' ', 2)
            else:
                x, y = line.split(' ')
        except ValueError:
            print('bad config file, please refer to config to check how'
                  f' to fix it. (check line {i})')
            raise
        if not x.isnumeric() or not y.isnumeric():
            raise RuntimeError('some of the coords you wrote in the config'
                  f' file are not numeric, please fix this. (check line {i})')
        coords.append((int(x), int(y)))

    return ((width, height), generations, coords)


class anim_c:
    max_iterations = 200
    def __init__(self, fig, img, grid, width, height,
                 update_interval = 50, max_iterations = None):

        if max_iterations:
            self.max_iterations = max_iterations
        self.iterations = 0

        self.ani = animation.FuncAnimation(
            fig, self.update, fargs = (img, grid, width, height),
            frames = 60,
        )

    def update(self, frameNum, img, grid, width, height):

        # check iterations, if limit
        self.iterations += 1
        if self.iterations > self.max_iterations:
            self.ani.event_source.stop()

        # copy grid since we require 8 neighbors for calculation
        # and we go line by line
        new_grid = grid.copy()
        for i in range(width):
            for j in range(height):

                # we have to calc the total amount of `ON` neighbors, we check
                # them by index, using the `%N` for it to continue on the next
                # side of the board when we reached a side. (like the snake
                # game when reaching the walls). Then we have to divide by 255,
                # this is because the values in the grid are 0 or 255, and we
                # are looking how many neighbors the cell has, so we want to
                # change that 255 to 1
                total =int(
                    (
                        grid[i, (j-1)% height] + grid[i, (j+1)% height] +
                        grid[(i-1)% width, j] + grid[(i+1)% width, j] +
                        grid[(i-1)% width, (j-1)% height] +
                        grid[(i-1)% width, (j+1)% height] +
                        grid[(i+1)% width, (j-1)% height] +
                        grid[(i+1)% width, (j+1)% height]
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
