# Particle model: first order reaction

Numerically solve the stationary spherically symmetric problem

$$\frac{1}{r^{2}}\frac{\partial}{\partial r}\left( r^{2}D\frac{\partial c}{\partial r} \right) - kc = \mathrm{div}\left( D\ \mathrm{grad}(c) \right) - kc = 0$$

with the boundary condition $c(R) = 1$.

**Questions**:

1. Perform the spatial discretization (start with a uniform grid) and
   implement it in Python. Note that the spherical geometry is
   accounted for by the proper definition of the divergence operator.

2. Construct, implement, and solve the matrix-vector equation.

3. Compute the apparent reaction rate from the concentration gradient
   at the surface of the particle.

4. Investigate the effectiveness as a function of the Thiele modulus.

5. Does the result correspond to the analytical solution?

6. Consider the high Thiele modulus case and improve the solution by
   using a spatial discretization that is refined near the wall.
