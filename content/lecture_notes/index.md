# Lecture Notes

These notes accompany the **Multiphase Reactor Modeling (MRM)** course (6EMA05) at TU Eindhoven. This is a preview version auto-generated using Claude Code. It is no replacement for the MRM slide deck.
Each chapter corresponds to one or more lectures and provides:

- concise derivation of the governing equations,
- a table of the relevant pymrm building blocks,
- minimal working code examples with inline figures, and
- a summary of key takeaways.

The four reactor-type chapters describe the phase structure, closure correlations,
and pymrm modeling strategy for important industrial reactor classes.

## Lecture chapters

| Chapter | Topic |
|---|---|
| [L1: ODE Solving](L1_ode_reactor_modeling.ipynb) | Batch/PFR models, solve_ivp, Euler methods, Newton–Raphson |
| [L2: Convection-Reaction](L2_convection_reaction.ipynb) | Method of lines, FOU, TVD limiters, CFL condition |
| [L3: Diffusion-Reaction](L3_diffusion_reaction.ipynb) | Grad/div operators, BCs, steady-state BVP, Newton solver |
| [L4: Dispersion & Mass Transfer](L4_dispersion_mass_transfer.ipynb) | Axial dispersion, RTD, Wakao-Funazkri, heterogeneous bed |
| [L5: 2D Reactor Models](L5_2d_reactor_models.ipynb) | Kronecker assembly, cylindrical geometry, pellet model |
| [L6–7: Maxwell-Stefan](L67_maxwell_stefan.ipynb) | GMS equations, B-matrix, osmotic/reverse diffusion |
| [L8: Advanced Modeling](L8_advanced_modeling.ipynb) | Multi-scale coupling, Darcy flow, Schur complement |

## Reactor-type chapters

| Chapter | Reactor | Key correlations |
|---|---|---|
| [Packed Bed](reactor_packed_bed.ipynb) | Fixed catalyst bed | Ergun, Edwards-Richardson, Wakao-Funazkri |
| [Fluidized Bed](reactor_fluidized_bed.ipynb) | Gas-solid fluidized bed | Kunii-Levenspiel, Werther |
| [Slurry Bubble Column](reactor_slurry_bubble_column.ipynb) | G-L-S three-phase | Krishna holdup, $k_L a$ correlations |
| [GLS Packed Bed](reactor_gls_packed_bed.ipynb) | Trickle-bed reactor | Larkins $\Delta P$, Lara-Marquez $k_L a$ |
