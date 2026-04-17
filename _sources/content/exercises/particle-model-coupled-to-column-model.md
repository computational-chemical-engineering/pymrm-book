# Particle Model Coupled to Column Model

Consider both a batch model and a particle model. Inside a particle, a diffusion-reaction equation is solved in a spherically symmetric geometry:

$$
\frac{\partial c_{s}}{\partial t} = \frac{1}{r^{2}} \frac{\partial}{\partial r} \left( r^{2} D \frac{\partial c_{s}}{\partial r} \right) + \text{react} = \mathrm{div}_{r}\left( D \, \mathrm{grad}_{r}\left( c_{s} \right) \right) + \text{react},
$$

with the boundary condition:

$$
- D \left. \frac{\partial c_{s}}{\partial r} \right|_{R} = k_{m} \left( c_{s}(R) - c_{f} \right).
$$

This model is coupled to a balance of a column:

$$
\begin{align*}
\frac{\partial \varepsilon_{b} c_{f}}{\partial t} + \frac{\partial U c_{f}}{\partial z} - \frac{\partial}{\partial z} \left( D_{ax} \frac{\partial c_{f}}{\partial z} \right) &= r_{\mathrm{app}}, \\
\frac{\partial \varepsilon_{b} c_{f}}{\partial t} + \mathrm{div}_{z}\left( U c_{f} - D_{ax} \, \mathrm{grad}_{z}\left( c_{f} \right) \right) &= r_{\mathrm{app}}.
\end{align*}
$$

The apparent reaction rate can be obtained from the particle model as:

$$
r_{\mathrm{app}}(x) = - a D \left. \frac{\partial c_{s}}{\partial r} \right|_{R}, \quad a = \frac{3 \left( 1 - \varepsilon_{b} \right)}{R}.
$$

**Questions**:

1. Make separate implementations for the particle and reactor models.

2. Verify both implementations. (Think of good critical test cases.)

3. Combine the two models such that the particle model can provide the apparent reaction rate for the batch reactor. Use an explicit coupling where, within a time step, you call the models sequentially.

4. Verify the explicit coupling.

5. Provide an implicitly coupled implementation using a "Schur complement" strategy.

6. Verify the implicit coupling.

:::note  
Ensure that all numerical implementations are consistent with the provided equations and boundary conditions.
:::
