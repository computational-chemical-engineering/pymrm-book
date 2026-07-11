# `pymrm.ibm.construct_ibm`

[Back to module page](../modules/pymrm.ibm) · [Back to alphabetical overview](../alphabetical_overview)

## Signature

`construct_ibm(sdf, x_c, axes = None, shape = None, rescale = True)`

## Summary

Build the immersed-boundary data from a spatial signed-distance field.

## Documentation

### Parameters

- `sdf` (*array_like*)
  Signed-distance field sampled at the **spatial** cell centres.
  ``sdf.shape`` must equal ``tuple(shape[a] for a in axes)``.
  Cells with ``sdf < 0`` are solid; ``sdf >= 0`` is fluid.

- `x_c` (*array_like or list of array_like*)
  Cell-centre coordinates.  For a 1-D spatial grid a single 1-D array
  is accepted; for N-D spatial grids supply a list of N 1-D arrays (one
  per spatial axis).  The i-th element has length ``sdf.shape[i]``.

- `axes` (*tuple of int, optional*)
  Which axes of the **full field** array correspond to spatial
  coordinates.  Length must equal ``sdf.ndim``.  Defaults to
  ``tuple(range(sdf.ndim))`` (all axes are spatial).

- `shape` (*tuple of int, optional*)
  Full field shape, including any non-spatial dimensions (components,
  phases, species, etc.).  Defaults to ``sdf.shape`` (purely spatial,
  no non-spatial axes).

- `rescale` (*bool, optional*)
  If ``True`` (default), apply a geometric per-row conditioning scale.

### Returns

- `IBM`
  Container holding per-crossing geometry, Lagrange coefficients, and
  per-row conditioning scales for both sides of the interface.

### Notes

The IBM uses cell-centre coordinates directly.  Face coordinates are not
required because the Lagrange interpolation nodes are the cell centres and
the wall position is found from the SDF: ``x_w = x_c + θ (x_ghost − x_c)``.

Every wall crossing ``k`` is the face between one fluid cell and one solid
cell.  ``ibm.coords[k]``, ``ibm.row_out[k]`` (fluid side, spatial flat
index), and ``ibm.row_in[k]`` (solid side, spatial flat index) all refer
to the same physical wall crossing.

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm.py#L612-L658)

```python
def construct_ibm(sdf, x_c, axes=None, shape=None, rescale=True):
    """Build the immersed-boundary data from a spatial signed-distance field.

    Parameters
    ----------
    sdf : array_like
        Signed-distance field sampled at the **spatial** cell centres.
        ``sdf.shape`` must equal ``tuple(shape[a] for a in axes)``.
        Cells with ``sdf < 0`` are solid; ``sdf >= 0`` is fluid.
    x_c : array_like or list of array_like
        Cell-centre coordinates.  For a 1-D spatial grid a single 1-D array
        is accepted; for N-D spatial grids supply a list of N 1-D arrays (one
        per spatial axis).  The i-th element has length ``sdf.shape[i]``.
    axes : tuple of int, optional
        Which axes of the **full field** array correspond to spatial
        coordinates.  Length must equal ``sdf.ndim``.  Defaults to
        ``tuple(range(sdf.ndim))`` (all axes are spatial).
    shape : tuple of int, optional
        Full field shape, including any non-spatial dimensions (components,
        phases, species, etc.).  Defaults to ``sdf.shape`` (purely spatial,
        no non-spatial axes).
    rescale : bool, optional
        If ``True`` (default), apply a geometric per-row conditioning scale.

    Returns
    -------
    IBM
        Container holding per-crossing geometry, Lagrange coefficients, and
        per-row conditioning scales for both sides of the interface.

    Notes
    -----
    The IBM uses cell-centre coordinates directly.  Face coordinates are not
    required because the Lagrange interpolation nodes are the cell centres and
    the wall position is found from the SDF: ``x_w = x_c + θ (x_ghost − x_c)``.

    Every wall crossing ``k`` is the face between one fluid cell and one solid
    cell.  ``ibm.coords[k]``, ``ibm.row_out[k]`` (fluid side, spatial flat
    index), and ``ibm.row_in[k]`` (solid side, spatial flat index) all refer
    to the same physical wall crossing.
    """
    sdf = np.asarray(sdf, dtype=float)
    strides = np.array(
        [math.prod(sdf.shape[a + 1:]) for a in range(sdf.ndim)], dtype=np.intp
    )
    return _construct_ibm_core(sdf < 0.0, _sdf_theta_fn(sdf, strides), x_c,
                               axes, shape, rescale)
```
