# Reactor Model for Heterogeneous Bubble Columns

In this exercise, you are tasked with modeling mass transfer in a slurry bubble column as proposed by Maretto and Krishna (*Catalysis Today*, 52 (1999) 279-289). The column is described by three phases: two bubble phases (large and small) and a slurry phase. Large bubbles transport gas in a plug flow manner, while small bubbles exhibit a more turbulent flow pattern, modeled as well-mixed. Gas can dissolve from the bubble phases into the slurry phase, which consists of liquid with suspended catalyst particles. Catalytic conversion occurs within the particles.

::: {figure} ./media/image2.svg
:width: 40%
:align: center
:::

The balances for the phases, where subscript $b$ refers to large bubbles, $df$ to small bubbles, and $s$ to the slurry, are given as:

$$
\begin{align*}
\varepsilon_{b} \frac{\partial c_{b,i}}{\partial t} + \frac{\partial}{\partial z} \left( U_{b} c_{b,i} - \varepsilon_{b} E_{b} \frac{\partial c_{b,i}}{\partial z} \right) &= - \left( k_{l} a \right)_{b,i} \left( \frac{c_{b,i}}{m_{i}} - c_{sl,i} \right), \\
\left( 1 - \varepsilon_{b} \right) \varepsilon_{df} \frac{\partial c_{df,i}}{\partial t} + \frac{\partial}{\partial z} \left( U_{df} c_{df,i} - \left( 1 - \varepsilon_{b} \right) \varepsilon_{df} E_{df} \frac{\partial c_{df,i}}{\partial z} \right) &= - \left( k_{l} a \right)_{df,i} \left( \frac{c_{df,i}}{m_{i}} - c_{sl,i} \right), \\
\left( 1 - \varepsilon_{b} \right) \left( 1 - \varepsilon_{df} \right) \frac{\partial c_{sl,i}}{\partial t} + \frac{\partial}{\partial z} \left( - \left( 1 - \varepsilon_{b} \right) \left( 1 - \varepsilon_{df} \right) E_{s} \frac{\partial c_{sl,i}}{\partial z} \right) &= \left( k_{l} a \right)_{b,i} \left( \frac{c_{b,i}}{m_{i}} - c_{sl,i} \right) \\
&\quad + \left( k_{l} a \right)_{df,i} \left( \frac{c_{df,i}}{m_{i}} - c_{sl,i} \right) \\
&\quad + \left( 1 - \varepsilon_{b} \right) \left( 1 - \varepsilon_{df} \right) \varepsilon_{s} r_{i}.
\end{align*}
$$

Although only the steady state is of interest, solving the equations time-dependently might help in finding this steady state. The dispersion coefficients are numerical parameters, as we are interested in their limiting values. The large bubble phase is modeled as plug flow, so $E_{b} = 0$. For the small bubble and slurry phases, a well-mixed state is assumed. This can be achieved by choosing $E_{df}$ and $E_{s}$ sufficiently large. However, excessively large values may cause numerical issues, and the optimal choice can be determined through trial and error.

In the work of Maretto and Krishna, the Fischer-Tropsch reaction is considered, where CO and $H_{2}$ react with the catalyst particles in the slurry to form hydrocarbons. Hold-ups, superficial velocities, and mass transfer coefficients are derived from correlations. Here, the focus is on implementing the model and investigating its behavior depending on the primary resistance to mass transfer.

**Questions**:

1. Implement the slurry bubble column model for one inert tracer species.

   :::note  
   Use the following parameter values:
   :::

   | Quantity                  | Large Bubble ($b$)         | Small Bubble ($df$)       | Slurry ($s$)            |
   |---------------------------|----------------------------|---------------------------|-------------------------|
   | Holdup                    | $\varepsilon_{b} = 0.096$ | $\varepsilon_{df} = 0.135$ | $\varepsilon_{s} = 0.30$ |
   | Superficial Velocity      | $U_{b} = 0.255~\mathrm{m~s^{-1}}$ | $U_{df} = 0.045~\mathrm{m~s^{-1}}$ | $0~\mathrm{m~s^{-1}}$ |
   | Mass Transfer Coefficient | $\left( k_{l} a \right)_{b} = 0.2~\mathrm{s^{-1}}$ | $\left( k_{l} a \right)_{df} = 1.2~\mathrm{s^{-1}}$ | - |

2. Determine the cumulative residence time distribution for a tracer species introduced in the gas phase. Assume $m = 3$ for the distribution coefficient and vary the column height up to $30~\mathrm{m}$.

3. Assume the species is reactive and undergoes a first-order reaction at the catalyst particles. Perform a parameter study for the reaction rate coefficient $k$ of the first-order reaction.

