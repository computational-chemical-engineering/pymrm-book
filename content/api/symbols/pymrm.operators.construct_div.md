# `pymrm.operators.construct_div`

[Back to module page](../modules/pymrm.operators.md) · [Back to alphabetical overview](../alphabetical_overview.md)

## Signature

`construct_div(shape, x_f, nu = 0, axis = 0, format = 'csc')`

## Summary

Construct a divergence matrix that maps face fluxes to cell balances.

## Documentation

### Parameters

- `shape` (*tuple[int, ...] or int*)
  Cell-centered field shape.

- `x_f` (*array_like*)
  Face coordinates along ``axis``.

- `nu` (*int or callable, optional*)
  Geometry descriptor. ``0`` gives Cartesian, ``1`` cylindrical,
  ``2`` spherical, and a callable ``nu(x)`` enables custom metrics.

- `axis` (*int, optional*)
  Axis for flux divergence.

- `format` (*{'csc', 'csr'}, optional*)
  Sparse format of the returned operator.

### Returns

- `scipy.sparse.csc_array or scipy.sparse.csr_array`
  Divergence operator.

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/0b0ac9e5d5a7ceb669718e3aafef1ebd9960b860/src/pymrm/operators.py#L400-L508)

```python
def construct_div(shape, x_f, nu=0, axis=0, format="csc"):
    """Construct a divergence matrix that maps face fluxes to cell balances.

    Parameters
    ----------
    shape : tuple[int, ...] or int
        Cell-centered field shape.
    x_f : array_like
        Face coordinates along ``axis``.
    nu : int or callable, optional
        Geometry descriptor. ``0`` gives Cartesian, ``1`` cylindrical,
        ``2`` spherical, and a callable ``nu(x)`` enables custom metrics.
    axis : int, optional
        Axis for flux divergence.
    format : {'csc', 'csr'}, optional
        Sparse format of the returned operator.

    Returns
    -------
    scipy.sparse.csc_array or scipy.sparse.csr_array
        Divergence operator.
    """
    if isinstance(shape, int):
        shape = (shape,)
    else:
        shape = tuple(shape)
    x_f = generate_grid(shape[axis], x_f)

    shape_f = shape[:axis] + (shape[axis] + 1,) + shape[axis + 1:]
    shape_t = (math.prod(shape[:axis]), shape[axis], math.prod(shape[axis + 1:]))
    shape_f_t = (shape_t[0], shape_f[axis], shape_t[2])

    n0, n1, n2 = shape_t
    # Each cell references its left face [j] and right face [j+1]
    i0 = np.arange(n0).reshape(-1, 1, 1, 1)
    i1 = np.arange(n1).reshape(1, -1, 1, 1)
    i2 = np.arange(n2).reshape(1, 1, -1, 1)
    face_pair = np.array([0, 1]).reshape(1, 1, 1, -1)
    i_f = np.ravel_multi_index((i0, i1 + face_pair, i2), shape_f_t)

    if callable(nu):
        area = nu(x_f).ravel()
        inv_sqrt3 = 1 / np.sqrt(3)
        x_f_r = x_f.ravel()
        dx_f = x_f_r[1:] - x_f_r[:-1]
        dvol_inv = 1 / (
            (
                nu(x_f_r[:-1] + (0.5 - 0.5 * inv_sqrt3) * dx_f)
                + nu(x_f_r[:-1] + (0.5 + 0.5 * inv_sqrt3) * dx_f)
            )
            * 0.5
            * dx_f
        )
    elif nu == 0:
        area = np.ones(shape_f_t[1])
        dvol_inv = 1 / (x_f[1:] - x_f[:-1])
    else:
        area = np.power(x_f.ravel(), nu)
        vol = area * x_f.ravel() / (nu + 1)
        dvol_inv = 1 / (vol[1:] - vol[:-1])

    values = np.empty((shape_t[1], 2))
    values[:, 0] = -area[:-1] * dvol_inv
    values[:, 1] = area[1:] * dvol_inv
    values_per_axis = values  # per-axis values (n1, 2) before tiling
    values = np.tile(values.reshape((1, -1, 1, 2)), (shape_t[0], 1, shape_t[2]))

    num_cells = np.prod(shape_t, dtype=int)
    num_face_flat = np.prod(shape_f_t, dtype=int)
    if format == "csc":
        # Build CSC data in column (face) order with indptr.
        # Cell indices: shape (n0, n1, n2)
        i_c = np.ravel_multi_index(
            (i0[..., 0], i1[..., 0], i2[..., 0]), (n0, n1, n2)
        )
        # (n0, n1+1, n2, 2): slot 0 = from cell j-1, slot 1 = from cell j
        csc_data = np.zeros((n0, n1 + 1, n2, 2))
        csc_rows = np.empty((n0, n1 + 1, n2, 2), dtype=np.intp)
        # Slot 0: entry from cell j-1 (right face = face j), valid j=1..n1
        csc_data[:, 1:, :, 0] = values_per_axis[:, 1].reshape(1, n1, 1)
        csc_rows[:, 1:, :, 0] = i_c
        # Face 0 has no cell j-1; use cell 0's row so the dummy zero
        # entry lands on a valid row that already carries a zero value.
        csc_rows[:, 0, :, 0] = i_c[:, 0, :]
        # Slot 1: entry from cell j (left face = face j), valid j=0..n1-1
        csc_data[:, :-1, :, 1] = values_per_axis[:, 0].reshape(1, n1, 1)
        csc_rows[:, :-1, :, 1] = i_c
        # Face n1 has no cell j; use cell n1-1's row so the dummy zero
        # entry lands on a valid row that already carries a zero value.
        csc_rows[:, -1, :, 1] = i_c[:, -1, :]
        # Uniform 2 entries per column → simple indptr
        indptr = np.arange(0, 2 * num_face_flat + 1, 2, dtype=np.intp)
        div_matrix = csc_array(
            (csc_data.ravel(), csc_rows.ravel(), indptr),
            shape=(num_cells, num_face_flat),
        )
    elif format == "csr":
        # Uniform 2 entries per row (each cell references left + right face)
        indptr = np.arange(0, 2 * num_cells + 1, 2, dtype=np.intp)
        div_matrix = csr_array(
            (values.ravel(), i_f.ravel(), indptr),
            shape=(num_cells, num_face_flat),
        )
    else:
        raise ValueError(
            f"format must be 'csc' or 'csr', got {format!r}"
        )
    div_matrix.sort_indices()
    return div_matrix
```
