# `pymrm.particles.AnalyticParticle`

[Back to module page](../modules/pymrm.particles) · [Back to alphabetical overview](../alphabetical_overview)

## Signature

`AnalyticParticle(level_func, bounding_box, position, orientation = None, normal_func = None)`

## Summary

Particle from a user-supplied body-frame level function.

## Documentation

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

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L312-L347)

```python
class AnalyticParticle(Particle):
    """Particle from a user-supplied body-frame level function.

    Parameters
    ----------
    level_func : callable
        ``level_func(coords) -> values`` with ``coords`` shaped (..., ndim);
        negative inside, positive outside, approximately a distance near the
        surface.
    bounding_box : tuple of (lo, hi)
        Body-frame box containing the particle surface.
    position, orientation : see :class:`Particle`.
    normal_func : callable, optional
        Body-frame outward normal direction (need not be normalised);
        default: finite differences of *level_func*.
    """

    def __init__(self, level_func, bounding_box, position, orientation=None,
                 normal_func=None):
        super().__init__(position, orientation)
        self._level_func = level_func
        self._box = tuple((float(lo), float(hi)) for lo, hi in bounding_box)
        if len(self._box) != self.ndim:
            raise ValueError("bounding_box length must equal len(position)")
        self._normal_func = normal_func

    def level_body(self, coords):
        return np.asarray(self._level_func(np.asarray(coords, dtype=float)))

    def normal_body(self, coords):
        if self._normal_func is None:
            return super().normal_body(coords)
        return np.asarray(self._normal_func(np.asarray(coords, dtype=float)))

    def bounding_box_body(self):
        return self._box
```

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
