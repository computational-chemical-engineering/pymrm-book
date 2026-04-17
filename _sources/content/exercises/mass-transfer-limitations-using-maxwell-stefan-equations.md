# Mass Transfer Limitations Using Maxwell-Stefan Equations

We consider the same exothermal catalytic fixed bed 1D column process as in previous Exercise 1.3. In this exercise, you will investigate the influence of external mass transfer limitations.

In a fixed bed catalyst tube of length $L = 0.5~\mathrm{m}$, the following exothermal reaction takes place in catalytic particles:

$$
A \rightarrow B + C, \quad r = k_{r} c_{A}, \quad k_{r} = k_{0} \exp\left[ - \frac{E_{a}}{RT} \right], \quad -r_{A} = r_{B} = r_{C} = r,
$$

where $k_{0} = 1.0 \cdot 10^{9}~\mathrm{s^{-1}}$, $E_{a} = 50~\mathrm{kJ~mol^{-1}}$. The reaction is exothermic with $-\Delta H_{r} = 15~\mathrm{kJ~mol^{-1}}$ at the reference temperature of $293~\mathrm{K}$. The molar heat capacities of the gases are $100$, $60$, and $40~\mathrm{J~mol^{-1}~K^{-1}}$ for $A$, $B$, and $C$, respectively. The reactor operates adiabatically. The inlet gas stream consists of pure $A$ and is at a pressure of $1~\mathrm{bar}$ and a temperature of $293~\mathrm{K}$. The interstitial inlet gas velocity $v$ equals $2.0~\mathrm{m~s^{-1}}$.

In earlier exercises, the effect of external mass transfer limitations from the gas bulk to the active sites on the catalyst surface was neglected, allowing for a homogeneous reaction rate source term if intra-particle resistances were also small. Now, let's assume that the catalyst particles are spherical with a uniform diameter of $3.0~\mathrm{mm}$ (bed porosity of $0.4$), and that the mass transfer coefficients are:  
$k_{AB} = 0.005~\mathrm{m~s^{-1}}$, $k_{BC} = k_{AC} = 0.020~\mathrm{m~s^{-1}}$.  
These coefficients are assumed to be independent of the operating conditions (simplification).

:::{note}  
- In this exercises, we considered three species only, i.e., there is no fourth inert species. Note that because the reaction is non-equimolar, this would mean in practice that the superficial velocity increases along the reactor length. This effect is neglected in this exercise.

- Note that there is ambiguity in the different exercises on the exact definition of the reaction rate, i.e., is it per $\mathrm{m^{3}}$ of reactor, solid, or fluid? For the purpose of the current exercise, make a convenient choice and ensure your equations are consistent with this choice. When evaluating the influence of mass transfer resistances, compare similar situations, i.e., with the same definitions of the reaction rate.
:::

**Questions**:

1. Show with a simple estimation whether external mass transfer limitations could be important and should be included in the computations.

2. Formulate the (simplified) equations to account for external mass transfer limitations using the Maxwell-Stefan approach. Make the assumption of linearization of the concentration profiles.

3. Implement the formulated heterogeneous model to account for external mass transfer limitations using the linearized Maxwell-Stefan equations and calculate the axial profiles of the reactant concentration and bed temperature. Assume there are no internal mass transfer limitations.

   :::note  
   For each species, there are now two types of concentrations, namely the concentrations in the bulk of the fluid and the fluid concentrations at the particle surface. There are two approaches to introduce these surface concentrations:  
   1. Only consider these in the reaction term of the column model and eliminate these from the set of equations, such that it returns the apparent reaction rate as a function of the bulk fluid concentrations only.  
   2. Extend the number of variables of unknowns in the column model with the surface concentrations. Solve the set of equations for the full set of variables simultaneously. The equations for the surface concentrations are algebraic.  
   Choose one of the approaches and at the end of the exercise, return and attempt the other one.  
   :::

4. Verify that the profiles coincide with the results obtained with the homogeneous reaction rate expressions in case the mass transfer coefficients are increased a thousandfold. Compare the axial profiles of the reactant concentration with and without mass transfer limitations and explain the observed differences.

5. **Advanced**: Formulate the equations to adequately account for external mass transfer limitations using the Maxwell-Stefan approach. Assume that the ideal gas law is valid and use the (exact) matrix method.

6. **Advanced**: Implement the formulated heterogeneous model with the Maxwell-Stefan equations using the exact matrix method. Compare the results with the linearized solutions.

7. **Advanced (optional)**: Combine the (linearized) Maxwell-Stefan model with the particle-model implementation.
