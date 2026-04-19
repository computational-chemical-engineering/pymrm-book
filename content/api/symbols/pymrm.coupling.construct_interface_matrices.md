# `pymrm.coupling.construct_interface_matrices`

[Back to module page](../modules/pymrm.coupling.md) · [Back to alphabetical overview](../alphabetical_overview.md)

## Signature

`construct_interface_matrices(shapes, x_fs, x_cs = (None, None), ic = ({'a': (1, 1), 'b': (0, 0), 'd': 0}, {'a': (0, 0), 'b': (1, -1), 'd': 0}), axis = 0, shapes_d = (None, None), format = 'csc')`

## Summary

Construct implicit interface-coupling matrices for two adjacent domains.

## Documentation

### Parameters

- `shapes` (*tuple[tuple[int, ...], tuple[int, ...]]*)
  Shapes of the two subdomains.

- `x_fs` (*tuple[array_like, array_like]*)
  Face coordinates for each subdomain along ``axis``.

- `x_cs` (*tuple[array_like | None, array_like | None], optional*)
  Cell-center coordinates for each subdomain.

- `ic` (*tuple[dict, dict], optional*)
  Two interface equations. Each dictionary may define ``a``, ``b``, and
  ``d`` terms with coefficients for both subdomains.

- `axis` (*int, optional*)
  Interface-normal axis.

- `shapes_d` (*tuple[tuple | None, tuple | None], optional*)
  Optional source-vector shapes for decomposed inhomogeneous terms.

- `format` (*{'csc', 'csr'}, optional*)
  Sparse format for the homogeneous interface matrices.

### Returns

- `tuple`
  Without ``shapes_d``:
  ``(mat0, bc0, mat1, bc1)``.
  With ``shapes_d``:
  ``(mat0, bc00, bc01, mat1, bc10, bc11)``.

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/0b0ac9e5d5a7ceb669718e3aafef1ebd9960b860/src/pymrm/coupling.py#L190-L394)

```python
def construct_interface_matrices(
    shapes,
    x_fs,
    x_cs=(None, None),
    ic=({"a": (1, 1), "b": (0, 0), "d": 0}, {"a": (0, 0), "b": (1, -1), "d": 0}),
    axis=0,
    shapes_d=(None, None),
    format="csc",
):
    """Construct implicit interface-coupling matrices for two adjacent domains.

    Parameters
    ----------
    shapes : tuple[tuple[int, ...], tuple[int, ...]]
        Shapes of the two subdomains.
    x_fs : tuple[array_like, array_like]
        Face coordinates for each subdomain along ``axis``.
    x_cs : tuple[array_like | None, array_like | None], optional
        Cell-center coordinates for each subdomain.
    ic : tuple[dict, dict], optional
        Two interface equations. Each dictionary may define ``a``, ``b``, and
        ``d`` terms with coefficients for both subdomains.
    axis : int, optional
        Interface-normal axis.
    shapes_d : tuple[tuple | None, tuple | None], optional
        Optional source-vector shapes for decomposed inhomogeneous terms.
    format : {'csc', 'csr'}, optional
        Sparse format for the homogeneous interface matrices.

    Returns
    -------
    tuple
        Without ``shapes_d``:
        ``(mat0, bc0, mat1, bc1)``.
        With ``shapes_d``:
        ``(mat0, bc00, bc01, mat1, bc10, bc11)``.
    """

    if not all(
        s1 == s2 for i, (s1, s2) in enumerate(zip(shapes[0], shapes[1])) if i != axis
    ):
        raise ValueError(
            "Tuples shapes[0] and shapes[1] must be equal except for the specified axis."
        )
    shape = tuple(
        s1 + s2 if i == axis else s1
        for i, (s1, s2) in enumerate(zip(shapes[0], shapes[1]))
    )
    shape_i = tuple(1 if i == axis else s for i, s in enumerate(shape))

    # Extract the cell-centered grid points for the two subdomains
    for i in range(2):
        if x_cs[i] is None:
            x_cs = list(x_cs)
            x_cs[i] = 0.5 * (x_fs[i][1:] + x_fs[i][:-1])

    a, b = [
        [
            tuple(
                (
                    unwrap_bc_coeff(shape, ic_elem.get(key, (0, 0))[j], axis=axis)
                    if ic_elem and key in ic_elem
                    else np.zeros((1,) * len(shape_i))
                )
                for j in range(2)
            )
            for ic_elem in ic
        ]
        for key in ["a", "b"]
    ]

    d = [
        (
            unwrap_bc_coeff(shape, ic_elem.get("d", 0), axis=axis)
            if ic_elem and "d" in ic_elem
            else np.zeros((1,) * len(shape_i))
        )
        for ic_elem in ic
    ]

    alpha_1 = [None, None]
    alpha_1[0] = -(x_cs[0][-2] - x_fs[0][-1]) / (
        (x_cs[0][-1] - x_fs[0][-1]) * (x_cs[0][-2] - x_cs[0][-1])
    )
    alpha_1[1] = (x_cs[1][1] - x_fs[1][0]) / (
        (x_cs[1][0] - x_fs[1][0]) * (x_cs[1][1] - x_cs[1][0])
    )
    alpha_2 = [None, None]
    alpha_2[0] = -(x_cs[0][-1] - x_fs[0][-1]) / (
        (x_cs[0][-2] - x_fs[0][-1]) * (x_cs[0][-2] - x_cs[0][-1])
    )
    alpha_2[1] = (x_cs[1][0] - x_fs[1][0]) / (
        (x_cs[1][1] - x_fs[1][0]) * (x_cs[1][1] - x_cs[1][0])
    )
    alpha_0 = [alpha_1[0] - alpha_2[0], alpha_1[1] - alpha_2[1]]

    # reminder of notation
    # dc/dn[0] = alpha_0[0] c_i - alpha_1[0] c[-1] + alpha_2[0] c[-2]
    # dc/dn[1] = -alpha_0[1] c_i + alpha_1[1] c[0] - alpha_2[1] c[1]
    # interface conditions of the form:

    m = [[None for _ in range(2)] for _ in range(2)]
    v = [[None for _ in range(4)] for _ in range(2)]
    m_inv = [[None for _ in range(2)] for _ in range(2)]
    values = [[None for _ in range(4)] for _ in range(2)]
    for i in range(2):  # loop over the two conditions
        m[i][0] = a[i][0] * alpha_0[0] + b[i][0]
        m[i][1] = a[i][1] * alpha_0[1] + b[i][1]
        v[i][0] = -a[i][0] * alpha_2[0]
        v[i][1] = a[i][0] * alpha_1[0]
        v[i][2] = a[i][1] * alpha_1[1]
        v[i][3] = -a[i][1] * alpha_2[1]
    det = m[0][0] * m[1][1] - m[0][1] * m[1][0]
    det_inv = np.where(det != 0.0, 1.0 / det, 0.0)
    m_inv[0][0] = m[1][1] * det_inv
    m_inv[0][1] = -m[0][1] * det_inv
    m_inv[1][0] = -m[1][0] * det_inv
    m_inv[1][1] = m[0][0] * det_inv
    for j in range(2):
        for i in range(4):
            values[j][i] = m_inv[j][0] * v[0][i] + m_inv[j][1] * v[1][i]
            values[j][i] = np.broadcast_to(values[j][i], shape_i)
        values[j] = np.concatenate(values[j], axis=axis)

    shape_t = [math.prod(shape[0:axis]), shape[axis], math.prod(shape[axis + 1:])]
    n0, n1, n2 = shape_t
    i0 = np.arange(n0).reshape(-1, 1, 1)
    i2 = np.arange(n2).reshape(1, 1, -1)
    # Row indices: flat index into the interface (n0 x n2) array
    row_indices = np.ravel_multi_index(
        (i0, np.zeros((1, 4, 1), dtype=int), i2), (n0, 1, n2)
    )
    # Column indices: 4-point stencil around the interface
    stencil = (shapes[0][axis] + np.array([-2, -1, 0, 1])).reshape(1, -1, 1)
    col_indices = np.ravel_multi_index((i0, stencil, i2), shape_t)

    # Create the sparse matrix representing the interface
    interface_matrix = [None] * 2
    for j in range(2):
        fltr = values[j].ravel() != 0
        values_filtered = values[j].ravel()[fltr]
        row_indices_filtered = row_indices.ravel()[fltr]
        col_indices_filtered = col_indices.ravel()[fltr]
        interface_matrix[j] = _sparse_array(
            (values_filtered, (row_indices_filtered, col_indices_filtered)),
            shape=(shape_t[0] * shape_t[2], math.prod(shape_t)),
            format=format,
        )

    row_indices_bc = np.ravel_multi_index(
        (np.arange(n0).reshape(-1, 1), np.arange(n2).reshape(1, -1)), (n0, n2)
    )
    if shapes_d[0] is None and shapes_d[1] is None:
        interface_bc = [None] * 2
        for j in range(2):
            values_bc = m_inv[j][0] * d[0] + m_inv[j][1] * d[1]
            values_bc = np.broadcast_to(values_bc, shape_i)
            fltr = values_bc.ravel() != 0
            values_filtered = values_bc.ravel()[fltr]
            row_indices_filtered = row_indices_bc.ravel()[fltr]
            interface_bc[j] = csc_array(
                (values_filtered, row_indices_filtered, np.array([0, row_indices_filtered.size])),
                shape=(shape_t[0] * shape_t[2], 1),
            )
        return (
            interface_matrix[0],
            interface_bc[0],
            interface_matrix[1],
            interface_bc[1],
        )
    else:
        interface_bc = [[None for _ in range(2)] for _ in range(2)]
        for j in range(2):
            for i in range(2):
                values_bc = m_inv[j][i] * d[i]
                values_bc = np.broadcast_to(values_bc, shape_i)
                fltr = values_bc.ravel() != 0
                values_filtered = values_bc.ravel()[fltr]
                row_indices_filtered = row_indices_bc.ravel()[fltr]
                if shapes_d[j] is None:
                    interface_bc[j][i] = csc_array(
                        (
                            values_filtered,
                            row_indices_filtered,
                            np.array([0, row_indices_filtered.size]),
                        ),
                        shape=(shape_t[0] * shape_t[2], 1),
                    )
                else:
                    num_cols = math.prod(shapes_d[j])
                    col_indices_bc = np.arange(num_cols, dtype=int).reshape(shapes_d[j])
                    col_indices_bc = np.broadcast_to(col_indices_bc, shape_i)
                    col_indices_filtered = col_indices_bc.ravel()[fltr]
                    interface_bc[j][i] = csc_array(
                        (values_filtered, (row_indices_filtered, col_indices_filtered)),
                        shape=(shape_t[0] * shape_t[2], num_cols),
                    )
        return (
            interface_matrix[0],
            interface_bc[0][0],
            interface_bc[0][1],
            interface_matrix[1],
            interface_bc[1][0],
            interface_bc[1][1],
        )
```
