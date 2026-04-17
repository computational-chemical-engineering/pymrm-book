# Multi-component 1D counter-current convection with reaction

Consider the reaction kinetics and boundary conditions as in exercise
3.2 but now with counter-current convection instead of diffusion. Assume
that reactant $A$ and product $C$ move from left to right, and reactant $B$
and product $D$ from right to left. One can imagine counter-current liquid
and gas flows where some of the components are liquid and others gas.
This is modeling a counter-current process where any mass-transfer
resistance are neglected.

$$
\begin{align*}
\frac{\partial c_{A}}{\partial t} + \mathrm{div}(v_f \, c_{A}) &= - r, \quad \text{with} \quad r = - k_{1} \, c_{A} \, c_{B} + k_{2} \, c_{C} \, c_{D} \\
\frac{\partial c_{B}}{\partial t} + \mathrm{div}(v_b \, c_{B}) &= - r \\
\frac{\partial c_{C}}{\partial t} + \mathrm{div}(v_f \, c_{C}) &= r \\
\frac{\partial c_{D}}{\partial t} + \mathrm{div}(v_b \, c_{D}) &= r
\end{align*}
$$

$$c_{A}(0) = 10.0~\mathrm{kmol \cdot m^{-3}}, \quad c_{B}(L) = 10.0~\mathrm{kmol \cdot m^{-3}}, \quad c_{C}(0) = 0.0~\mathrm{kmol \cdot m^{-3}}, \quad c_{D}(L) = 0.0~\mathrm{kmol \cdot m^{-3}}$$

:::{table} 
| Parameter                                      | Value                          |
|------------------------------------------------|--------------------------------|
| Reactor length $L$                              | $1.0~\mathrm{m}$               |
| Kinetic constant $k_{1}$                        | $1.0~\mathrm{m^3 \cdot kmol^{-1} \cdot s^{-1}}$ |
| Kinetic constant $k_{2}$                        | $0.0~\mathrm{m^3 \cdot kmol^{-1} \cdot s^{-1}}$   |
| Velocity $v_f$                                      | $1.0~\mathrm{m \cdot s^{-1}}$ |
| Velocity $v_b$                                      | $-1.0~\mathrm{m \cdot s^{-1}}$ |
:::

**Questions**:

1.  Write down the governing time-dependent evolution equations.

2.  Write down the spatially discretized equations in terms of matrices
    corresponding to the discretization of the divergence and gradient
    operator. Discuss, how the boundary conditions contribute to the
    discretized equations.

3.  Use backwards Euler time discretization for all terms. Write down
    the root-seeking problem that needs to be solved. Also provide the
    Jacobian of the function that needs to be solved.

4.  Formulate the solution algorithm applying the Newton-Raphson method.

5.  Provide a Python implementation for the set of equations and its
    Jacobian using the pymrm building blocks: `construct_grad`,
    `construct_div` and `numjac`.

6.  Implement the numerical solution using the `newton` function from the
    `pymrm` package.

7.  Provide an unsteady solution using Newton-Raphson iteration for
    each time-step.

8.  Play with the reaction rates and boundary conditions. For higher
    reaction rates, when do numerical issues arise? How can these be
    resolved? Hint: the `pymrm` function `clip_approach` can be used as a
    callback function in `newton`, to make sure that values stay within
    bounds also inside iterations.
