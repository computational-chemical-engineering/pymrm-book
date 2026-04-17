# Coupled Batch Reactor and Particle Model

Consider both a batch reactor model and a particle model. Inside a particle, a diffusion-reaction equation is solved in a spherically symmetric geometry:

$$
\frac{\partial c_{s}}{\partial t} = \mathrm{div}\left( D \, \mathrm{grad}\left( c_{s} \right) \right) + r,
$$

with the boundary condition:

$$
- D \left. \frac{\partial c_{s}}{\partial r} \right|_{R} = k_{m} \left( c_{s}(R) - c_{f} \right).
$$

This model is coupled to a balance of a batch reactor:

$$
\varepsilon_{b} \frac{dc_{f}}{dt} = r_{\mathrm{app}},
$$

where the apparent reaction rate can be obtained from the particle model as:

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
