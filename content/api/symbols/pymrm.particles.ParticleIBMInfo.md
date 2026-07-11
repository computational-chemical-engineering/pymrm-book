# `pymrm.particles.ParticleIBMInfo`

[Back to module page](../modules/pymrm.particles) · [Back to alphabetical overview](../alphabetical_overview)

## Signature

`ParticleIBMInfo()`

## Summary

Side-car information produced by `construct_ibm_particles`.

## Documentation

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

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L411-L447)

```python
class ParticleIBMInfo:
    """Side-car information produced by :func:`construct_ibm_particles`.

    Attributes
    ----------
    owner : ndarray of int
        Per spatial cell, index of the owning particle (deepest level
        function) or ``-1`` for fluid.  Shaped like the spatial grid.
    crossing_particle : ndarray of int, shape (n_crossings,)
        Owning particle of the solid (``in``) side of each crossing.
    contact : ndarray of bool, shape (n_crossings,)
        True for contact crossings (solid–solid faces between two particles
        under the ``"no_flux"`` policy).  For these,
        ``crossing_particle`` is the ``in``-side particle and
        ``contact_partner`` the ``out``-side one.
    contact_partner : ndarray of int, shape (n_crossings,)
        The ``out``-side particle of a contact crossing, ``-1`` elsewhere.
    normals : ndarray, shape (n_crossings, ndim)
        Exact outward (solid→fluid) unit normals from the owning particle —
        pass to ``construct_ibm_normal_derivative(..., normals=...)``.  For
        contact crossings: the ``in``-side particle's outward normal.
    pseudo_sdf : ndarray
        Sign-correct union level field on the spatial grid (positive filler
        far from every particle) for region classification in the
        reconstruction.
    segmentation : Segmentation
        Per-particle labels (``owner + 1``) — valid even at exact contact,
        where :func:`pymrm.segment_domain` would merge the bodies.
    """

    owner: np.ndarray
    crossing_particle: np.ndarray
    contact: np.ndarray
    contact_partner: np.ndarray
    normals: np.ndarray
    pseudo_sdf: np.ndarray
    segmentation: Segmentation
```

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
