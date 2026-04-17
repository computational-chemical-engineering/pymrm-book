# Counter-Current Column Processes

Many separation processes, such as absorption, stripping, and extraction, are often operated in counter-current mode. In this exercise, we consider a simple stationary two-phase counter-current process for one component with linear driving forces for mass transfer:

$$
\begin{align*}
\mathrm{div}\left( U_{g} \, c_{g} \right) &= k_\mathrm{ov} \, a \, \left( c_{l} - \frac{c_{g}}{m} \right), \quad \text{with } \mathrm{sgn}\left( U_{g} \right) > 0, \\
\mathrm{div}\left( U_{l} \, c_{l} \right) &= -k_\mathrm{ov} \, a \, \left( c_{l} - \frac{c_{g}}{m} \right), \quad \text{with } \mathrm{sgn}\left( U_{l} \right) < 0,
\end{align*}
$$

with boundary conditions: $c_{g}(0) = c_{g,\mathrm{in}}$, and $c_{l}(L) = c_{l,\mathrm{in}}.$

Here, $U_{l}$ and $U_{g}$ are superficial velocities, $k_\mathrm{ov} a$ is an overall mass-transfer coefficient, and $a$ is the specific surface area of the interface between the phases $g$ and $l$. The coefficient $m$ is a distribution coefficient. At phase equilibrium, ${c_{g}}/{c_{l}} = m$. The driving force for mass transfer is non-zero when there is a deviation from this equilibrium.

**Questions**:

1. Implement the model in Python.
2. **Advanced**: Derive the analytical solution of the model and verify the implementation with the analytical solution.
3. Extend the model to a multicomponent system with a non-linear equilibrium relation between the components in the two phases.

