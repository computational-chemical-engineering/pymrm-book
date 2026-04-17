# Multicomponent convection-reaction with general chemical kinetics

Consider the same governing equations as in 2.2 but now for general
multicomponent kinetics (non first-order). When the convection term is
taken explicitly in time values of $\mathbf{f}_{conv,j}^{n}$ can be
computed from the concentration values of the previous time step, $n$.
With the reaction term implicit, we have in each cell $j$ the implicit
equation

$$\frac{\mathbf{c}_{j}^{n + 1} - \mathbf{c}_{j}^{n}}{\Delta t} = \mathbf{f}_{conv,j}^{n} + \mathbf{r}_{j}^{n + 1}$$

So, for the new concentrations in each cell, $\mathbf{c}_{j}^{n + 1},$ a
root-seeking problem needs to be solved:

$$\mathbf{g}\left( \mathbf{c} \right)\mathbf{=}\frac{\mathbf{c} - \mathbf{c}_{j}^{n}}{\Delta t} - \mathbf{r}_{j}\left( \mathbf{c} \right) - \mathbf{f}_{conv,j}^{n} = \mathbf{0} \rightarrow \ \mathbf{c}_{j}^{n + 1} ≔ \mathbf{c}$$

To solve the root-seeking problem, you can use the SciPy method
optimize.root, or the newton method from pymrm. For the newton function
you need to supply the Jacobian (by means of a function argument that
returns $\mathbf{g}$ and its Jacobian). You can use the function
numjac_local from pymrm to compute the Jacobian. (For optimize.root the
Jacobian is optional and needs to be full, while in pymrm we use mostly
sparse matrices.)

**Questions**:

1. Repeat the case of exercise 2.2 with this general method. Does it
    give the same results?

2. Implement a system non-linear reactions. For example:

$$
\begin{align*}
A &\rightarrow X \\
2X + Y &\rightarrow 3X \\
B + X &\rightarrow Y + D \\
X &\rightarrow E
\end{align*}
$$

This is the famous Brusselator (see
[Wikipedia](https://en.wikipedia.org/wiki/Brusselator)). Here components
$A$ and $B$ are present in access and thus constant. The kinetics is
usually written down in a dimensionless form with all reaction
coefficient equal to 1. Suggested inlet concentrations are: $c_{A} = 1$,
$c_{B} = 1.7$, $c_{X} = 0$, $c_{Y} = 0$ and for case two: $c_{A} = 1$,
$c_{B} = 3$, $c_{X} = 0$, $c_{Y} = 0$.
