# analysis of the examples

simple analysis of what is happening in each configuration example, in case you
do not have any idea of what is going on.

**NOTE** when talking about density, we are talking about the dye density.

let's start with the basic one:

## `no_obj.conf`
simple fluid sim without anything fancy going on. It is clear how the dye is
spread across the fluid, the velocity force is linear so no crazy circles or
anything. Nevertheless it let you appreciate how the system works, in its
more basic form.

It also works to see how the conf file looks:
```
density {
    # position: density
    10 30 10 30: 100
    # 70 90 70 90: 100
}
velocity {
    10 10: 2 2
}
color viridis
```
and how it supports comments

## `obj_centre.conf`
fluid simulation where there is an object at the centre of the grid, as you
can see in the video the dye goes around the fluid without touching it inside,
this creates the "illusion" that there is an object there. Focus on the word
_illusion_, because all we are doing is not letting any forces of the dye get
inside that square. The dye does not bounce or anything, that would implicate
getting into more complex maths, instead this method works and looks pretty
similar.

here is the conf file:
```
density {
    # position: density
    10 30 10 30: 100
}
velocity {
    10 10: 2 2
}
object {
    40 50 40 50
}
color viridis
```

## `mess.conf`
this fluid simulation is a combination of the other two, it has another dye
dense zone, and it has two velocities applied instead of one, it also has two
objects that will disturbe the flow of the fluid. This shows how can we build
a complex simulation, just by adding more velocities and more dye zones in the
fluid

here is the actual conf file:
```
density {
    # position: density
    10 30 10 30: 100
    70 90 70 90: 100
}
velocity {
    90 90: -2 -2
    10 10: 2 2
}
object {
    30 50 30 50
    55 60 55 60
}
color magma
```

## `clockwise.conf` and `counterclockwise.conf`

here are the last two examples, they look very different from the other ones
because in these two the velocities are animated, meaning that they are not
just linear. They move in a circular way the first as the name implies, move
clockwise and the latter counterclockwise. The way we achieve this is simply
using the sine and cosine function add some time to the function and the
fluid starts moving in circles.

```
density {
    # position: density
    20 40 20 40: 100
    60 80 60 80: 100
}
velocity {
    45 50: 2 2
}
object {
    60 80 20 40
    20 40 60 80
}
color viridis
force clockwise
```
