# Dehydrogenation of Ethanol

Consider the heterogeneously catalyzed reaction:

$$\text{Ethanol} \rightarrow \text{Acetaldehyde} + \mathrm{H}_{2}$$

The first-order (surface) reaction rate coefficient is $k_{r} = 0.45~\mathrm{m~s^{-1}}$. The (zero flux) binary mass-transfer coefficients are: $k_{12} = 0.07~\mathrm{m~s^{-1}}$, $k_{13} = 0.23~\mathrm{m~s^{-1}}$, and $k_{23} = 0.23~\mathrm{m~s^{-1}}$.
These values are given at the operating conditions $p = 1.0 \cdot 10^{5}~\mathrm{Pa}$ and $T = 548~\mathrm{K}$. The bulk gas phase composition is:  
$x_{1} = 0.60$, $x_{2} = 0.20$, $x_{3} = 0.20$.  

Assume ideal gases and that a film model is appropriate.

**Questions**:

1. Write down the Maxwell-Stefan equations.

2. Solve this system by direct numerical integration. What are the molar fluxes?

3. Solve this system using the exact "matrix method."

4. Make a linear approximation of the concentration profiles and solve the resulting algebraic equations.

5. Solve this system using the approximate "matrix method" in a mass-average reference frame.

6. Compare the accuracy of the different methods.

:::{note}
Ensure that all numerical implementations are consistent with the provided equations and parameter values.
:::
