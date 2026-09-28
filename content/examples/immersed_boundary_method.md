# Immersed Boundary Method

These examples use the immersed boundary method (IBM) of `pymrm`: solid
particles of arbitrary shape inside a regular Cartesian grid, with boundary or
interface conditions imposed where the grid lines cross the particle surfaces.
They go from a single particle to many particles and a derived engineering
quantity.

- [Diffusion around a circle](../../pymrm/examples/ibm_diffusion.ipynb): the ghost-cell method for a single analytically described particle, two components.
- [Two touching particles](../../pymrm/examples/ibm_touching_particles.ipynb): general boundary and interface conditions at the particle surfaces.
- [Grid convergence](../../pymrm/examples/ibm_touching_convergence.ipynb): heat conduction with a contact-conductance condition and the observed order of the method.
- [Domain segmentation](../../pymrm/examples/ibm_segmentation.ipynb): assigning conditions per wall crossing with signed-distance fields.
- [Effective diffusivity](../../pymrm/examples/ibm_effective_diffusivity.ipynb): many randomly placed particles and a grid-convergence study of the effective diffusion coefficient.

The notebooks can be downloaded from
[pymrm/examples](https://github.com/computational-chemical-engineering/pymrm/tree/main/examples).
