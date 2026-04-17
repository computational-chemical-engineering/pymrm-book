# Multi-component 1D counter-diffusion with reaction

Build a model of two reactive components counter-diffusing in a
membrane. A chemical reaction is carried out in a membrane reactor. The
reaction scheme and reaction kinetics are given as follows:

$$A + B \rightleftarrows C + D$$

Reaction kinetics:
$- r_{A} = - r_{B} = r_{C} = r_{D} = k_{1} \, c_{A} \, c_{B} - k_{2} \, c_{C} \, c_{D}$.
The reactants $A$ and $B$ are fed at different sides of a porous membrane.
The concentrations on the boundaries are provided in the figure below.
For the description of this problem you may assume that the diffusion
obeys Fick's law.

:::{figure} media/counter_diffusion_1d.png
:alt: Counter diffusion 1D
:width: 50%
:::

:::{table} 
| Parameter                                      | Value                          |
|------------------------------------------------|--------------------------------|
| Membrane thickness $L$                         | $0.01~\mathrm{m}$              |
| Kinetic constant $k_{1}$                       | $10^6~\mathrm{m^3 \cdot kmol^{-1} \cdot s^{-1}}$ |
| Kinetic constant $k_{2}$                       | $0~\mathrm{m^3 \cdot kmol^{-1} \cdot s^{-1}}$   |
| Effective diffusion coefficients of A, B, C and D | $10^{-5}~\mathrm{m^2 \cdot s^{-1}}$ |
:::

**Questions**:

1.  Write down the governing steady-state equations. For the diffusive
    term use the notation with a divergence and gradient operator.

2.  Write down the spatially discretized equations in terms of matrices
    corresponding to the discretization of the divergence and gradient
    operator. Discuss, how the boundary conditions contribute to the
    discretized equations.

3.  The reaction term is non-linear. Formulate the equation to be solved
    as a root-seeking problem (i.e. a set of non-linear equations that
    all need equal zero).

4.  Formulate the solution algorithm applying the Newton-Raphson method.

5.  Provide a Python implementation for the set of equations and its
    Jacobian using the pymrm building blocks: `construct_grad`,
    `construct_div` and `numjac`.

6.  Implement the numerical solution using the `newton` function from the
    `pymrm` package.

7.  Obtain the steady state solution using Newton-Raphson iteration.

8.  Make an unsteady implementation assuming initial zero
    concentrations.

9.  Play with the reaction rates and boundary conditions.
