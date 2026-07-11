# `pymrm.particles.GridParticle`

[Back to module page](../modules/pymrm.particles) · [Back to alphabetical overview](../alphabetical_overview)

## Signature

`GridParticle(values, x_local, position, orientation = None, method = 'cubic')`

## Summary

Particle from level-function samples on its own body-frame grid.

## Documentation

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

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L350-L403)

```python
class GridParticle(Particle):
    """Particle from level-function samples on its own body-frame grid.

    The samples are interpolated with a cubic B-spline
    (:class:`scipy.interpolate.RegularGridInterpolator`), so the particle can
    be translated and rotated for free.  The local grid **must extend beyond
    the particle surface** (positive samples all around); queries outside the
    local grid return the clamped boundary value plus the clamping distance,
    keeping the sign correct far away.

    Parameters
    ----------
    values : ndarray
        Level-function samples, negative inside.
    x_local : list of 1-D arrays
        Body-frame cell coordinates of the sample grid, one per axis.
    position, orientation : see :class:`Particle`.
    method : str, optional
        Interpolation method (default ``"cubic"``).
    """

    def __init__(self, values, x_local, position, orientation=None,
                 method="cubic"):
        position = np.asarray(position, dtype=float)
        super().__init__(position, orientation)
        from scipy.interpolate import RegularGridInterpolator
        values = np.asarray(values, dtype=float)
        x_local = [np.asarray(x, dtype=float) for x in x_local]
        if values.ndim != self.ndim or len(x_local) != self.ndim:
            raise ValueError("values/x_local dimensionality mismatch")
        self._lo = np.array([x[0] for x in x_local])
        self._hi = np.array([x[-1] for x in x_local])
        self._interp = RegularGridInterpolator(
            x_local, values, method=method, bounds_error=False, fill_value=None)
        self._eps = 1e-5 * float(np.max(self._hi - self._lo))

    def level_body(self, coords):
        coords = np.asarray(coords, dtype=float)
        clipped = np.clip(coords, self._lo, self._hi)
        excess = np.linalg.norm(coords - clipped, axis=-1)
        return self._interp(clipped) + excess

    def normal_body(self, coords):
        coords = np.asarray(coords, dtype=float)
        eps = self._eps
        g = np.empty(coords.shape)
        for a in range(self.ndim):
            dp = coords.copy(); dp[..., a] += eps
            dm = coords.copy(); dm[..., a] -= eps
            g[..., a] = (self.level_body(dp) - self.level_body(dm)) / (2 * eps)
        return g

    def bounding_box_body(self):
        return tuple((lo, hi) for lo, hi in zip(self._lo, self._hi))
```

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
