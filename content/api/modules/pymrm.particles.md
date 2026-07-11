# `pymrm.particles`

[Back to modules overview](../api)

Particle-based immersed boundaries for `pymrm`.

Instead of sampling one global signed-distance field, an assembly of
`Particle` objects generates the immersed-boundary data directly:
each particle classifies the cells it covers (bounding-box window only),
provides the *exact* wall position on every cut face (analytic where the
shape allows it, root-finding otherwise), and evaluates the *exact* outward
normal at every wall crossing.  This avoids the two error sources of the
union-SDF route near particle contacts:

* the union ``min_i(level_i)`` has a gradient kink on the contact medial
  axis, degrading SDF-gradient normals to O(1) locally (observed to reduce
  the flux/conjugate IBM from 2nd to ~1st order for touching particles);
* the fractional wall position ``theta`` interpolated from the union is
  polluted when the ghost cell's union value comes from a *different*
  particle.

## Particle protocol

A particle answers three geometric questions, all in world coordinates:

* `Particle.level` — signed level function (< 0 inside, > 0 outside;
  approximately a distance near the surface),
* `Particle.intersect` — surface crossing on a straight segment whose
  endpoints straddle the surface,
* `Particle.normal` — outward (solid → fluid) unit normal at surface
  points.

The base class supplies world↔body transforms (``position`` plus an
``orientation``: an angle in 2-D, a `scipy.spatial.transform.Rotation`
in 3-D) and numeric defaults for ``intersect`` (vectorised bisection) and
``normal`` (finite differences), so a new shape only has to implement the
body-frame level function and bounding box.  `Sphere` (alias
`Circle`), `Box`, `AnalyticParticle` and
`GridParticle` (B-spline interpolated local samples) are provided.

## Contact policy

When two particles are closer than one grid cell, the cell-centre
classification alone cannot see the gap: two adjacent cells are solid but
belong to *different* particles.  ``construct_ibm_particles`` detects these
*contact faces* (the segment between the two cell centres leaves one particle
before entering the other) and applies a policy:

* ``"no_flux"`` (default): a contact crossing is created with each side's
  Lagrange reconstruction anchored at its *own* particle surface; impose a
  Neumann–Neumann interface condition on these crossings (see
  `contact_conditions`) so there is no direct transport between the
  particles.
* ``"merge"``: no crossing is created; the particles are numerically
  connected (the union-SDF behaviour).
* ``"error"``: raise, for setups where contact indicates a bug.

Faces where the particles genuinely overlap (the segment does not leave one
particle before entering the other) are always merged — interpenetrating
particles form one body.

## Usage

::

    particles = [Sphere(c, r) for c, r in zip(centers, radii)]
    ibm, info = construct_ibm_particles(particles, x_c)
    recon = construct_ibm_normal_derivative(ibm, info.pseudo_sdf, x_c,
                                         normals=info.normals)
    ic = contact_conditions(base_ic, ibm, info)
    A, g = apply_ibm_interface(L, ibm, recon, ic)

[View module source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py)

## Public API

| Symbol | Type | Summary |
| ------ | ---- | ------- |
| [`AnalyticParticle`](../symbols/pymrm.particles.AnalyticParticle) | class | Particle from a user-supplied body-frame level function. |
| [`Box`](../symbols/pymrm.particles.Box) | class | Axis-aligned (in body frame) box; rotate via ``orientation``. |
| [`GridParticle`](../symbols/pymrm.particles.GridParticle) | class | Particle from level-function samples on its own body-frame grid. |
| [`Particle`](../symbols/pymrm.particles.Particle) | class | Abstract particle: a shape at a position with an orientation. |
| [`ParticleIBMInfo`](../symbols/pymrm.particles.ParticleIBMInfo) | class | Side-car information produced by `construct_ibm_particles`. |
| [`Sphere`](../symbols/pymrm.particles.Sphere) | class | Sphere (any dimension; in 2-D this is a disk — see `Circle`). |
| [`construct_ibm_particles`](../symbols/pymrm.particles.construct_ibm_particles) | function | Build immersed-boundary data directly from a particle assembly. |
| [`contact_conditions`](../symbols/pymrm.particles.contact_conditions) | function | Per-crossing ic: *base_ic* everywhere, a contact condition on contacts. |

## `AnalyticParticle(level_func, bounding_box, position, orientation = None, normal_func = None)`

[Open dedicated reference page](../symbols/pymrm.particles.AnalyticParticle)

Particle from a user-supplied body-frame level function.

### Parameters

- `level_func` (*callable*)
  ``level_func(coords) -> values`` with ``coords`` shaped (..., ndim);
  negative inside, positive outside, approximately a distance near the
  surface.

- `bounding_box` (*tuple of (lo, hi)*)
  Body-frame box containing the particle surface.

- `position, orientation` (*see `Particle`.*)

- `normal_func` (*callable, optional*)
  Body-frame outward normal direction (need not be normalised);
  default: finite differences of *level_func*.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L312-L347)

## Members

### `__init__(level_func, bounding_box, position, orientation = None, normal_func = None)`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L329-L336)

### `bounding_box(pad = 0.0)`

World axis-aligned bounding box ``((lo, hi), ...)`` per axis.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L208-L214)

### `bounding_box_body()`

Body-frame bounding box ``((lo, hi), ...)`` per axis.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L346-L347)

### `intersect(p0, p1)`

Surface crossing fraction ``t`` on the segments ``p0 → p1``.

``p0``/``p1`` are ``(n, ndim)`` batches whose endpoints straddle the
surface (``level(p0)`` and ``level(p1)`` of opposite sign); returns
``t in (0, 1)`` with ``level(p0 + t (p1 - p0)) == 0``.  Default:
vectorised bisection on `level`; shapes with closed-form
intersections override this.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L216-L238)

### `level(coords)`

Signed level function at world ``coords`` shaped (..., ndim).

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L199-L201)

### `level_body(coords)`

Signed level function at body-frame ``coords`` shaped (..., ndim).

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L338-L339)

### `normal(coords)`

Outward (solid→fluid) unit normal at world surface points.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L203-L206)

### `normal_body(coords)`

Gradient direction of `level_body` (finite differences).

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L341-L344)

### `to_body(coords)`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L190-L192)

### `vec_to_world(vecs)`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L194-L195)

### `__slots__`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L188-L188)

## `Box(position, half_extents, orientation = None)`

[Open dedicated reference page](../symbols/pymrm.particles.Box)

Axis-aligned (in body frame) box; rotate via ``orientation``.

``half_extents`` are the half side lengths per axis.  Exact SDF and
face normals; segment intersections by the default bisection.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L280-L309)

## Members

### `__init__(position, half_extents, orientation = None)`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L287-L291)

### `bounding_box(pad = 0.0)`

World axis-aligned bounding box ``((lo, hi), ...)`` per axis.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L208-L214)

### `bounding_box_body()`

Body-frame bounding box ``((lo, hi), ...)`` per axis.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L308-L309)

### `intersect(p0, p1)`

Surface crossing fraction ``t`` on the segments ``p0 → p1``.

``p0``/``p1`` are ``(n, ndim)`` batches whose endpoints straddle the
surface (``level(p0)`` and ``level(p1)`` of opposite sign); returns
``t in (0, 1)`` with ``level(p0 + t (p1 - p0)) == 0``.  Default:
vectorised bisection on `level`; shapes with closed-form
intersections override this.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L216-L238)

### `level(coords)`

Signed level function at world ``coords`` shaped (..., ndim).

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L199-L201)

### `level_body(coords)`

Signed level function at body-frame ``coords`` shaped (..., ndim).

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L293-L297)

### `normal(coords)`

Outward (solid→fluid) unit normal at world surface points.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L203-L206)

### `normal_body(coords)`

Gradient direction of `level_body` (finite differences).

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L299-L306)

### `to_body(coords)`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L190-L192)

### `vec_to_world(vecs)`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L194-L195)

### `__slots__`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L188-L188)

## `GridParticle(values, x_local, position, orientation = None, method = 'cubic')`

[Open dedicated reference page](../symbols/pymrm.particles.GridParticle)

Particle from level-function samples on its own body-frame grid.

The samples are interpolated with a cubic B-spline
(`scipy.interpolate.RegularGridInterpolator`), so the particle can
be translated and rotated for free.  The local grid **must extend beyond
the particle surface** (positive samples all around); queries outside the
local grid return the clamped boundary value plus the clamping distance,
keeping the sign correct far away.

### Parameters

- `values` (*ndarray*)
  Level-function samples, negative inside.

- `x_local` (*list of 1-D arrays*)
  Body-frame cell coordinates of the sample grid, one per axis.

- `position, orientation` (*see `Particle`.*)

- `method` (*str, optional*)
  Interpolation method (default ``"cubic"``).

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L350-L403)

## Members

### `__init__(values, x_local, position, orientation = None, method = 'cubic')`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L371-L384)

### `bounding_box(pad = 0.0)`

World axis-aligned bounding box ``((lo, hi), ...)`` per axis.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L208-L214)

### `bounding_box_body()`

Body-frame bounding box ``((lo, hi), ...)`` per axis.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L402-L403)

### `intersect(p0, p1)`

Surface crossing fraction ``t`` on the segments ``p0 → p1``.

``p0``/``p1`` are ``(n, ndim)`` batches whose endpoints straddle the
surface (``level(p0)`` and ``level(p1)`` of opposite sign); returns
``t in (0, 1)`` with ``level(p0 + t (p1 - p0)) == 0``.  Default:
vectorised bisection on `level`; shapes with closed-form
intersections override this.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L216-L238)

### `level(coords)`

Signed level function at world ``coords`` shaped (..., ndim).

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L199-L201)

### `level_body(coords)`

Signed level function at body-frame ``coords`` shaped (..., ndim).

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L386-L390)

### `normal(coords)`

Outward (solid→fluid) unit normal at world surface points.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L203-L206)

### `normal_body(coords)`

Gradient direction of `level_body` (finite differences).

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L392-L400)

### `to_body(coords)`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L190-L192)

### `vec_to_world(vecs)`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L194-L195)

### `__slots__`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L188-L188)

## `Particle(position, orientation = None)`

[Open dedicated reference page](../symbols/pymrm.particles.Particle)

Abstract particle: a shape at a position with an orientation.

Subclasses implement the **body-frame** interface
(`level_body`, `bounding_box_body`, optionally
`normal_body`); the world-frame API used by the IBM assembly
(`level`, `normal`, `intersect`,
`bounding_box`) is provided here, including the numeric fallbacks.

### Parameters

- `position` (*array_like, shape (ndim,)*)
  World position of the particle (body-frame origin).

- `orientation` (*optional*)
  ``None`` (default), an angle in radians (2-D), a
  `scipy.spatial.transform.Rotation` (3-D), or an explicit
  rotation matrix.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L140-L238)

## Members

### `__init__(position, orientation = None)`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L159-L165)

### `bounding_box(pad = 0.0)`

World axis-aligned bounding box ``((lo, hi), ...)`` per axis.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L208-L214)

### `bounding_box_body()`

Body-frame bounding box ``((lo, hi), ...)`` per axis.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L174-L175)

### `intersect(p0, p1)`

Surface crossing fraction ``t`` on the segments ``p0 → p1``.

``p0``/``p1`` are ``(n, ndim)`` batches whose endpoints straddle the
surface (``level(p0)`` and ``level(p1)`` of opposite sign); returns
``t in (0, 1)`` with ``level(p0 + t (p1 - p0)) == 0``.  Default:
vectorised bisection on `level`; shapes with closed-form
intersections override this.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L216-L238)

### `level(coords)`

Signed level function at world ``coords`` shaped (..., ndim).

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L199-L201)

### `level_body(coords)`

Signed level function at body-frame ``coords`` shaped (..., ndim).

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L170-L171)

### `normal(coords)`

Outward (solid→fluid) unit normal at world surface points.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L203-L206)

### `normal_body(coords)`

Gradient direction of `level_body` (finite differences).

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L177-L186)

### `to_body(coords)`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L190-L192)

### `vec_to_world(vecs)`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L194-L195)

### `__slots__`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L188-L188)

## `ParticleIBMInfo()`

[Open dedicated reference page](../symbols/pymrm.particles.ParticleIBMInfo)

Side-car information produced by `construct_ibm_particles`.

### Attributes

- `owner` (*ndarray of int*)
  Per spatial cell, index of the owning particle (deepest level
  function) or ``-1`` for fluid.  Shaped like the spatial grid.

- `crossing_particle` (*ndarray of int, shape (n_crossings,)*)
  Owning particle of the solid (``in``) side of each crossing.

- `contact` (*ndarray of bool, shape (n_crossings,)*)
  True for contact crossings (solid–solid faces between two particles
  under the ``"no_flux"`` policy).  For these,
  ``crossing_particle`` is the ``in``-side particle and
  ``contact_partner`` the ``out``-side one.

- `contact_partner` (*ndarray of int, shape (n_crossings,)*)
  The ``out``-side particle of a contact crossing, ``-1`` elsewhere.

- `normals` (*ndarray, shape (n_crossings, ndim)*)
  Exact outward (solid→fluid) unit normals from the owning particle —
  pass to ``construct_ibm_normal_derivative(..., normals=...)``.  For
  contact crossings: the ``in``-side particle's outward normal.

- `pseudo_sdf` (*ndarray*)
  Sign-correct union level field on the spatial grid (positive filler
  far from every particle) for region classification in the
  reconstruction.

- `segmentation` (*Segmentation*)
  Per-particle labels (``owner + 1``) — valid even at exact contact,
  where `pymrm.segment_domain` would merge the bodies.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L411-L447)

## Members

### `contact`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L443-L443)

### `contact_partner`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L444-L444)

### `crossing_particle`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L442-L442)

### `normals`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L445-L445)

### `owner`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L441-L441)

### `pseudo_sdf`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L446-L446)

### `segmentation`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L447-L447)

## `Sphere(center, radius)`

[Open dedicated reference page](../symbols/pymrm.particles.Sphere)

Sphere (any dimension; in 2-D this is a disk — see `Circle`).

Fully analytic: exact level function, normals, and segment intersections.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L241-L274)

## Members

### `__init__(center, radius)`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L247-L249)

### `bounding_box(pad = 0.0)`

World axis-aligned bounding box ``((lo, hi), ...)`` per axis.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L208-L214)

### `bounding_box_body()`

Body-frame bounding box ``((lo, hi), ...)`` per axis.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L257-L259)

### `intersect(p0, p1)`

Surface crossing fraction ``t`` on the segments ``p0 → p1``.

``p0``/``p1`` are ``(n, ndim)`` batches whose endpoints straddle the
surface (``level(p0)`` and ``level(p1)`` of opposite sign); returns
``t in (0, 1)`` with ``level(p0 + t (p1 - p0)) == 0``.  Default:
vectorised bisection on `level`; shapes with closed-form
intersections override this.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L261-L274)

### `level(coords)`

Signed level function at world ``coords`` shaped (..., ndim).

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L199-L201)

### `level_body(coords)`

Signed level function at body-frame ``coords`` shaped (..., ndim).

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L251-L252)

### `normal(coords)`

Outward (solid→fluid) unit normal at world surface points.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L203-L206)

### `normal_body(coords)`

Gradient direction of `level_body` (finite differences).

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L254-L255)

### `to_body(coords)`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L190-L192)

### `vec_to_world(vecs)`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L194-L195)

### `__slots__`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L188-L188)

## `construct_ibm_particles(particles, x_c, *, axes = None, shape = None, rescale = True, contact = 'no_flux', halo = 2, fill_value = None)`

[Open dedicated reference page](../symbols/pymrm.particles.construct_ibm_particles)

Build immersed-boundary data directly from a particle assembly.

### Parameters

- `particles` (*sequence of Particle*)

- `x_c` (*array_like or list of array_like*)
  Cell-centre coordinates, one 1-D array per spatial axis.

- `axes, shape, rescale` (*see `pymrm.construct_ibm`.*)

- `contact` (*{'no_flux', 'merge', 'error'}, optional*)
  Policy for solid–solid faces between two different particles whose
  surfaces are separated by a sub-cell gap (see the module docstring).
  Genuinely overlapping particles are always merged.

- `halo` (*int, optional*)
  Extra cells around each particle's bounding box when classifying.

- `fill_value` (*float, optional*)
  ``pseudo_sdf`` value for cells not covered by any particle window
  (default: 4× the largest cell spacing — any positive value works,
  only the sign is used downstream).

### Returns

- `ibm` (*IBM*)
  Standard immersed-boundary container; all of `pymrm.apply_ibm`,
  `pymrm.apply_ibm_interface`, etc. apply unchanged.

- `info` (*ParticleIBMInfo*)
  Ownership, exact normals, contact bookkeeping, ``pseudo_sdf`` and a
  per-particle `~pymrm.segmentation.Segmentation`.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L520-L712)

## `contact_conditions(base_ic, ibm, info, *, contact_ic = None)`

[Open dedicated reference page](../symbols/pymrm.particles.contact_conditions)

Per-crossing ic: *base_ic* everywhere, a contact condition on contacts.

### Parameters

- `base_ic` (*tuple of two dicts*)
  Interface condition for the regular (fluid–solid) crossings, in the
  format of `pymrm.apply_ibm_interface`.  Coefficients may be
  scalars or ns-broadcastable arrays (no per-crossing arrays).

- `ibm` (*IBM*)

- `info` (*ParticleIBMInfo*)

- `contact_ic` (*tuple of two dicts, optional*)
  Condition imposed on the contact crossings.  Default: independent
  homogeneous Neumann on both sides (``q_out = 0`` and ``q_in = 0``) —
  no transport between the particles.

### Returns

- `tuple of two dicts with per-crossing coefficient arrays.`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L807-L856)
