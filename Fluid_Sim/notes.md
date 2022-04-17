# initial things
fluid sim is based on navier-stokes equations, but they are to complicated
let's just focus on the code

think of a fluid as a collection of boxes that interact with each other
each one properties like velocity and density

the water is equally dense everywhere, when talking about
density we are going to talk about dye density not the fluid

we'll have a 3D array that represents the cubes

each cube will have:
- size (same for all cubes)
- length of the time step
- the amount of diffusion (how fast stuff spreads out in the fluid)
- viscosity (how thick the fluid is)

- density array
- three velocity arrays (x, y, z)

we need a function to create the cube and one to destroy it

we also need a function to add the density (dye) to the cube
and a function to add velocity

# sim outline

there are 3 main operations

- diffuse: when you drop sauce in some still water it will spread out, this
  will also be used to make the velocities of the fluid spread out

- project: since we are using just incompressible fluids (like water and not
  like air), the amount of fluid in each box must remain constant, this means
  when we add the dye, the same amount of fluid must be taken out. this
  operation runs thru the boxes and fixes them in equilibrium

- advect: every box has a set of velocities, and these velocities make things
  move. This is called advection.

There are some subroutines used by these operations.

- `set_bnd`, set bound: we need walls in the boxes to make the simulation works
  better

- `lin_solve`, solves some sort of linear differential equation. is used in
  diffuse and project

now we can have a cube step on the sim,
- it diffuse all three velocities and components
- fix up velocities so they keep things incompressible
- move the velocities around according to the velocities of the fluid
- fixes the velocities again lol
- diffuse the dye
- move the dye around according to the velocity
