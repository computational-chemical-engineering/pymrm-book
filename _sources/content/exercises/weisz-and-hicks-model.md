# Weisz and Hicks model

This exercise considers diffusion and reaction in a spherical particle for first-order kinetics. The reaction rate is temperature-dependent via an Arrhenius dependence.

$$
\begin{align*}
\frac{\partial c}{\partial t} &= \frac{1}{r^{2}}\frac{\partial}{\partial r}\left( r^{2}D_{e}\frac{\partial c}{\partial r} \right) + r = \mathrm{div}\left( D_{e}\ \mathrm{grad}(c) \right) + r, \\
r &= - k_{0}\exp\left[ \frac{E_{a}}{R_{G}}\left( \frac{1}{T_{f}} - \frac{1}{T} \right) \right] c, \\
\rho C_{p}\frac{\partial T}{\partial t} &= \frac{1}{r^{2}}\frac{\partial}{\partial r}\left( r^{2}\lambda_{S}\frac{\partial T}{\partial r} \right) + r\ \Delta H_{r} = \mathrm{div}\left( \lambda_{S}\ \mathrm{grad}(T) \right) + r\ \Delta H_{r}.
\end{align*}
$$

Assume Dirichlet boundary conditions for both concentration and temperature on the particle surface.

**Questions**:

1. Formulate the model in a dimensionless way by introducing characteristic numbers $\varphi$, $\beta$, and $\gamma$. The Thiele modulus is defined as $\varphi = R\sqrt{\frac{k_{0}}{D_{e}}}$, $\beta = \frac{c_{f}(-\Delta H_{r})D_{e}}{T_{f}\lambda_{S}}$ (ratio of heat generation to transport), and $\gamma = \frac{E}{R_{G}T_{f}}$ (ratio of activation to thermal energy).

2. Provide a backward Euler Python implementation of both the diffusion and temperature equations.

3. Can you reproduce the case of effectiveness, $\eta > 1$, for a specific choice of $\beta$, $\gamma$, and $\varphi$?

::: {hint}
Use a small enough time step to avoid stability issues. Based on the profiles you find, explain what causes the efficiency to be larger than 1.
:::

::: {figure} ./media/image1.png
:width: 80%
:align: center
:::

Source: *Chem. Engin. Sc.*, 1962, Vol. 17, pp. 265-275
