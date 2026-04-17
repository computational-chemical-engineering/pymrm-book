# Convection-dispersion-reaction in a 1D reactor model 

In this exercise you will build an implicit solver for unsteady
convection-dispersion-reaction equations. A one-component unsteady
convection-reaction equation with constant coefficients has the form

$$\frac{\partial c}{\partial t} + v~\frac{\partial c}{\partial x} - D_{ax}~\frac{\partial^{2}c}{\partial x^{2}} - r = 0 \rightarrow \frac{\partial c}{\partial t} + \mathrm{div}\left( vc - D_{ax}~\mathrm{grad}(c) \right) - r = 0$$

The solution method will be the method-of-lines where the spatial
dependence is discretized first. After discretization you will get a set
of ODE's. Here the unknowns in the system are represented by a column vector. Differential operators become matrices. After spatial discretization we get:

$$\frac{\partial\mathbf{c}}{\partial t} + \mathbf{D} \, \left( \mathbf{U}\,\mathbf{c} + \mathbf{u}_{bc} - D_{ax}~\left( \mathbf{G} \, \mathbf{c} + \mathbf{g}_{bc} \right) \right) = 0$$

In this equation conventions are used to write (column) vectors as bold roman lowercase symbols.
For example, $\mathbf{c}$ denotes the concentration vector. A component $c_{j}$ of this column vector corresponds to the concentration in spatial cell $j$.
The matrix $\mathbf{D}$ is the discretized divergence operator, and $\mathbf{G}$ the gradient matrix.
For the discretized gradient operator, inhomogeneous boundary conditions, give rise to vector with non zero entries only near the boundaries. This vector is indicated by $\mathbf{g}_{bc}$. The convective term is also represented by a matrix-vector multiplication ($\mathbf{U} \, \mathbf{c}$) plus a vector ($\mathbf{u}_{bc}$).

In the Python codes we will for example use $\tt{div\_mat}$ for the divergence matrix. In `SciPy` the @ operator is used to indicate matrix multiplication.
For time-discretization we will use
implicit Euler. It looks schematically, in matrix and Python notation, like:

$$
\begin{align*}
\mathbf{g}\left( \mathbf{c}^{n + 1} \right) & = \frac{\mathbf{c}^{n + 1} - \mathbf{c}^{n}}{\Delta t} + \mathbf{D} \, \left( \mathbf{U}\,\mathbf{c}^{n + 1} + \mathbf{u}_{bc} - D_{ax}~\left( \mathbf{G} \, \mathbf{c}^{n + 1} + \mathbf{g}_{bc} \right) \right) = 0\\
\mathbf{g}\left( \mathbf{c}^{n + 1} \right) & = \frac{\mathbf{c}^{n + 1} - \mathbf{c}^{n}}{\Delta t} + \tt{div\_mat} \,  @  \, \left( \tt{conv\_mat} \, @ \, \mathbf{c}^{n + 1} + \tt{conv\_bc} - D_{ax} * \left( \tt{grad\_mat} \, @ \, \mathbf{c}^{n + 1} + \tt{grad\_bc} \right) \right) = 0
\end{align*}
$$

**Questions**:

1. Perform the spatial discretization by constructing the sparse
    matrices for the dispersion and convective terms. Assume a general
    boundary condition at the inlet,
$$D_{ax}~\frac{\partial c}{\partial n} + v~c = v~c_{0}$$
and a Neumann boundary condition at the outlet

$$\frac{\partial c}{\partial n} = 0$$

Make use of the `pymrm` functions `construct_grad`, `construct_conv`, and
`construct_div`.

2. Perform the time discretization for the convection-dispersion by
    means of the implicit Euler scheme, and formulate the problem,
    without reaction, as a root-seeking problem:
    $\mathbf{g}\left( \mathbf{c}^{n + 1} \right) = 0$ for each
    time step.

3. Provide an Python implementation, that consists of a time-loop,
    where for each timestep the newton method from the pymrm package is
    applied to solve the root-seeking problem.

4. Test your code for only dispersion, only convection, combined etc.
    Play around with parameters (numerical and physical ones).

5. Include a first order reaction term. Compare results to the analytical solution (in a semi-infinite domain) for steady state.

6. Adapt the code for general non-linear kinetics. Make use of the
    function numjac to compute the Jacobian of such a reaction term.

7. Verify your code by implementing a reaction kinetics
    $r = - k\,c^{\alpha}$.

    :::{note}
    For power-law kinetics with values of $\alpha < 1$ the derivative of the reaction rate diverges when $c\rightarrow 0$.
    This gives issues for numerical solutions with the Newton-Raphson method, which depends on linearized equations. In general, fractional powers are cumbersome, because, within iterations, negative concentrations might occur. Fractional powers of negative numbers are ill defined (i.e.\ give rise to imaginary numbers).    
     Power-law behavior at small concentrations is also physically unrealistic. 
    A recommended regularization is making the kinetics linear, when concentrations become of the order of a user-supplied small concentration $c_\mathrm{small}$:
    $r = - k\,(|c| + c_\mathrm{small})^{\alpha-1} \, c$ 
    :::