#!/usr/bin/env python3
"""
Based on the Jos Stam paper
https://www.researchgate.net/publication/2560062_Real-Time_Fluid_Dynamics_for_Games
and the mike ash vulgarization
https://mikeash.com/pyblog/fluid-simulation-for-dummies.html

https://github.com/Guilouf/python_realtime_fluidsim
"""
import numpy as np
import argparse
import math
import logging

import lib

parser = argparse.ArgumentParser(
    description = "fluid simulation based on the Jos Stam paper"
)

parser.add_argument(
    '-f', '--file',
    dest = 'file', required = True,
    help = 'configuration file for the simulation'
)

args = parser.parse_args()
logger = logging.getLogger('fluid')
logger.setLevel(logging.DEBUG)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

ch.setFormatter(lib.custom_formater_c())

logger.addHandler(ch)

class Fluid:

    def __init__(self):
        self.rotx = 1
        self.roty = 1
        self.cntx = 1
        self.cnty = -1

        self.size = 100 # map size
        self.dt = 0.2  # time interval
        self.iter = 2  # linear equation solving iteration number

        self.diff = 0.0000  # Diffusion
        self.visc = 0.0000  # viscosity

        # Previous densityA
        self.s = np.full(
            (self.size, self.size), 0, dtype=float,
        )
        # Current density
        self.density = np.full(
            (self.size, self.size), 0, dtype=float,
        )

        # array of 2d vectors, [x, y]
        self.velo = np.full(
            (self.size, self.size, 2), 0, dtype=float
        )
        self.velo0 = np.full(
            (self.size, self.size, 2), 0, dtype=float
        )

    def step(self):
        '''
        now we can have a cube step on the sim,
        - it diffuse all three velocites and components
        - fix up velocoites so they keep things incompressible
        - move the velocites around according to the velocites of the fluid
        - fixes the velocites again lol
        - diffuse the dye
        - move the dye around according to the velocity
        '''
        self.diffuse(self.velo0, self.velo, self.visc)

        # x0, y0, x, y
        self.project(self.velo0[:, :, 0], self.velo0[:, :, 1], self.velo[:, :, 0], self.velo[:, :, 1])

        self.advect(self.velo[:, :, 0], self.velo0[:, :, 0], self.velo0)
        self.advect(self.velo[:, :, 1], self.velo0[:, :, 1], self.velo0)

        self.project(self.velo[:, :, 0], self.velo[:, :, 1], self.velo0[:, :, 0], self.velo0[:, :, 1])

        self.diffuse(self.s, self.density, self.diff)

        self.advect(self.density, self.s, self.velo)

    def lin_solve(self, x, x0, a, c):
        '''
        solves some sort of linear differnetial equations, it is used in
        diffuse and project hopefully we wont have to modify it
        '''
        c_recip = 1 / c

        for iteration in range(0, self.iter):
            # Calculates the interactions with the 4 closest neighbors
            x[1:-1, 1:-1] = (x0[1:-1, 1:-1] + a * (x[2:, 1:-1] + x[:-2, 1:-1] + x[1:-1, 2:] + x[1:-1, :-2])) * c_recip

            self.set_boundaries(x)

    def set_boundaries(self, table):
        '''
        we need  walls in the boxes to make the simulation works better
        :return:
        '''

        if len(table.shape) > 2:  # 3d velocity vector array
            # Simulating the bouncing effect of the velocity array
            # vertical, invert if y vector
            table[:, 0, 1] = - table[:, 0, 1]
            table[:, self.size - 1, 1] = - table[:, self.size - 1, 1]

            # horizontal, invert if x vector
            table[0, :, 0] = - table[0, :, 0]
            table[self.size - 1, :, 0] = - table[self.size - 1, :, 0]

        table[0, 0] = 0.5 * (table[1, 0] + table[0, 1])
        table[0, self.size - 1] = 0.5 * (table[1, self.size - 1] + table[0, self.size - 2])
        table[self.size - 1, 0] = 0.5 * (table[self.size - 2, 0] + table[self.size - 1, 1])
        table[self.size - 1, self.size - 1] = 0.5 * table[self.size - 2, self.size - 1] + \
                                              table[self.size - 1, self.size - 2]

    def diffuse(self, x, x0, diff):
        '''
        when you drop sauce in some still water it will spread out, this
        function does that, it will also be used to make the velocities of the
        fluid spread out
        '''
        if diff != 0:
            a = self.dt * diff * (self.size - 2) * (self.size - 2)
            self.lin_solve(x, x0, a, 1 + 6 * a)
        else:  # equivalent to lin_solve with a = 0
            x[:, :] = x0[:, :]

    def project(self, velo_x, velo_y, p, div):
        '''
        since we are using just incompressible fluids (like water and unlike
        air), the amount of fluid in each box must remain constat, this means
        when we add the dye, the same amount of fluid must be taken out. this
        operation runs thru the boxes and fixes them in equilibrium
        '''
        # numpy equivalent to this in a for loop:
        # div[i, j] = -0.5 * (velo_x[i + 1, j] - velo_x[i - 1, j] + velo_y[i, j + 1] - velo_y[i, j - 1]) / self.size
        div[1:-1, 1:-1] = -0.5 * (
                velo_x[2:, 1:-1] - velo_x[:-2, 1:-1] +
                velo_y[1:-1, 2:] - velo_y[1:-1, :-2]) / self.size
        p[:, :] = 0

        self.set_boundaries(div)
        self.set_boundaries(p)
        self.lin_solve(p, div, 1, 6)

        velo_x[1:-1, 1:-1] -= 0.5 * (p[2:, 1:-1] - p[:-2, 1:-1]) * self.size
        velo_y[1:-1, 1:-1] -= 0.5 * (p[1:-1, 2:] - p[1:-1, :-2]) * self.size

        self.set_boundaries(self.velo)

    def advect(self, d, d0, velocity):
        '''
        every box has a set of velocites, and these velocites make things move
        this is calles advection.
        '''
        dtx = self.dt * (self.size - 2)
        dty = self.dt * (self.size - 2)

        for j in range(1, self.size - 1):
            for i in range(1, self.size - 1):
                tmp1 = dtx * velocity[i, j, 0]
                tmp2 = dty * velocity[i, j, 1]
                x = i - tmp1
                y = j - tmp2

                if x < 0.5:
                    x = 0.5
                if x > (self.size - 1) - 0.5:
                    x = (self.size - 1) - 0.5
                i0 = math.floor(x)
                i1 = i0 + 1.0

                if y < 0.5:
                    y = 0.5
                if y > (self.size - 1) - 0.5:
                    y = (self.size - 1) - 0.5
                j0 = math.floor(y)
                j1 = j0 + 1.0

                s1 = x - i0
                s0 = 1.0 - s1
                t1 = y - j0
                t0 = 1.0 - t1

                i0i = int(i0)
                i1i = int(i1)
                j0i = int(j0)
                j1i = int(j1)

                try:
                    d[i, j] = s0 * (t0 * d0[i0i, j0i] + t1 * d0[i0i, j1i]) + \
                              s1 * (t0 * d0[i1i, j0i] + t1 * d0[i1i, j1i])
                except IndexError:
                    # tmp = str("inline: i0: %d, j0: %d, i1: %d, j1: %d" % (i0, j0, i1, j1))
                    # print("tmp: %s\ntmp1: %s" %(tmp, tmp1))
                    raise IndexError
        self.set_boundaries(d)

    def turn(self):
        self.cntx += 1
        self.cnty += 1
        if self.cntx == 3:
            self.cntx = -1
            self.rotx = 0
        elif self.cntx == 0:
            self.rotx = self.roty * -1
        if self.cnty == 3:
            self.cnty = -1
            self.roty = 0
        elif self.cnty == 0:
            self.roty = self.rotx
        return self.rotx, self.roty


if __name__ == "__main__":
    try:
        import matplotlib.pyplot as plt
        from matplotlib import animation

        inst = Fluid()

        try:
            with open(args.file, 'r') as f:
                lines = f.readlines()
        except FileNotFoundError:
            logger.error('can not access file you sent, bailing out :)')
            raise

        densities, velocities, objects, color, force = lib.parse_conf(lines)

        def update_im(i):
            # We add new density creators in here
            factor = 1, 1
            if force:
                if force == 'clockwise':
                    factor = 1.5 * math.sin(i), 1.5 * math.cos(i)
                if force == 'counterclockwise':
                    factor = 1.5 * math.cos(i), 1.5 * math.sin(i)

            for density in densities:
                # add density into a n*n square
                position, value = density
                a, b, c, d = tuple(map(int, position))
                value = int(value)
                inst.density[a:b, c:d] += value

            # We add velocity vector values in here
            for velocity in velocities:
                # add density into a n*n square
                position, value = velocity
                a, b = tuple(map(int, position))
                c, d = tuple(map(int, value))
                inst.velo[a, b] = [
                    c * factor[0],
                    d * factor[1],
                ]

            for obj in objects:
                # add density into a n*n square
                start, end = obj
                a, b = tuple(map(int, start))
                c, d = tuple(map(int, end))
                inst.velo[a:b, c:d] = 0
                inst.density[a+1:b-1, c+1:d-1] += 100
                #inst.density[41:44, 41:44] += 100

            inst.step()
            im.set_array(inst.density)

            q.set_UVC(inst.velo[:, :, 1], inst.velo[:, :, 0]) # TODO
            # print(f"Density sum: {inst.density.sum()}")
            im.autoscale()

        fig = plt.figure()

        # plot density
        try:
            im = plt.imshow(
                inst.density,
                vmax=100,
                interpolation='bilinear',
                cmap=color
            )
        except ValueError:
            logger.error('invalid color name, falling back to default')
            im = plt.imshow(
                inst.density,
                vmax = 100,
                interpolation = 'bilinear',
            )

        # plot vector field
        q = plt.quiver(
            inst.velo[:, :, 1],
            inst.velo[:, :, 0],
            scale=10,
            angles='xy'
        )

        anim = animation.FuncAnimation(fig, update_im, interval=0)
        anim.save("movie.mp4", fps=30) # extra_args=['-vcodec', 'libx264'])
        plt.show()

    except ImportError:
        import imageio

        frames = 30

        flu = Fluid()

        video = np.full((frames, flu.size, flu.size), 0, dtype=float)

        for step in range(0, frames):
            flu.density[4:7, 4:7] += 100  # add density into a 3*3 square
            flu.velo[5, 5] += [1, 2]

            flu.step()
            video[step] = flu.density

        imageio.mimsave('./video.gif', video.astype('uint8'))
