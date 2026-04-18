# `pymrm.convect.construct_convflux_bc`

## Signature

`pymrm.convect.construct_convflux_bc(shape, x_f, x_c=None, bc=(None, None), v=1.0, axis=0, shapes_d=(None, None), format='csc')`

## Docstring

```text
Construct boundary-face upwind corrections and source terms.

Parameters
----------
shape : tuple[int, ...]
    Cell-centered field shape.
x_f : array_like
    Face coordinates along ``axis``.
x_c : array_like, optional
    Cell-center coordinates.
bc : tuple[dict | None, dict | None], optional
    Left and right boundary-condition dictionaries with keys ``a``, ``b``,
    and ``d``.
v : float or array_like, optional
    Face velocity field.
axis : int, optional
    Convection axis.
shapes_d : tuple[tuple | None, tuple | None], optional
    Optional source-vector shapes for inhomogeneous boundary terms.
format : {'csc', 'csr'}, optional
    Sparse format for returned operator matrices.

Returns
-------
tuple
    ``(conv_matrix_bc, conv_bc)`` when ``shapes_d`` is not supplied, or
    ``(conv_matrix_left, conv_bc_left, conv_matrix_right, conv_bc_right)``
    otherwise.
```

## Implementation

```python
def construct_convflux_bc(
    shape, x_f, x_c=None, bc=(None, None), v=1.0, axis=0, shapes_d=(None, None),
    format="csc"
):
    """Construct boundary-face upwind corrections and source terms.

    Parameters
    ----------
    shape : tuple[int, ...]
        Cell-centered field shape.
    x_f : array_like
        Face coordinates along ``axis``.
    x_c : array_like, optional
        Cell-center coordinates.
    bc : tuple[dict | None, dict | None], optional
        Left and right boundary-condition dictionaries with keys ``a``, ``b``,
        and ``d``.
    v : float or array_like, optional
        Face velocity field.
    axis : int, optional
        Convection axis.
    shapes_d : tuple[tuple | None, tuple | None], optional
        Optional source-vector shapes for inhomogeneous boundary terms.
    format : {'csc', 'csr'}, optional
        Sparse format for returned operator matrices.

    Returns
    -------
    tuple
        ``(conv_matrix_bc, conv_bc)`` when ``shapes_d`` is not supplied, or
        ``(conv_matrix_left, conv_bc_left, conv_matrix_right, conv_bc_right)``
        otherwise.
    """

    # Trick: Reshape to triplet shape_t
    shape_f = shape[:axis] + (shape[axis] + 1,) + shape[axis + 1:]
    shape_t = (math.prod(shape[:axis]), shape[axis], math.prod(shape[axis + 1:]))
    shape_f_t = (shape_t[0], shape_f[axis], shape_t[2])
    shape_bc = shape[:axis] + (1,) + shape[axis + 1:]
    shape_bc_d = (shape_t[0], shape_t[2])

    n0, n1, n2 = shape_t
    i0 = np.arange(n0).reshape(-1, 1, 1)
    i2 = np.arange(n2).reshape(1, 1, -1)

    # Handle special case with one cell in the dimension axis
    if n1 == 1:
        a, b, d = [
            [
                (
                    unwrap_bc_coeff(shape, bc_element[key], axis=axis)
                    if bc_element
                    else np.zeros((1,) * len(shape))
                )
                for bc_element in bc
            ]
            for key in ["a", "b", "d"]
        ]
        if x_c is None:
            x_c = 0.5 * (x_f[0:-1] + x_f[1:])
        # Both faces reference cell 0
        i_c = np.ravel_multi_index(
            (i0, np.array([0, 0]).reshape(1, -1, 1), i2), shape_t
        )
        i_f = np.ravel_multi_index(
            (i0, np.array([0, 1]).reshape(1, -1, 1), i2), shape_f_t
        )
        values = np.empty(shape_f_t)
        alpha_1 = (x_f[1] - x_f[0]) / ((x_c[0] - x_f[0]) * (x_f[1] - x_c[0]))
        alpha_2_left = (x_c[0] - x_f[0]) / ((x_f[1] - x_f[0]) * (x_f[1] - x_c[0]))
        alpha_0_left = alpha_1 - alpha_2_left
        alpha_2_right = -(x_c[0] - x_f[1]) / ((x_f[0] - x_f[1]) * (x_f[0] - x_c[0]))
        alpha_0_right = alpha_1 - alpha_2_right
        fctr = (b[0] + alpha_0_left * a[0]) * (
            b[1] + alpha_0_right * a[1]
        ) - alpha_2_left * alpha_2_right * a[0] * a[1]
        np.divide(1, fctr, out=fctr, where=(fctr != 0))
        values = np.empty((shape_t[0], 2, shape_t[2]))
        values[:, 0, :] = np.broadcast_to(
            alpha_1 * a[0] * (a[1] * (alpha_0_right - alpha_2_left) + b[1]) * fctr,
            shape,
        ).reshape(shape_bc_d)
        values[:, 1, :] = np.broadcast_to(
            alpha_1 * a[1] * (a[0] * (alpha_0_left - alpha_2_right) + b[0]) * fctr,
            shape,
        ).reshape(shape_bc_d)

        i_f_bc = np.ravel_multi_index(
            (i0, np.array([0, shape_f_t[1] - 1]).reshape(1, -1, 1), i2), shape_f_t
        )
        values_bc = np.empty((n0, 2, n2))
        values_bc[:, 0, :] = np.broadcast_to(
            ((a[1] * alpha_0_right + b[1]) * d[0] - alpha_2_left * a[0] * d[1]) * fctr,
            shape_bc,
        ).reshape(shape_bc_d)
        values_bc[:, 1, :] = np.broadcast_to(
            ((a[0] * alpha_0_left + b[0]) * d[1] - alpha_2_right * a[1] * d[0]) * fctr,
            shape_bc,
        ).reshape(shape_bc_d)

        if isinstance(v, (float, int)):
            values *= v
            values_bc *= v
        else:
            slicer = [slice(None)] * len(shape)
            slicer[axis] = [0, -1]
            shape_f_b = list(shape_f)
            shape_f_b[axis] = 2
            values = values.reshape(shape_f_b)
            values *= v[tuple(slicer)]
            values_bc = values_bc.reshape(shape_f_b)
            values_bc *= v[tuple(slicer)]
        conv_matrix = _sparse_array(
            (values.ravel(), (i_f.ravel(), i_c.ravel())),
            shape=(math.prod(shape_f_t), math.prod(shape_t)),
            format=format,
        )
    else:
        # Cell indices: 2 near left + 2 near right boundary
        cell_axis_idx = np.array([0, 1, n1 - 2, n1 - 1]).reshape(1, -1, 1)
        i_c = np.ravel_multi_index((i0, cell_axis_idx, i2), shape_t)
        # Face indices: left face (0) twice, right face twice
        nf = shape_f_t[1]
        face_axis_idx = np.array([0, 0, nf - 1, nf - 1]).reshape(1, -1, 1)
        i_f = np.ravel_multi_index((i0, face_axis_idx, i2), shape_f_t)
        i_f_bc = np.ravel_multi_index(
            (i0, np.array([0, nf - 1]).reshape(1, -1, 1), i2), shape_f_t
        )
        values_bc = np.empty((n0, 2, n2))
        values = np.empty((n0, 4, n2))
        if x_c is None:
            x_c = 0.5 * np.array(
                [x_f[0] + x_f[1], x_f[1] + x_f[2], x_f[-3] + x_f[-2], x_f[-2] + x_f[-1]]
            )

        # Get a, b, and d for left bc from dictionary
        a, b, d = [
            (
                unwrap_bc_coeff(shape, bc[0][key], axis=axis)
                if bc[0]
                else np.zeros((1,) * len(shape))
            )
            for key in ["a", "b", "d"]
        ]
        alpha_1 = (x_c[1] - x_f[0]) / ((x_c[0] - x_f[0]) * (x_c[1] - x_c[0]))
        alpha_2 = (x_c[0] - x_f[0]) / ((x_c[1] - x_f[0]) * (x_c[1] - x_c[0]))
        alpha_0 = alpha_1 - alpha_2
        fctr = alpha_0 * a + b
        np.divide(1, fctr, out=fctr, where=(fctr != 0))
        a_fctr = a * fctr
        a_fctr = np.broadcast_to(a_fctr, shape_bc).reshape(shape_bc_d)
        d_fctr = d * fctr
        d_fctr = np.broadcast_to(d_fctr, shape_bc).reshape(shape_bc_d)
        values[:, 0, :] = a_fctr * alpha_1
        values[:, 1, :] = -a_fctr * alpha_2
        values_bc[:, 0, :] = d_fctr

        # Get a, b, and d for right bc from dictionary
        a, b, d = [
            (
                unwrap_bc_coeff(shape, bc[1][key], axis=axis)
                if bc[1]
                else np.zeros((1,) * len(shape))
            )
            for key in ["a", "b", "d"]
        ]
        alpha_1 = -(x_c[-2] - x_f[-1]) / ((x_c[-1] - x_f[-1]) * (x_c[-2] - x_c[-1]))
        alpha_2 = -(x_c[-1] - x_f[-1]) / ((x_c[-2] - x_f[-1]) * (x_c[-2] - x_c[-1]))
        alpha_0 = alpha_1 - alpha_2
        fctr = alpha_0 * a + b
        np.divide(1, fctr, out=fctr, where=(fctr != 0))
        a_fctr = a * fctr
        a_fctr = np.broadcast_to(a_fctr, shape_bc).reshape(shape_bc_d)
        d_fctr = d * fctr
        d_fctr = np.broadcast_to(d_fctr, shape_bc).reshape(shape_bc_d)
        values[:, -1, :] = a_fctr * alpha_1
        values[:, -2, :] = -a_fctr * alpha_2
        values_bc[:, -1, :] = d_fctr
        if isinstance(v, (float, int)):
            values *= v
            values_bc *= v
        else:
            slicer = [slice(None)] * len(shape)
            slicer[axis] = [0, 0, -1, -1]
            shape_f_b = list(shape_f)
            shape_f_b[axis] = 4
            values = values.reshape(shape_f_b)
            values *= v[tuple(slicer)]
            shape_f_b[axis] = 2
            slicer[axis] = [0, -1]
            values_bc = values_bc.reshape(shape_f_b)
            values_bc *= v[tuple(slicer)]

    if (shapes_d[0] is None) and (shapes_d[1] is None):
        conv_bc = csc_array(
            (values_bc.ravel(), i_f_bc.ravel(), np.array([0, i_f_bc.size])),
            shape=(math.prod(shape_f_t), 1),
        )
        conv_matrix = _sparse_array(
            (values.ravel(), (i_f.ravel(), i_c.ravel())),
            shape=(math.prod(shape_f_t), math.prod(shape_t)),
            format=format,
        )
        conv_matrix.sort_indices()
        return conv_matrix, conv_bc
    else:
        values = values.reshape((shape_t[0], 4, shape_t[2]))
        values_bc = values_bc.reshape((shape_t[0], 2, shape_t[2]))
        conv_bc = [None] * 2
        shapes_d = list(shapes_d)
        for i in range(2):
            if shapes_d[i] is None:
                shapes_d[i] = (1,) * len(shape_bc)
            num_cols = math.prod(shapes_d[i])
            i_cols_bc = np.arange(num_cols, dtype=int).reshape(shapes_d[i])
            i_cols_bc = np.broadcast_to(i_cols_bc, shape_bc)
            conv_bc[i] = csc_array(
                (
                    values_bc[:, i, :].ravel(),
                    (i_f_bc[:, i, :].ravel(), i_cols_bc.ravel()),
                ),
                shape=(math.prod(shape_f_t), num_cols),
            )
        if shape_t[1] == 1:
            conv_matrix_0 = _sparse_array(
                (values[:, 0, :].ravel(), (i_f[:, 0, :].ravel(), i_c[:, 0, :].ravel())),
                shape=(math.prod(shape_f_t), math.prod(shape_t)),
                format=format,
            )
            conv_matrix_1 = _sparse_array(
                (
                    values[:, -1, :].ravel(),
                    (i_f[:, -1, :].ravel(), i_c[:, -1, :].ravel()),
                ),
                shape=(math.prod(shape_f_t), math.prod(shape_t)),
                format=format,
            )
        else:
            conv_matrix_0 = _sparse_array(
                (
                    values[:, :2, :].ravel(),
                    (i_f[:, :2, :].ravel(), i_c[:, :2, :].ravel()),
                ),
                shape=(math.prod(shape_f_t), math.prod(shape_t)),
                format=format,
            )
            conv_matrix_1 = _sparse_array(
                (
                    values[:, -2:, :].ravel(),
                    (i_f[:, -2:, :].ravel(), i_c[:, -2:, :].ravel()),
                ),
                shape=(math.prod(shape_f_t), math.prod(shape_t)),
                format=format,
            )
        return conv_matrix_0, conv_bc[0], conv_matrix_1, conv_bc[1]

```
