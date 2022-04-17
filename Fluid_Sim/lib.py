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
                    logger.warning(f'bad syntax in conf file, line {line_num}'
                                    ' maybe in the denisty part? skipping'
                                    ' line')
                    continue
            if switch == 'velocity':
                try:
                    position, value = line.split(':')
                    a, b = position.split()
                    c, d = value.split()
                    tmp = ((a, b), (c, d))
                    velocity.append(tmp)
                except ValueError:
                    logger.warning(f'bad syntax in conf file, line {line_num}'
                                    ' maybe in the velocity part? skipping'
                                    ' line.')
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

class custom_formater_c(logging.Formatter):
    '''
    add color to logger, just copy and pasted from:
    https://stackoverflow.com/a/56944256
    '''

    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }
    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

logger = logging.getLogger('fluid')
logger.setLevel(logging.DEBUG)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

ch.setFormatter(custom_formater_c())

logger.addHandler(ch)
