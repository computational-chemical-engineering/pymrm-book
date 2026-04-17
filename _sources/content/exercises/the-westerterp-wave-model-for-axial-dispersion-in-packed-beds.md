# The Westerterp Wave-Model for Axial Dispersion in Packed Beds

Flow profiles in a tube, combined with diffusion in the radial direction, can cause dispersion of a solute. Solute particles experience different flow velocities depending on their radial position within the tube: particles near the center move faster, while those near the walls move slower. This difference in velocity causes the solute to spread along the length of the tube, a phenomenon known as Taylor dispersion. This is explicitly modeled in Exercise 5.7.

In 1D models of a tubular reactor, this dispersion is often mathematically modeled as a diffusive term. The axial dispersion coefficient for a parabolic velocity profile is:

$$
D_{ax} = D + \frac{v^{2} R^{2}}{48 D},
$$

where $D$ is the molecular diffusion coefficient, $v$ is the average velocity in the tube, and $R$ is its radius.

Modeling dispersion using a diffusion term has been criticized. An alternative approach was proposed by Westerterp et al. (*AIChE Journal*, 41 (1995) 2013–2028). In this approach, Taylor dispersion is modeled in a 1D framework as two phases with different velocities and mass transfer between them:

$$
\begin{align*}
\varepsilon_{1} \frac{\partial c_{1}}{\partial t} + \varepsilon_{1} v_{1} \frac{\partial c_{1}}{\partial z} - \varepsilon_{1} D \frac{\partial^{2} c_{1}}{\partial z^{2}} &= \frac{1}{\tau} \left( c_{2} - c_{1} \right), \\
\varepsilon_{2} \frac{\partial c_{2}}{\partial t} + \varepsilon_{2} v_{2} \frac{\partial c_{2}}{\partial z} - \varepsilon_{2} D \frac{\partial^{2} c_{2}}{\partial z^{2}} &= -\frac{1}{\tau} \left( c_{2} - c_{1} \right),
\end{align*}
$$

with:

$$
\varepsilon_{1} = 0.37493, \quad \varepsilon_{2} = 0.62507, \quad v_{1} = 1.83395 v, \quad v_{2} = 0.49978 v, \quad \tau = 0.21310 \frac{R^{2}}{D}.
$$

**Questions**:

1. Implement a 1D diffusion-convection model where the diffusion term models Taylor dispersion.

2. Implement the two-phase model of Taylor dispersion.

3. Determine the residence time distributions for the two models for a range of dimensionless Péclet numbers, $Pe = \frac{v R}{D}$, and aspect ratios $\frac{L}{R}$.

:::note  
Ensure that all numerical implementations are consistent with the provided equations and parameter values.
:::
