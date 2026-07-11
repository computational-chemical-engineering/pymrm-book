# `pymrm.particles.Particle`

[Back to module page](../modules/pymrm.particles) · [Back to alphabetical overview](../alphabetical_overview)

## Signature

`Particle(position, orientation = None)`

## Summary

Abstract particle: a shape at a position with an orientation.

## Documentation

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

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L140-L238)

```python
class Particle(ABC):
    """Abstract particle: a shape at a position with an orientation.

    Subclasses implement the **body-frame** interface
    (:meth:`level_body`, :meth:`bounding_box_body`, optionally
    :meth:`normal_body`); the world-frame API used by the IBM assembly
    (:meth:`level`, :meth:`normal`, :meth:`intersect`,
    :meth:`bounding_box`) is provided here, including the numeric fallbacks.

    Parameters
    ----------
    position : array_like, shape (ndim,)
        World position of the particle (body-frame origin).
    orientation : optional
        ``None`` (default), an angle in radians (2-D), a
        :class:`scipy.spatial.transform.Rotation` (3-D), or an explicit
        rotation matrix.
    """

    def __init__(self, position, orientation=None):
        self.position = np.asarray(position, dtype=float)
        if self.position.ndim != 1:
            raise ValueError("position must be a 1-D coordinate array")
        self.ndim = self.position.size
        self._R = _rotation_matrix(orientation, self.ndim)
        self.orientation = orientation

    # -- body-frame interface (implemented by shapes) -----------------------

    @abstractmethod
    def level_body(self, coords):
        """Signed level function at body-frame ``coords`` shaped (..., ndim)."""

    @abstractmethod
    def bounding_box_body(self):
        """Body-frame bounding box ``((lo, hi), ...)`` per axis."""

    def normal_body(self, coords):
        """Gradient direction of :meth:`level_body` (finite differences)."""
        coords = np.asarray(coords, dtype=float)
        eps = 1e-5 * max(hi - lo for lo, hi in self.bounding_box_body())
        g = np.empty(coords.shape)
        for a in range(self.ndim):
            dp = coords.copy(); dp[..., a] += eps
            dm = coords.copy(); dm[..., a] -= eps
            g[..., a] = (self.level_body(dp) - self.level_body(dm)) / (2 * eps)
        return g

    # -- world-frame transforms ---------------------------------------------

    def to_body(self, coords):
        v = np.asarray(coords, dtype=float) - self.position
        return v if self._R is None else v @ self._R

    def vec_to_world(self, vecs):
        return vecs if self._R is None else vecs @ self._R.T

    # -- world-frame API consumed by the assembly ---------------------------

    def level(self, coords):
        """Signed level function at world ``coords`` shaped (..., ndim)."""
        return self.level_body(self.to_body(coords))

    def normal(self, coords):
        """Outward (solid→fluid) unit normal at world surface points."""
        n = self.vec_to_world(self.normal_body(self.to_body(coords)))
        return n / np.linalg.norm(n, axis=-1, keepdims=True)

    def bounding_box(self, pad=0.0):
        """World axis-aligned bounding box ``((lo, hi), ...)`` per axis."""
        box = self.bounding_box_body()
        corners = np.array(np.meshgrid(*box, indexing="ij")).reshape(self.ndim, -1).T
        world = (corners if self._R is None else corners @ self._R.T) + self.position
        return tuple((world[:, a].min() - pad, world[:, a].max() + pad)
                     for a in range(self.ndim))

    def intersect(self, p0, p1):
        """Surface crossing fraction ``t`` on the segments ``p0 → p1``.

        ``p0``/``p1`` are ``(n, ndim)`` batches whose endpoints straddle the
        surface (``level(p0)`` and ``level(p1)`` of opposite sign); returns
        ``t in (0, 1)`` with ``level(p0 + t (p1 - p0)) == 0``.  Default:
        vectorised bisection on :meth:`level`; shapes with closed-form
        intersections override this.
        """
        p0 = np.asarray(p0, dtype=float)
        p1 = np.asarray(p1, dtype=float)
        a = np.zeros(p0.shape[0])
        b = np.ones(p0.shape[0])
        fa = self.level(p0)
        d = p1 - p0
        for _ in range(60):
            m = 0.5 * (a + b)
            fm = self.level(p0 + m[:, None] * d)
            same = (fm < 0) == (fa < 0)
            a = np.where(same, m, a)
            fa = np.where(same, fm, fa)
            b = np.where(same, b, m)
        return 0.5 * (a + b)
```

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
