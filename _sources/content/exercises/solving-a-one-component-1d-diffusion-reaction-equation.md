# Solving a one-component 1D diffusion-reaction equation 

In this exercise you will build an implicit solver for a diffusion
equation. A one-component stationary diffusion equation with constant
coefficients has the form

$$D\ \frac{\partial^{2}c}{\partial x^{2}} = 0$$

This equation needs to be solved on a domain of length $L$ with on the
left and right boundaries a boundary condition of the form

$$a\frac{\partial c}{\partial n} + bc = d,$$

where $n$ indicates the outward pointing normal direction, i.e. $- x$
for the left boundary and $x$ for the right boundary.

**Questions**:

1. Assume a spatial discretization of $N$ cells with points $j$ located
    in cell centers. Write down the spatial discretization formula for
    the diffusion terms for points $j = 1,\ldots,N - 2$. (Note that
    cells $j = 0$ and $j = N - 1$, are neighboring a boundary).

2. Write down the spatial discretization formula's for points $j = 0$
    and $j = N - 1$ by implementing a Dirichlet boundary condition
    ($a = 0$, $b = 1$).

3. Write down the resulting formula's in matrix-vector form.

4. Implement the matrix-vector equation in Python using SciPy. Define a
    sparse matrix using the SciPy sparse array, e.g., by means of:
    scipy.sparse.diags_array.

5. Verify the implementation for Dirichlet BCs on both sides.

6. Extend the boundary condition implementation to general mixed
    boundary conditions (any value of $a$ and $b$). Write down the
    resulting formula's in matrix-vector form.

7. Verify the implementation of the mixed boundary conditions by
    choosing values of $a$, $b$ and $d$ on both sides and compare the
    result with the expected analytical solution.

Dispersion with a first order reaction obeys

$$D\ \frac{\partial^{2}c}{\partial x^{2}} - kc = 0$$

**Questions**:

8. Include the first order reaction term to the matrix-vector equation.

9. Verify the implementation for varying values of $k$ and general
    mixed boundary conditions by comparison with the expected analytical
    solution.

The unsteady diffusion (first order) reaction equation is

$$\frac{\partial c}{\partial t} = D\ \frac{\partial^{2}c}{\partial x^{2}} - kc$$

**Questions**:

10. Add an implementation of the accumulation term using Euler-backward
    time discretization.

11. Solve the equations in time and verify the accumulation term by
    comparison with analytical solutions for (simple) initial and
    boundary conditions.
