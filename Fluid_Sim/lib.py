#! /usr/bin/env python
import logging

def parse_conf(lines):
    '''
    parse conf file for the simulation. To see the format of the file
    please refer to README. If you dont feel like it well it's pretty
    similar to conf files in  BSD systems, like httpd.conf etc...

    We only have 3 keywords: `color`, `density`, and `velocity`.
    The file will look something like this:
    >>> color: blue
    >>> density {
    >>>     # position: density
    >>>     15 27 15 27: 100
    >>>     30 35 30 35: 100
    >>> }
    >>> velocity {
    >>>     # position: velocity
    >>>     20 20: -1 1
    >>>     32 32: -2 -2
    >>> }

    NOTE: comments only supported at start of lines.

    :returns tuple: (density: list, velocity: list, color: string)
    '''
    lines[:] = [line.strip() for line in lines] # remove tabs and spaces
    density = []
    velocity = []
    color = None
    switch = False
    for i, line in enumerate(lines):
        line_num = i + 1
        if line.startswith('#'): # we dont care of lines with comments
            continue

        if line.startswith('density'):
            switch = 'density'
            continue

        if line.startswith('velocity'):
            switch = 'velocity'
            continue

        if switch: # we are inside the braces of density
            if line.startswith('}'):
                switch = False
                continue
            if switch == 'density':
                try:
                    position, value = line.split(':')
                    a, b, c, d = position.split()
                    tmp = ((a, b, c, d), value)
                    density.append(tmp)
                except ValueError:
                    logging.error(f'bad syntax in conf file, line {line_num},'
                                  ' skipping line.')
                continue
            if switch == 'velocity':
                try:
                    position, value = line.split(':')
                    a, b = position.split()
                    c, d = value.split()
                    tmp = ((a, b), (c, d))
                    velocity.append(tmp)
                except ValueError:
                    logging.error(f'bad syntax in conf file, line {line_num},'
                                  ' skipping line.')
                continue

        if line.startswith('color'):
            try:
                _, color = line.split()
            except ValueError:
                logging.error(f'bad syntax in conf file, line {line_num},'
                              ' falling back to default color')
                color = 'plasma'
            continue

    return density, velocity, color
