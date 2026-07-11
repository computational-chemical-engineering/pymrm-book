# `pymrm.particles.Box`

[Back to module page](../modules/pymrm.particles) · [Back to alphabetical overview](../alphabetical_overview)

## Signature

`Box(position, half_extents, orientation = None)`

## Summary

Axis-aligned (in body frame) box; rotate via ``orientation``.

## Documentation

``half_extents`` are the half side lengths per axis.  Exact SDF and
face normals; segment intersections by the default bisection.

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L280-L309)

```python
class Box(Particle):
    """Axis-aligned (in body frame) box; rotate via ``orientation``.

    ``half_extents`` are the half side lengths per axis.  Exact SDF and
    face normals; segment intersections by the default bisection.
    """

    def __init__(self, position, half_extents, orientation=None):
        position = np.asarray(position, dtype=float)
        super().__init__(position, orientation)
        self.half_extents = np.broadcast_to(
            np.asarray(half_extents, dtype=float), (self.ndim,)).copy()

    def level_body(self, coords):
        q = np.abs(np.asarray(coords, dtype=float)) - self.half_extents
        outside = np.linalg.norm(np.maximum(q, 0.0), axis=-1)
        inside = np.minimum(np.max(q, axis=-1), 0.0)
        return outside + inside

    def normal_body(self, coords):
        coords = np.asarray(coords, dtype=float)
        q = np.abs(coords) - self.half_extents
        pos = np.maximum(q, 0.0)
        out = np.any(q > 0.0, axis=-1)
        n = np.where(out[..., None], pos,
                     np.where(q == np.max(q, axis=-1, keepdims=True), 1.0, 0.0))
        return n * np.sign(coords + np.where(coords == 0.0, 1.0, 0.0))

    def bounding_box_body(self):
        return tuple((-h, h) for h in self.half_extents)
```

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
