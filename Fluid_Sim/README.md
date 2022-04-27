================
fluid simulation
================

basic 2D fluid simulation based on mike ash post:
https://mikeash.com/pyblog/fluid-simulation-for-dummies.html
and https://github.com/Guilouf/python_realtime_fluidsim

how it works
============

I'd recommend reading `notes.md` in this same repository, it will have
the notes I took while trying to understand the code and while reading
the blog post from mike ash, the text is not long and gives a good
introduction on how all this will work.

installation
===========

well, you'll need python3 installed of course, then you can do:
```
pip install -r requirements.txt
```
NOTE: I'd strongly suggest that you run the pip install inside a virutalenv
(https://docs.python.org/3/library/venv.html), this way you wont have to mess
with numpys versions and all those things.

usage
=====

the usage is pretty straight forward, you can just run the file and send the
config file
```
./fluid.py -f <conf file>
```
you can also do
```
./fluid.py --help
```
in case you forget the `f`. It is the only param the sim will receive, so
it is kind of important. The param is not optional, you must send a conf
file with every run. If you just want to see it running, grab one of the files
inside the `examples/` directory.

the conf file
-------------
its pretty similar to conf files in BSD systems, like httpd.conf, I chose this
format because it is really human readable and using json just felt kind of
weird for this project in particular.

here is an example
```
density {
    # position: density
    10 30 10 30: 100
    # 70 90 70 90: 100
}
velocity {
    90 90: -2 -2
    10 10: 2 2
}
object {
    40 50 40 50
}
color inferno
force clockwise
```
as you can see there are 5 keywords:
- density
  - position: density
- velocity
  - position: velocity
- object
  - edges of a square
- color
  - please go
    [here](https://matplotlib.org/3.5.0/tutorials/colors/colormaps.html)
    to check all the color available. (I'll save you time, the coolest ones are
    magma, viridis, inferno and plasma.)
- force
  - you can animate the velocity force meaning, you can make that it goes in
    a circular way: **counterclockwise** or **clockwise**.

the order of the keywords does not matter, so you can start by setting the
color then the object the parser wont care.

also, comments are supported, just **start** a line with `#`, if the `#` is not
at the beginning of the file the line wont be valid, so just don't type comments
at the end of lines.
