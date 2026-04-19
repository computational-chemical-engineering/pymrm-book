# `pymrm.interpolate.construct_boundary_value_matrices`

[Back to module page](../modules/pymrm.interpolate.md) · [Back to alphabetical overview](../alphabetical_overview.md)

## Signature

`construct_boundary_value_matrices(shape, x_f, x_c = None, bc = None, axis = 0, bound_id = 0, shape_d = None, format = 'csc')`

## Summary

Build matrices that evaluate boundary values from cell-centered unknowns.

## Documentation

### Parameters

- `shape` (*tuple[int, ...]*)
  Cell-centered field shape.

- `x_f` (*array_like*)
  Face coordinates along ``axis``.

- `x_c` (*array_like, optional*)
  Cell-center coordinates near the selected boundary.

- `bc` (*dict, optional*)
  Boundary-condition dictionary with keys ``a``, ``b``, and ``d``.

- `axis` (*int, optional*)
  Boundary-normal axis.

- `bound_id` (*{0, 1}, optional*)
  ``0`` for the lower/left boundary, ``1`` for upper/right.

- `shape_d` (*tuple[int, ...], optional*)
  Shape of external inhomogeneous source unknowns.

- `format` (*{'csc', 'csr'}, optional*)
  Sparse format for the homogeneous matrix.

### Returns

- `tuple`
  ``(matrix, mat_bc)`` where ``matrix`` maps cell-centered values to
  boundary values and ``mat_bc`` maps inhomogeneous boundary terms.

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/0b0ac9e5d5a7ceb669718e3aafef1ebd9960b860/src/pymrm/interpolate.py#L577-L722)

```python
def construct_boundary_value_matrices(
    shape, x_f, x_c=None, bc=None, axis=0, bound_id=0, shape_d=None, format="csc"
):
    """Build matrices that evaluate boundary values from cell-centered unknowns.

    Parameters
    ----------
    shape : tuple[int, ...]
        Cell-centered field shape.
    x_f : array_like
        Face coordinates along ``axis``.
    x_c : array_like, optional
        Cell-center coordinates near the selected boundary.
    bc : dict, optional
        Boundary-condition dictionary with keys ``a``, ``b``, and ``d``.
    axis : int, optional
        Boundary-normal axis.
    bound_id : {0, 1}, optional
        ``0`` for the lower/left boundary, ``1`` for upper/right.
    shape_d : tuple[int, ...], optional
        Shape of external inhomogeneous source unknowns.
    format : {'csc', 'csr'}, optional
        Sparse format for the homogeneous matrix.

    Returns
    -------
    tuple
        ``(matrix, mat_bc)`` where ``matrix`` maps cell-centered values to
        boundary values and ``mat_bc`` maps inhomogeneous boundary terms.
    """

    if bound_id not in (0, 1):
        raise ValueError("bound_id must be 0 or 1")

    # Trick: Reshape to triplet shape_t
    shape_t = (math.prod(shape[:axis]), shape[axis], math.prod(shape[axis + 1:]))
    shape_bc = shape[:axis] + (1,) + shape[axis + 1:]
    shape_bc_d = (shape_t[0], shape_t[2])

    # Handle special case with one cell in the dimension axis

    if bound_id == 0:
        idx_c_0 = 0
        idx_c_1 = 1
        idx_0 = 0
        idx_1 = 1
        sgn = 1
    else:
        idx_c_0 = shape_t[1] - 2
        idx_c_1 = shape_t[1] - 1
        idx_0 = -1
        idx_1 = -2
        sgn = -1
    if x_c is None:
        if bound_id == 0:
            x_c = 0.5 * np.array([x_f[0] + x_f[1], x_f[1] + x_f[2]])
        else:
            x_c = 0.5 * np.array([x_f[-3] + x_f[-2], x_f[-2] + x_f[-1]])
    n0, n1, n2 = shape_t
    i0 = np.arange(n0).reshape(-1, 1, 1)
    i2 = np.arange(n2).reshape(1, 1, -1)
    # Cell indices: two cells nearest the boundary
    i_c = np.ravel_multi_index(
        (i0, np.array([idx_c_0, idx_c_1]).reshape(1, -1, 1), i2), shape_t
    )
    # Row indices: both entries map to row 0 (single boundary row per batch)
    i_f = np.ravel_multi_index(
        (i0, np.array([0, 0]).reshape(1, -1, 1), i2), (n0, 1, n2)
    )
    i_f_bc = np.ravel_multi_index(
        (np.arange(n0).reshape(-1, 1), np.arange(n2).reshape(1, -1)), (n0, n2)
    ).reshape(n0, 1, n2)
    values_bc = np.empty((shape_t[0], shape_t[2]))
    values = np.empty((shape_t[0], 2, shape_t[2]))

    # Get a, b, and d from dictionary
    a, b, d = [
        (
            unwrap_bc_coeff(shape, bc[key], axis=axis)
            if bc
            else np.zeros((1,) * len(shape))
        )
        for key in ["a", "b", "d"]
    ]
    a *= sgn
    alpha_1 = (x_c[idx_1] - x_f[idx_0]) / (
        (x_c[idx_0] - x_f[idx_0]) * (x_c[idx_1] - x_c[idx_0])
    )
    alpha_2 = (x_c[idx_0] - x_f[idx_0]) / (
        (x_c[idx_1] - x_f[idx_0]) * (x_c[idx_1] - x_c[idx_0])
    )
    alpha_0 = alpha_1 - alpha_2
    fctr = alpha_0 * a + b
    np.divide(1, fctr, out=fctr, where=(fctr != 0))
    a_fctr = a * fctr
    a_fctr = np.broadcast_to(a_fctr, shape_bc).reshape(shape_bc_d)
    d_fctr = d * fctr
    d_fctr = np.broadcast_to(d_fctr, shape_bc).reshape(shape_bc_d)
    values[:, idx_0, :] = a_fctr * alpha_1
    values[:, idx_1, :] = -a_fctr * alpha_2
    values_bc[:, :] = d_fctr
    if np.any(fctr == 0.0):
        fltr = np.reshape(np.broadcast_to((fctr == 0.0), shape_bc), shape_bc_d)
        values[:, idx_0, :][fltr] = (x_c[idx_1] - x_f[idx_0]) / (
            x_c[idx_1] - x_c[idx_0]
        )
        values[:, idx_1, :][fltr] = (x_c[idx_0] - x_f[idx_0]) / (
            x_c[idx_0] - x_c[idx_1]
        )
        values_bc[fltr] = 0.0

    if format == "csc":
        matrix = csc_array(
            (values.ravel(), (i_f.ravel(), i_c.ravel())),
            shape=(math.prod(shape_bc), math.prod(shape_t)),
        )
    elif format == "csr":
        # Each boundary row has 2 entries (the two nearest cells).
        # Reorder to (n0, n2, 2) so entries are grouped by row.
        values_csr = values.transpose(0, 2, 1)
        cols_csr = i_c.transpose(0, 2, 1)
        num_rows = n0 * n2
        indptr = np.arange(0, 2 * num_rows + 1, 2, dtype=np.intp)
        matrix = csr_array(
            (values_csr.ravel(), cols_csr.ravel(), indptr),
            shape=(math.prod(shape_bc), math.prod(shape_t)),
        )
    else:
        raise ValueError(
            f"format must be 'csc' or 'csr', got {format!r}"
        )
    matrix.sort_indices()
    if shape_d is None:
        mat_bc = csc_array(
            (values_bc.ravel(), i_f_bc.ravel(), np.array([0, i_f_bc.size])),
            shape=(math.prod(shape_bc), 1),
        )
    else:
        num_cols = math.prod(shape_d)
        i_cols_bc = np.arange(num_cols, dtype=int).reshape(shape_d)
        i_cols_bc = np.broadcast_to(i_cols_bc, shape_bc)
        mat_bc = csc_array(
            (values_bc.ravel(), (i_f_bc.ravel(), i_cols_bc.ravel())),
            shape=(math.prod(shape_bc), num_cols),
        )
    return matrix, mat_bc
```
