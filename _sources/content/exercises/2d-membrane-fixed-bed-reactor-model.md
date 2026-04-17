# 2D Membrane Fixed Bed Reactor Model

In a (single tube) membrane fixed bed reactor, a heterogeneously catalyzed chemical equilibrium reaction is carried out. The reaction scheme and associated kinetics are as follows:

$$
A + B \rightleftarrows C + D,
$$

The tube wall of the fixed bed consists of a perm-selective membrane through which component $C$ selectively permeates. The associated flux expression is given by:

$$
N_{C} = k_{m} \left[ c \big|_{r = R} - c_{0} \right],
$$

where $k_{m}$ represents the effective mass transfer coefficient for intra-membrane transport, and $c_{0}$ is the concentration of component $C$ in the sweep gas in the annular zone. The concentration of species $C$ in the sweep gas, $c_{0}$, can be assumed to be zero, corresponding to a very large sweep gas flow rate.

::: {figure} ./media/fixed_bed.png
:width: 40%
:align: center
:::

The effective radial dispersion coefficient $D_{e,r}$ of all species $A$, $B$, $C$, and $D$ is $D_{e,r} = 10^{-4}~\mathrm{m^{2}~s^{-1}}$. The inlet concentrations of species $A$ and $B$ are $c_{A,\mathrm{in}} = c_{B,\mathrm{in}} = 10.0~\mathrm{mol~m^{-3}}$, while the inlet concentrations of species $C$ and $D$ are $c_{C,\mathrm{in}} = c_{D,\mathrm{in}} = 0.0~\mathrm{mol~m^{-3}}$. The reactor operates under isothermal conditions.

| Parameter                          | Value                          |
|------------------------------------|--------------------------------|
| Superficial gas velocity, $U_{0}$  | $0.2~\mathrm{m~s^{-1}}$       |
| Inner radius of fixed bed tube     | $0.02~\mathrm{m}$             |
| Length of fixed bed tube           | $1.00~\mathrm{m}$             |
| Forward kinetic constant, $k_{f}$ | $0.1~\mathrm{m^{3}~mol^{-1}~s^{-1}}$ |
| Backward kinetic constant, $k_{b}$ | $0.1~\mathrm{m^{3}~mol^{-1}~s^{-1}}$ |

**Questions**:

1. Calculate the thermodynamic equilibrium conversion.

2. Formulate the model equations and the associated boundary conditions according to the homogeneous two-dimensional reactor model. Account for the selective permeation of component $C$ through the membrane. Neglect axial dispersion effects.

3. Implement the formulated model equations in Python. It is suggested to use a method-of-lines approach where the spatial discretization is performed in the radial direction, and the axial dependence is solved using `solve_ivp`.

4. For the case of no permeation of $C$ ($k_{m} = 0.0~\mathrm{m~s^{-1}}$), calculate the chemical conversion.

5. Repeat the calculation for part 4 using $k_{m}$ values of $0.01$, $0.1$, $1.0$, $10.0$, and $100.0~\mathrm{m~s^{-1}}$ for the effective mass transfer coefficient. Explain the observed differences with respect to the chemical conversion and the obtained radial concentration profiles. Discuss the validity of the model equations for $k_{m} = 100~\mathrm{m~s^{-1}}$.

6. Repeat part 5 using an effective radial dispersion coefficient $D_{e,r} = 10^{-5}~\mathrm{m^{2}~s^{-1}}$. Discuss the observed results.

:::note  
Ensure that all numerical implementations are consistent with the provided equations and parameter values.
:::
