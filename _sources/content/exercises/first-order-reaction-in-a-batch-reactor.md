# First order reaction in a batch reactor

Implement first order kinetics of one species in a batch reactor.

$$\frac{dc}{dt} = - kc.$$

Suggested approach:

-   Write a function that computes the reaction rate for a provided
    concentration

-   Write this function in such a way that the reaction rate
    coefficients can be passed as parameters.

-   Provide an analytical expression of the concentration as function of
    time. Verify your codes with the analytical solution for the case
    $k = 1.0~\mathrm{s^{-1}}$, with initial concentration
    $c_{0} = 1.0~\mathrm{mol\cdot m^{-3}}$.

**Questions**:

1.  Solve using forward Euler discretization

2.  Solve using backward Euler discretization

3.  Solve using `scipy.integrate.solve_ivp`
