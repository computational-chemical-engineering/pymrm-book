# Convection of one species using different schemes

The unsteady convection equation for a concentration $c$ that is
convected with velocity $v$ is:

$$\frac{\partial c}{\partial t} = - v\ \frac{\partial c}{\partial x}$$

For unsteady problems we will use the method of lines. After performing
a spatial discretization the resulting set of ODE's has the form:

$$\frac{d\mathbf{c}}{dt} = \mathbf{f}\left( t,\mathbf{c} \right)$$

where $\mathbf{c}$ is the column vector that contains the
concentrations, $c_{i}$, where $i$ is the label of the grid cell.

You are asked to implement the one-component convection equation using
the method-of-lines described above, using different spatial
discretization methods, namely, upwind, central differencing and a total
variance diminishing (TVD) scheme. For the time integration use a
standard IVP solver.

Suggested approach:

-   Use NumPy arrays to store the concentrations, $c_{i}$, and right
    hand side, $f_{i}$, at different axial positions $i$.

-   Prefer using NumPy array indexing notation over for loops for
    element-wise operations. This approach leverages NumPy's optimized
    performance and often results in more readable and efficient code.

-   For each method, plot axial concentration profiles for several
    times.

-   Compare your results with an analytical solution of the problem to
    verify your code.

-   Play with the number of grid points $N$ used in the spatial
    discretization.

**Questions**:

1.  Implement upwind discretization, where

$$f_{i} = \left\{ \begin{matrix}
  - v\left( \frac{c_{0} - c_{in}}{\Delta x} \right),\ \text{for}\ i = 0 \\
  - v\left( \frac{c_{i} - c_{i - 1}}{\Delta x} \right),\ \text{for}\ i > 0
\end{matrix} \right.\ $$

2.  Implement central differencing, where

$$f_{i} = \left\{ \begin{array}{l}
  - v\left( \frac{c_{1} - c_{in}}{\Delta x} \right),\ \text{for}\ i = 0 \\
  - v\left( \frac{c_{i + 1} - c_{i - 1}}{2\ \Delta x} \right),\ \text{for}\ i > 0 \\
  - v\left( \frac{c_{i} - c_{i - 1}}{\Delta x} \right),\ \text{for}\ i = N - 1
\end{array} \right.\ $$

3.  Implement a TVD scheme, e.g. Min-Mod, for the convection. See lecture notes for the scheme.
