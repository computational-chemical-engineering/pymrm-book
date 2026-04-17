# Computing Residence Time Distributions

An important characterization of flow patterns and mixing characteristics in a chemical reactor is the residence time distribution. The cumulative residence time distribution, $F(t)$, can be obtained by measuring the total flow of a non-reactive tracer component at the outlet, starting with an empty reactor at $t = 0$ and supplying a constant inlet tracer flux.

**Questions**:

1. Write a routine to output the total outlet flux for a multiphase model.

2. Implement the 1D, 1-component unsteady convection-dispersion equation. Use the Danckwerts boundary condition for inflow and the Neumann boundary condition at outflow. Implement the dispersive term implicitly. For the convective term, you can choose implicit, explicit, or upwind with or without TVD.

3. Investigate the cumulative residence time distribution produced by this model using the written routine. Supply a concentration step at the input and measure the fluxes that leave the reactor. Plot the flux that leaves the reactor as a function of time, properly normalized to obtain the cumulative residence time distribution, $F(t)$.

   The analytical solution, for not too large axial dispersion, is given by:

   $$
   F(t) = \frac{1}{2} \mathrm{erfc}\left( \frac{L - v t}{2\sqrt{D_{ax} t}} \right)
   $$

   For very large axial diffusion, $D_{ax} \to \infty$, the behavior should be CISTR, and you have:

   $$
   F(t) = 1 - \exp\left( -\frac{v t}{L} \right)
   $$

   Compare numerical results with the analytical solution. Investigate both physical and numerical aspects (e.g., time step and grid size dependencies).

4. Model a system with a moving and stagnant phase that exchange mass. In the moving phase, both convection and dispersion take place. One example is a trickle bed where liquid trickles down, but some liquid close to the packing is stagnant due to capillary forces. Investigate the effect on the residence time distribution due to mass transfer to and from the stagnant liquid.

5. Use the routine to determine the residence time distribution for multiphase reactor models.
