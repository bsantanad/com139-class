# conways game of life sim

implementation of game of life. (it has only been tested in unix systems but
should work in Windows as well)


## setup

download the repo, and install the requirements in `requirements.txt`
```
pip install -r requirements.txt
```

## usage

If you want to run it with random values you can do

```
./conway.py
```
or
```
python conway.py
```

### flags

you can run the simulation with the following flags.

```
usage: conway.py [-h] [-s N] [-i ITER] [-f FILENAME]

Runs Conway's Game of Life system.py.

options:
  -h, --help            show this help message and exit
  -s N, --size N
  -i ITER, --iterations ITER
  -f FILENAME, --config-file FILENAME
```

this means you can do
```
./conway.py -s 200 -i 4
```
This would create a simulation with 200x200 grid and iterate 4 times the
simulation.

### config file

you can run it with a config file as well
```
./conway.py -f <path_to_file>
```
The config file must have the following format:
```
50 50   # im the size of the grid
1       # im the num of iterations
24 24   # im the coords of a cell that is ON
23 24
22 24
23 23
24 25
```
As you can see the config file support comments, so go crazy :)

## report

the report will look something like this:
```
------------------------
iteration 1
block total: 0 - 0.00 %
beehive total: 0 - 0.00 %
loaf total: 0 - 0.00 %
boat total: 0 - 0.00 %
tub total: 0 - 0.00 %
blinker total: 1 - 100.00 %
toad total: 0 - 0.00 %
beacon total: 0 - 0.00 %
glider total: 0 - 0.00 %
lw-spaceship total: 0 - 0.00 %
total number of shapes: 1
------------------------
iteration 2
block total: 0 - 0.00 %
beehive total: 0 - 0.00 %
loaf total: 0 - 0.00 %
boat total: 0 - 0.00 %
tub total: 0 - 0.00 %
blinker total: 1 - 100.00 %
toad total: 0 - 0.00 %
beacon total: 0 - 0.00 %
...
```
It will count the number of shapes in the current iteration, as you can
see when you run the program the report goes to `STDOUT`, so you can do
whatever you want.

if you want to run store it in a file you could do (unix systems):
```
./conway.py -f 1.in > out
```



If you want to store the report on a file in Windows systems, please refer
[here][msft]

[msft]: https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_redirection?view=powershell-7.2

