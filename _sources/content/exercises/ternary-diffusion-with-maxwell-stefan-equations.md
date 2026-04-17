# Ternary Diffusion with Maxwell-Stefan Equations

Consider the two-bulb diffusion experiment where bulb A contains a 50-50 molar-% $N_{2}$ and $CO_{2}$ mixture, and bulb B contains a 50-50 molar-% $N_{2}$ and $H_{2}$ mixture. The bulbs are connected by a capillary with length $\delta = 0.086~\mathrm{m}$. We will consider the diffusion of the three gases.

:::{figure} ./media/image10.png
:width: 60%
:align: left
---
Two-Bulb Diffusion Experiment
:::

Let's label the three components as 1: $H_{2}$, 2: $N_{2}$, and 3: $CO_{2}$. The binary Maxwell-Stefan diffusivities are:  
$D_{12} = 83.6 \cdot 10^{-6}~\mathrm{m^{2}~s^{-1}}$,  
$D_{13} = 68 \cdot 10^{-6}~\mathrm{m^{2}~s^{-1}}$,  
$D_{23} = 16.8 \cdot 10^{-6}~\mathrm{m^{2}~s^{-1}}$.  

The pressure and temperature are $P = 1.01 \cdot 10^{5}~\mathrm{Pa}$ and $T = 308~\mathrm{K}$, respectively.

The Maxwell-Stefan equations for the first two components can be written as:

$$
\begin{align*}
\frac{dx_{1}}{dz} &= \frac{x_{1} N_{2} - x_{2} N_{1}}{c_{tot} D_{12}} + \frac{x_{1} N_{3} - x_{3} N_{1}}{c_{tot} D_{13}}, \\
\frac{dx_{2}}{dz} &= \frac{x_{2} N_{1} - x_{1} N_{2}}{c_{tot} D_{12}} + \frac{x_{2} N_{3} - x_{3} N_{2}}{c_{tot} D_{23}}.
\end{align*}
$$

Using the constraint $x_{3} = 1 - x_{1} - x_{2}$ and the bootstrap $N_{1} + N_{2} + N_{3} = 0$, the mole fraction and molar flux of the third component can be eliminated from the set of equations.

**Questions**:

1. Implement and numerically solve the ODEs for components 1 and 2 using the boundary conditions at $z = 0$: $x_{1} = 0$ and $x_{2} = 0.5$. Use a shooting method to compute $N_{1}$ and $N_{2}$ from the boundary conditions at $z = \delta$: $x_{1} = 0.5$ and $x_{2} = 0.5$.

   :::{note}  
   In Python, you can use SciPy's `solve_ivp` to solve the ODEs and SciPy's `root` (or `newton` from `pymrm`) to obtain $N_{1}$ and $N_{2}$ such that the boundary conditions at $z = \delta$ are obeyed.  
   :::

2. Linearize the Maxwell-Stefan equations and compute the fluxes by solving the set of two linear equations.

3. Use the method of Toor, Steward, and Prober to solve the ternary Maxwell-Stefan diffusion problem.

4. Numerically solve the problem as a boundary value problem to compute the fluxes and compositions in the capillary (e.g., using the `pymrm` building blocks).

5. Consider a time-dependent problem where the concentrations in the bulbs evolve. The bulb volumes are:  
   $V_{A} = 77.99 \cdot 10^{-6}~\mathrm{m^{3}}$,  
   $V_{B} = 78.63 \cdot 10^{-6}~\mathrm{m^{3}}$.  

   The capillary has a cross-sectional area $A_{d} = 3.87 \cdot 10^{-5}~\mathrm{m^{2}}$ and length $d = 0.086~\mathrm{m}$. Assume constant pressure is maintained in the bulbs and the ideal gas law, such that $c_{tot}$ is equal and constant in time throughout the system and $N_{tot} = 0$. Assume pseudo-steady state in the capillary and use a linearization to compute the flux as a function of composition in the bulbs.
