# Steady-state 2D fixed bed reactor model: first order exothermal reaction

This is the 2D version of exercise 1.3. In a fixed-bed catalyst-tube of
0.5 m long a heterogeneously catalyzed exothermic (gas phase) chemical
reaction takes place. The reaction scheme and associated kinetics are as
follows:

$$A \rightarrow B + C,\ \ \ \ \ \ \ r = k_{r}\ c_{A},\ \ with\ k_{r} = k_{0}\exp\left\lbrack - \frac{E_{a}}{RT} \right\rbrack,\ \ {- r}_{A} = r_{B} = r_{C} = r$$

where $k_{0} = 1.0 \times 10^{9}\ s^{- 1}$, *E~a~*=50 kJ/mol. The
reaction is exothermic with --∆H~r~=15 kJ/mol at the reference
temperature of 293 K. The molar heat capacities of the gases equal 100,
60 and 40 J/(mol K), for $A$, $B$ and $C$, respectively. The (constant)
inlet gas stream consists of pure A and is at a pressure of 1 bar and a
temperature 293 K. The (constant and uniform) interstitial inlet gas
velocity $v$ equals 2.0 m/s.

Here we will model the reactor in a 2D fashion. The radius of the
tubular reactor is 0.01 m. The reaction is highly exothermic and
therefore the catalyst bed needs to be cooled at the wall of the tube.
The imposed wall temperature equals 293.0 K. Effective thermal
conduction and dispersion are modelled in the radial direction with
values $\lambda_{e,r} = 0.1\ W/(m \cdot K)$ and
$D_{e,r} = 10^{- 3}\ m^{2}/s$, respectively.

**Questions**:

1.  Make a 2D Python reactor model. Note that, because dispersion
    effects in the axial directions can be neglected, you can use the
    methods of lines by performing the discretization in the spatial
    direction and get a set of coupled ODE's in the axial direction.

2.  Calculate the adiabatic temperature rise.

3.  Compute the (radially averaged) axial concentration and temperature
    profiles. Compare the results with the 1D profiles.

4.  Compute the exit concentration and temperature profiles. Explain the
    observed radial temperature profile and explain how the maximum
    temperature can exceed the inlet temperature augmented with the
    adiabatic temperature rise.
