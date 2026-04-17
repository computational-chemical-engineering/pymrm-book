# Equilibrium consecutive batch reactions

Implement the kinetics:

$$A\begin{matrix}
k_{1} \\
 \rightleftarrows \\
k_{-1}
\end{matrix}B\begin{matrix}
k_{2} \\
 \rightarrow \\
\end{matrix}C$$

Suggested approach:

-   Write a function that computes the reaction rate for a provided
    concentration

-   Write this function in such a way that the reaction rate
    coefficients can be passed as function argument.

-   Concentration column vector of length 3 as input (for components $A$,
    $B$, $C$)

-   Reaction rate vector of length 3 as output

-   Provide an analytical expression of the concentration as function of
    time. Verify your codes with the analytical solution for the case
    $k_{1} = 2.0~\mathrm{s^{-1}}$, $k_{-1} = 1.0~\mathrm{s^{-1}}$ and
    $k_{2} = 3.0~\mathrm{s^{-1}}$, with initial concentration
    $c_A = 1.0~\mathrm{mol\cdot m^{-3}}$, $c_B = 0.0~\mathrm{mol\cdot m^{-3}}$,
    $c_C = 0.0~\mathrm{mol\cdot m^{-3}}$.

**Questions**:

1.  Solve using forward Euler discretization

2.  Solve using backward Euler discretization

3.  Implement backward Euler discretization, but allow for extension to
    non-linear kinetics. Express the discretized equations for a
    time-step as a root-seeking problem for the non-linear set of
    equations (and use Newton-Raphson).

4.  Solve using `scipy.integrate.solve_ivp`.
