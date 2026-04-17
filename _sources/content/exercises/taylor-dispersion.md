# Taylor Dispersion

Taylor dispersion is caused by the presence of a velocity profile. Solute particles experience different flow velocities depending on their radial position. By means of molecular diffusion, the particles sample these different velocities, which gives a spread in residence time.

:::{figure} ./media/Taylor_dispersion.png
:width: 60%
:align: left
---
Taylor Dispersion
:::

The spread of the solute can be described by a 2D convection-diffusion equation:

$$
\frac{\partial c}{\partial t} + \mathrm{div}\left( \mathbf{v}c - D_{m} \, \mathrm{grad}(c) \right) = 0
$$

In a tube with laminar (Poiseuille) flow, the velocity profile is:

$$
v_{z}(r) = 2\overline{v} \left( 1 - \frac{r^{2}}{R^{2}} \right)
$$

**Questions**:

1. Implement the 2D time-dependent convection-diffusion equations for a cylinder with developed Poiseuille flow.

2. Obtain the molar flow leaving the reactor as a function of time and construct a cumulative residence time distribution (RTD) from that.

3. Critically compare the RTD with results of the 1D models in Exercise 4.5.

:::note  
Ensure that all numerical implementations are consistent with the provided equations and boundary conditions.
:::
