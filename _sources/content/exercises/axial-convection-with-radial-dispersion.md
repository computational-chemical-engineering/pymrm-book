# Axial Convection with Radial Dispersion

Implement species transport in a tube with reaction at the tube wall. The governing equation is:

$$
v \frac{\partial c}{\partial x} = \frac{1}{r} \frac{\partial}{\partial r} \left( r D_{rad} \frac{\partial c}{\partial r} \right) = \mathrm{div}\left( D_{rad} \, \mathrm{grad}(c) \right).
$$

The inlet profile is uniform. Assume an infinitely fast surface reaction at the tube wall, meaning $c(R) = 0$. Choose your own parameters or make the equations dimensionless.

**Questions**:

1. What is the proper boundary condition at $r = 0$?

2. Use the method of lines: Perform a spatial discretization in the radial direction to obtain a set of ODEs:

   $$
   \frac{d\mathbf{c}}{dx} = \ldots
   $$

3. Use a standard SciPy ODE solver, `solve_ivp`, to solve the set of equations.

4. Compute the flux at the wall as a function of $x$.

5. Compute the Sherwood number (based on $\langle c \rangle$) as a function of $x$.

:::{note}
Ensure that all numerical implementations are consistent with the provided equations and boundary conditions.
:::
