# `pymrm.operators.construct_grad_bc`

[Back to module page](../modules/pymrm.operators) · [Back to alphabetical overview](../alphabetical_overview)

## Signature

`construct_grad_bc(shape, x_f, x_c = None, bc = (None, None), axis = 0, shapes_d = (None, None), format = 'csc')`

## Summary

Construct boundary-face gradient corrections and source terms.

## Documentation

### Parameters

- `shape` (*tuple[int, ...]*)
  Cell-centered field shape.

- `x_f` (*array_like*)
  Face coordinates along ``axis``.

- `x_c` (*array_like, optional*)
  Cell-center coordinates.

- `bc` (*tuple[dict | None, dict | None], optional*)
  Left and right boundary-condition dictionaries with keys ``a``, ``b``,
  and ``d``.

- `axis` (*int, optional*)
  Differentiation axis.

- `shapes_d` (*tuple[tuple | None, tuple | None], optional*)
  Optional source-vector shapes for left/right boundary contributions.

- `format` (*{'csc', 'csr'}, optional*)
  Sparse format for returned operator matrices.

### Returns

- `tuple`
  ``(grad_matrix_bc, grad_bc)`` when ``shapes_d`` is not supplied, or
  ``(grad_matrix_left, grad_bc_left, grad_matrix_right, grad_bc_right)``
  otherwise.

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/0b0ac9e5d5a7ceb669718e3aafef1ebd9960b860/src/pymrm/operators.py#L156-L397)

```python
def construct_grad_bc(
    shape, x_f, x_c=None, bc=(None, None), axis=0, shapes_d=(None, None), format="csc"
):
    """Construct boundary-face gradient corrections and source terms.

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
    axis : int, optional
        Differentiation axis.
    shapes_d : tuple[tuple | None, tuple | None], optional
        Optional source-vector shapes for left/right boundary contributions.
    format : {'csc', 'csr'}, optional
        Sparse format for returned operator matrices.

    Returns
    -------
    tuple
        ``(grad_matrix_bc, grad_bc)`` when ``shapes_d`` is not supplied, or
        ``(grad_matrix_left, grad_bc_left, grad_matrix_right, grad_bc_right)``
        otherwise.
    """
    shape_f = shape[:axis] + (shape[axis] + 1,) + shape[axis + 1:]
    shape_t = (math.prod(shape[:axis]), shape[axis], math.prod(shape[axis + 1:]))
    shape_f_t = (shape_t[0], shape_f[axis], shape_t[2])
    shape_bc = shape[:axis] + (1,) + shape[axis + 1:]
    shape_bc_d = (shape_t[0], shape_t[2])

    # Handle special case with one cell in the dimension axis.
    # This is convenient e.g. for flexibility where you can choose not to
    # spatially discretize a direction, but still use a BC, e.g. with a mass transfer coefficient
    # It is a bit subtle because in this case the two opposite faces influence each other
    n0, n1, n2 = shape_t
    i0 = np.arange(n0).reshape(-1, 1, 1)
    i2 = np.arange(n2).reshape(1, 1, -1)

    if n1 == 1:
        if x_c is None:
            x_c = 0.5 * (x_f[0:-1] + x_f[1:])
        # Both faces reference cell 0
        i_c = np.ravel_multi_index(
            (i0, np.array([0, 0]).reshape(1, -1, 1), i2), (n0, n1, n2)
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
        fctr = (b[0] + alpha_0_left * a[0]) * (
            b[1] + alpha_0_right * a[1]
        ) - alpha_2_left * alpha_2_right * a[0] * a[1]
        np.divide(1, fctr, out=fctr, where=(fctr != 0))
        value = np.broadcast_to(
            alpha_1 * b[0] * (a[1] * (alpha_0_right - alpha_2_left) + b[1]) * fctr,
            shape,
        )
        values[:, 0, :] = np.reshape(value, shape_bc_d)
        value = np.broadcast_to(
            alpha_1 * b[1] * (a[0] * (-alpha_0_left + alpha_2_right) - b[0]) * fctr,
            shape,
        )
        values[:, 1, :] = np.reshape(value, shape_bc_d)

        i_f_bc = np.ravel_multi_index(
            (i0, np.array([0, shape_f_t[1] - 1]).reshape(1, -1, 1), i2), shape_f_t
        )
        values_bc = np.empty((n0, 2, n2))
        value = np.broadcast_to(
            (
                (
                    a[1]
                    * (-alpha_0_left * alpha_0_right + alpha_2_left * alpha_2_right)
                    - alpha_0_left * b[1]
                )
                * d[0]
                - alpha_2_left * b[0] * d[1]
            )
            * fctr,
            shape_bc,
        )
        values_bc[:, 0, :] = np.reshape(value, shape_bc_d)
        value = np.broadcast_to(
            (
                (
                    a[0]
                    * (+alpha_0_left * alpha_0_right - alpha_2_left * alpha_2_right)
                    + alpha_0_right * b[0]
                )
                * d[1]
                + alpha_2_right * b[1] * d[0]
            )
            * fctr,
            shape_bc,
        )
        values_bc[:, 1, :] = np.reshape(value, shape_bc_d)
    else:
        # Cell indices: 2 near left boundary + 2 near right boundary
        cell_axis_idx = np.array([0, 1, n1 - 2, n1 - 1]).reshape(1, -1, 1)
        i_c = np.ravel_multi_index((i0, cell_axis_idx, i2), shape_t)
        # Face indices: left face (0) twice, right face (n1) twice
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
        alpha_1 = (x_c[1] - x_f[0]) / ((x_c[0] - x_f[0]) * (x_c[1] - x_c[0]))
        alpha_2 = (x_c[0] - x_f[0]) / ((x_c[1] - x_f[0]) * (x_c[1] - x_c[0]))
        alpha_0 = alpha_1 - alpha_2
        a, b, d = [
            (
                unwrap_bc_coeff(shape, bc[0][key], axis=axis)
                if bc[0]
                else np.zeros((1,) * len(shape))
            )
            for key in ["a", "b", "d"]
        ]
        b = b / alpha_0
        fctr = a + b
        np.divide(1, fctr, out=fctr, where=(fctr != 0))
        b_fctr = b * fctr
        b_fctr = np.broadcast_to(b_fctr, shape_bc).reshape(shape_bc_d)
        d_fctr = d * fctr
        d_fctr = np.broadcast_to(d_fctr, shape_bc).reshape(shape_bc_d)
        values[:, 0, :] = b_fctr * alpha_1
        values[:, 1, :] = -b_fctr * alpha_2
        values_bc[:, 0, :] = -d_fctr

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
        b = b / alpha_0
        fctr = a + b
        np.divide(1, fctr, out=fctr, where=(fctr != 0))
        b_fctr = b * fctr
        b_fctr = np.broadcast_to(b_fctr, shape_bc).reshape(shape_bc_d)
        d_fctr = d * fctr
        d_fctr = np.broadcast_to(d_fctr, shape_bc).reshape(shape_bc_d)
        values[:, -2, :] = b_fctr * alpha_2
        values[:, -1, :] = -b_fctr * alpha_1
        values_bc[:, -1, :] = d_fctr
    if (shapes_d[0] is None) and (shapes_d[1] is None):
        grad_bc = csc_array(
            (values_bc.ravel(), i_f_bc.ravel(), np.array([0, i_f_bc.size])),
            shape=(math.prod(shape_f_t), 1),
        )
        grad_matrix = _sparse_array(
            (values.ravel(), (i_f.ravel(), i_c.ravel())),
            shape=(math.prod(shape_f_t), math.prod(shape_t)),
            format=format,
        )
        return grad_matrix, grad_bc
    else:
        grad_bc = [None] * 2
        for i in range(2):
            if shapes_d[i] is None:
                shape_d = (1,) * len(shape_bc)
                num_cols = 1
            else:
                shape_d = shapes_d[i]
                num_cols = math.prod(shape_d)
            i_cols_bc = np.arange(num_cols, dtype=int).reshape(shape_d)
            i_cols_bc = np.broadcast_to(i_cols_bc, shape_bc)
            grad_bc[i] = csc_array(
                (
                    values_bc[:, i, :].ravel(),
                    (i_f_bc[:, i, :].ravel(), i_cols_bc.ravel()),
                ),
                shape=(math.prod(shape_f_t), num_cols),
            )
        if shape_t[1] == 1:
            grad_matrix_0 = _sparse_array(
                (values[:, 0, :].ravel(), (i_f[:, 0, :].ravel(), i_c[:, 0, :].ravel())),
                shape=(math.prod(shape_f_t), math.prod(shape_t)),
                format=format,
            )
            grad_matrix_1 = _sparse_array(
                (
                    values[:, -1, :].ravel(),
                    (i_f[:, -1, :].ravel(), i_c[:, -1, :].ravel()),
                ),
                shape=(math.prod(shape_f_t), math.prod(shape_t)),
                format=format,
            )
        else:
            grad_matrix_0 = _sparse_array(
                (
                    values[:, :2, :].ravel(),
                    (i_f[:, :2, :].ravel(), i_c[:, :2, :].ravel()),
                ),
                shape=(math.prod(shape_f_t), math.prod(shape_t)),
                format=format,
            )
            grad_matrix_1 = _sparse_array(
                (
                    values[:, -2:, :].ravel(),
                    (i_f[:, -2:, :].ravel(), i_c[:, -2:, :].ravel()),
                ),
                shape=(math.prod(shape_f_t), math.prod(shape_t)),
                format=format,
            )
        return grad_matrix_0, grad_bc[0], grad_matrix_1, grad_bc[1]
```
