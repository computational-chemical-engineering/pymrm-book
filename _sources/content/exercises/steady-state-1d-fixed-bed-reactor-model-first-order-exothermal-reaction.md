# Steady state 1D fixed bed reactor model: first order exothermal reaction

In a fixed bed catalyst tube of $0.5~\mathrm{m}$ long a heterogeneously catalyzed
exothermic (gas phase) chemical reaction takes place. The reaction
scheme and associated kinetics are as follows:

$$A \rightarrow B + C,\ \ \ \ \ \ \ r = k_{r}\ c_{A},\ \ \text{with}\ k_{r} = k_{0}\exp\left\lbrack - \frac{E_{a}}{RT} \right\rbrack,\ \ {- r}_{A} = r_{B} = r_{C} = r$$

where $k_{0} = 1.0 \times 10^{9}~\mathrm{s^{-1}}$, $E_{a} = 50~\mathrm{kJ \cdot mol^{-1}}$. The
reaction is exothermic with $\Delta H_{r} = 15~\mathrm{kJ \cdot mol^{-1}}$ at the reference
temperature of $293~\mathrm{K}$. The molar heat capacities of the gases equal $100,
60$ and $40~\mathrm{J \cdot (mol \cdot K)^{-1}}$, for $A$, $B$ and $C$, respectively.

Here we will model the reactor as adiabatic. (Of course the reactor
should be cooled but this will be considered in a later tutorial). The
inlet gas stream consists of pure $A$ and is at a pressure of $1~\mathrm{bar}$ and a
temperature $293~\mathrm{K}$. The interstitial inlet gas velocity $v$ equals $2.0~\mathrm{m \cdot s^{-1}}$.

**Questions**:

1.  Formulate the stationary convection-reaction equations for species
    $A$, $B$ and $C$ as well as for the temperature assuming a constant
    gas velocity.

2.  Solve the set of ordinary differential equations assuming constant
    gas velocity using a standard Python IVP solver.

3.  Formulate the stationary convection-reaction equations for species
    $A$, $B$ and $C$ as well as for the temperature assuming a constant
    pressure throughout the reactor. Hint: be cautious about placing the
    velocity inside or outside of the spatial derivative.

4.  Solve this set of ordinary differential equations assuming constant
    pressure using a standard Python IVP solver.

5.  Are the results according to your expectations? Is the temperature
    increase consistent with the adiabatic temperature rise? Is the
    increase in velocity in accordance with expectations?

6.  Try solving both sets of ODE's using your own Euler backward solver.
