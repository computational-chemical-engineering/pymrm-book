# Multicomponent convection-reaction with first-order chemical kinetics

In this exercise we will consider the unsteady convection-reaction
equation for three components:

$$\frac{\partial c_{i}}{\partial t} + v\ \frac{\partial c_{i}}{\partial x} = r_{i},$$

where the index $i$ refers to one of the 3 components $A$, $B$ or $C$. All
species move with the (same constant) velocity. The same kinetics as in
exercise 1.2 will be used:

$$A \rightleftarrows B \rightarrow C$$

For unsteady convection-reaction consider a first order temporal
discretization where the convection term is evaluated explicitly (using
e.g. a TVD scheme) and the reaction term implicitly:

$$\frac{\mathbf{c}_{j}^{n + 1} - \mathbf{c}_{j}^{n}}{\Delta t} = \mathbf{f}_{conv,j}^{n} + \mathbf{r}_{j}^{n + 1}$$

Here the bold-vector notation is used to indicate column vectors of 3
long where the 3 elements correspond to the 3 species. The subscript $j$
indicates the spatial cell and the superscript $n$ the time step.

**Questions**:

1.  Implement the unsteady convection-reaction equations.

Suggested approach:

-   Use a two dimensional array $c[i,j]$ where the first index, $i=0,...,
    N-1$, refers to the spatial positions and the second one, $i=0,1$ and $2$
    , the index of the species.

-   Compute the convection term using the concentration on the old
    time-step

-   Next loop over all grid cells $j=1...N$ and in each cell solve (with
    $\mathbf{r} = \mathbf{J\ c}$):

$$\frac{\mathbf{c}_{j}^{n + 1} - \mathbf{c}_{j}^{n}}{\Delta t} = \mathbf{f}_{conv,j}^{n} + \mathbf{J}\mathbf{c}_{j}^{n + 1} \rightarrow \ \left( \mathbf{I -}\mathbf{J}\Delta t \right)\ \mathbf{c}_{j}^{n + 1} = \mathbf{c}_{j}^{n} + \mathbf{f}_{conv,j}^{n}\ \Delta t$$

-   Please, notice how close this is to the problem solved in the second
    part of exercise 1.2b). Reuse the part of your code developed there.

2.  Perform simulations using the same kinetics as in exercise 1.2.
    Consider an initially empty column of length $L = 1~\mathrm{m}$. At the
    inlet feed pure $A$ with $c_{A,in} = 1~\mathrm{mol\cdot m^{-3}}$. Vary the
    residence time by changing the velocity $v$.

3.  Plot concentration profiles in the column for the three species at
    different times.
