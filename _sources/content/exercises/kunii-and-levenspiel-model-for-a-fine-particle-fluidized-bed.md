# Kunii and Levenspiel Model for a 'Fine Particle' Fluidized Bed

In reactor models of fluidized beds, we typically distinguish different phases, such as the emulsion phase and bubble phase. Depending on the flow regime, additional phases like cloud and wake may also exist. To construct the reactor model, one needs to determine the balance equations for concentrations in each phase, including mass exchange between phases.

In this exercise, we consider two phases: the emulsion phase and the bubble phase. The emulsion phase is a dense particle phase where the voidage remains close to the value at minimum fluidization conditions, $\varepsilon_{mf}$. At gas velocities above the minimum fluidization velocity, excess gas creates voids referred to as bubbles. For fluidized beds with fine particles (Geldart A), the emulsion phase has low permeability, causing excess gas to remain mostly in the bubbles. Consequently, bubbles rise faster than the gas velocity in the emulsion phase, $u_{b} > \frac{u_{mf}}{\varepsilon_{mf}}$.

In this exercise, you are tasked with modeling a catalytic fluidized bed. The particles are catalytically active, so conversion occurs in the emulsion phase, while most gas is transported by the bubbles. The balances for the concentration of gas species $i$ in the two phases, $b$ (bubble) and $e$ (emulsion), are:

$$
\begin{align*}
\delta \frac{\partial c_{b,i}}{\partial t} + \delta u_{b} \frac{\partial c_{b,i}}{\partial z} &= -\delta K_{be} \left( c_{b,i} - c_{e,i} \right), \\
(1 - \delta) \frac{\partial c_{e,i}}{\partial t} + (1 - \delta) u_{e} \frac{\partial c_{e,i}}{\partial z} &= \delta K_{be} \left( c_{b,i} - c_{e,i} \right) + (1 - \delta) r_{e,i}.
\end{align*}
$$

We assume that the bubble fraction and velocities are constant over the height. Note that if this were not the case, one should carefully consider the placement of terms inside or outside the spatial derivative. The parameter $\delta$ denotes the bubble hold-up. For a specified overall superficial gas velocity, $u_{0}$, a total balance for the volumetric flow rate gives:

$$
u_{0} = \delta u_{b} + (1 - \delta) u_{e},
$$

where $u_{b}$ and $u_{e}$ are the bubble rise velocity and the superficial gas velocity in the emulsion phase, respectively.

The reaction rate $r_{e}$ occurs only in the emulsion phase. This is an apparent reaction rate that includes potential mass-transfer resistances for transport between the emulsion gas and particles. For a first-order reaction of one species, we have:

$$
r_{e} = -K_{r} c_{e}.
$$

In this type of model, it is conventional to use volumetrically defined mass-transfer coefficients based on the bubble volume. This explains the $\delta$ appearing in front of $K_{be}$.

:::note  
The following parameter values are provided:
:::

| Quantity                          | Value                          |
|-----------------------------------|--------------------------------|
| $d_{b}$                           | $0.04~\mathrm{m}$             |
| $K_{be}$                          | $1.2~\mathrm{s^{-1}}$         |
| $K_{r}$                           | $10.0~\mathrm{s^{-1}}$        |
| $u_{0}$                           | $0.1~\mathrm{m~s^{-1}}$       |
| $u_{e} = u_{mf}$                  | $0.006~\mathrm{m~s^{-1}}$     |

In the standard text by Kunii and Levenspiel, many correlations for transport coefficients are provided. These are based on theoretical considerations mixed with empirical findings. For example, the bubble rise velocity in a fine-particle fluidized bed is given by:

$$
u_{b} = u_{0} - u_{mf} + u_{br}, \quad \text{with } u_{br} = 0.711 \sqrt{g d_{b}},
$$

where $d_{b}$ is the bubble diameter and $g$ is the gravitational constant.

**Questions**:

1. Using `pymrm` functions, implement the model for a fine-particle fluidized bed.
2. Compute the conversion as a function of height.
3. Investigate the influence of parameters $K_{r}$, $u_{0}$, and $d_{b}$.

:::note  
For larger particles (Geldart B), the emulsion phase is more permeable. Excess gas uses the bubbles as a low-resistance shortcut through the bed. In this case, the rise velocity of bubbles is lower than that of the gas in the emulsion phase.
:::
