# `pymrm.interpolate.compute_boundary_values`

[Back to module page](../modules/pymrm.interpolate.md) · [Back to alphabetical overview](../alphabetical_overview.md)

## Signature

`compute_boundary_values(cell_centered_values, x_f, x_c = None, bc = None, axis = 0, bound_id = None)`

## Summary

Compute boundary values and boundary-normal gradients.

## Documentation

### Parameters

- `cell_centered_values` (*numpy.ndarray*)
  Cell-centered solution values.

- `x_f` (*array_like*)
  Face coordinates along ``axis``.

- `x_c` (*array_like, optional*)
  Cell-center coordinates.

- `bc` (*dict or tuple[dict | None, dict | None], optional*)
  Boundary-condition data. For a single boundary query (``bound_id`` set),
  a single dictionary is accepted. For both boundaries, pass a
  two-element tuple.

- `axis` (*int, optional*)
  Axis normal to the boundary.

- `bound_id` (*{0, 1} or None, optional*)
  Boundary selector. ``None`` returns both boundaries.

### Returns

- `tuple`
  If ``bound_id`` is ``None``:
  ``(value_left, grad_left, value_right, grad_right)``.
  Otherwise: ``(value, grad)`` for the requested boundary.

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/0b0ac9e5d5a7ceb669718e3aafef1ebd9960b860/src/pymrm/interpolate.py#L363-L574)

```python
def compute_boundary_values(
    cell_centered_values, x_f, x_c=None, bc=None, axis=0, bound_id=None
):
    """Compute boundary values and boundary-normal gradients.

    Parameters
    ----------
    cell_centered_values : numpy.ndarray
        Cell-centered solution values.
    x_f : array_like
        Face coordinates along ``axis``.
    x_c : array_like, optional
        Cell-center coordinates.
    bc : dict or tuple[dict | None, dict | None], optional
        Boundary-condition data. For a single boundary query (``bound_id`` set),
        a single dictionary is accepted. For both boundaries, pass a
        two-element tuple.
    axis : int, optional
        Axis normal to the boundary.
    bound_id : {0, 1} or None, optional
        Boundary selector. ``None`` returns both boundaries.

    Returns
    -------
    tuple
        If ``bound_id`` is ``None``:
        ``(value_left, grad_left, value_right, grad_right)``.
        Otherwise: ``(value, grad)`` for the requested boundary.
    """
    shape = list(cell_centered_values.shape)
    if axis < 0:
        axis += len(shape)
    shape_t = [
        math.prod(shape[:axis]),
        math.prod(shape[axis: axis + 1]),
        math.prod(shape[axis + 1:]),
    ]  # reshape as a triplet
    shape_b_t = shape_t.copy()
    shape_b_t[1] = 2
    shape_bc = shape.copy()
    shape_bc[axis] = 1
    shape_bc_d = [shape_t[0], shape_t[2]]
    cell_centered_values = cell_centered_values.reshape(shape_t)

    if bound_id is None:
        bounds = [0, 1]
    else:
        bounds = [bound_id]

    if bound_id is None or shape_t[1] == 1:
        if bc is None:
            bc = ({"a": 0, "b": 0, "d": 0}, {"a": 0, "b": 0, "d": 0})
        elif not isinstance(bc, tuple) and len(bc) != 2:
            raise ValueError(
                "Boundary conditions must be a tuple of 2 dictionaries when 2 boundary conditions are required."
            )
        if bc[0] is None:
            bc[0] = {"a": 0, "b": 0, "d": 0}
        if bc[1] is None:
            bc[1] = {"a": 0, "b": 0, "d": 0}
    else:
        if bc is None:
            bc = {"a": 0, "b": 0, "d": 0}
        if bound_id == 0:
            bc = (bc, None)
        else:
            bc = (None, bc)

    boundary_values = [None, None]
    boundary_grads = [None, None]

    if shape_t[1] == 1:
        if x_c is None:
            x_c = 0.5 * (x_f[:-1] + x_f[1:])
        a, b, d = [
            [
                (
                    unwrap_bc_coeff(shape, bc_elem[key], axis=axis)
                    if bc_elem
                    else np.zeros((1,) * len(shape))
                )
                for bc_elem in bc
            ]
            for key in ["a", "b", "d"]
        ]
        alpha_1 = (x_f[1] - x_f[0]) / ((x_c[0] - x_f[0]) * (x_f[1] - x_c[0]))
        alpha_2 = [
            (x_c[0] - x_f[0]) / ((x_f[1] - x_f[0]) * (x_f[1] - x_c[0])),
            -(x_c[0] - x_f[1]) / ((x_f[0] - x_f[1]) * (x_f[0] - x_c[0])),
        ]
        alpha_0 = [alpha_1 - alpha_2[0], alpha_1 - alpha_2[1]]

        fctr = (b[0] + alpha_0[0] * a[0]) * (b[1] + alpha_0[1] * a[1]) - alpha_2[
            0
        ] * alpha_2[1] * a[0] * a[1]
        np.divide(1, fctr, out=fctr, where=(fctr != 0))

        for i in bounds:
            if i == 0:
                j = 1
                sgn = 1
            else:
                j = 0
                sgn = -1
            fctr_i = alpha_1 * (a[j] * (alpha_0[j] - alpha_2[i]) + b[j]) * fctr
            fctr_m = a[i] * fctr_i
            fctr_m = np.broadcast_to(fctr_m, shape_bc)
            fctr_m = np.reshape(fctr_m, shape_bc_d)
            boundary_values[i] = fctr_m * cell_centered_values[:, 0, :]
            fctr_m = b[i] * fctr_i
            fctr_m = np.broadcast_to(fctr_m, shape_bc)
            fctr_m = np.reshape(fctr_m, shape_bc_d)
            boundary_grads[i] = sgn * fctr_m * cell_centered_values[:, 0, :]

            fctr_m = (
                (a[j] * alpha_0[j] + b[j]) * d[i] - alpha_2[i] * a[i] * d[j]
            ) * fctr
            fctr_m = np.broadcast_to(fctr_m, shape_bc)
            fctr_m = np.reshape(fctr_m, shape_bc_d)
            boundary_values[i][...] += fctr_m
            fctr_m = (
                (
                    a[j] * (-alpha_0[i] * alpha_0[j] + alpha_2[i] * alpha_2[j])
                    - alpha_0[i] * b[j]
                )
                * d[i]
                - alpha_2[i] * b[i] * d[j]
            ) * fctr
            fctr_m = np.broadcast_to(fctr_m, shape_bc)
            fctr_m = np.reshape(fctr_m, shape_bc_d)
            boundary_grads[i][...] += sgn * fctr_m
            boundary_values[i] = boundary_values[i].reshape(shape_bc)
            boundary_grads[i] = boundary_grads[i].reshape(shape_bc)
    else:
        if x_c is None:
            x_c = np.concatenate(
                (0.5 * (x_f[0:2] + x_f[1:3]), 0.5 * (x_f[-3:-1] + x_f[-2:]))
            )
        for i in bounds:
            if i == 0:
                j = 1
                sgn = 1
                idx_0 = 0
                idx_1 = 1
            else:
                j = 0
                sgn = -1
                idx_0 = -1
                idx_1 = -2

            a, b, d = [
                (
                    unwrap_bc_coeff(shape, bc[i][key], axis=axis)
                    if bc[i]
                    else np.zeros((1,) * len(shape))
                )
                for key in ["a", "b", "d"]
            ]
            alpha_1 = (x_c[idx_1] - x_f[idx_0]) / (
                (x_c[idx_0] - x_f[idx_0]) * (x_c[idx_1] - x_c[idx_0])
            )
            alpha_2 = (x_c[idx_0] - x_f[idx_0]) / (
                (x_c[idx_1] - x_f[idx_0]) * (x_c[idx_1] - x_c[idx_0])
            )
            alpha_0 = alpha_1 - alpha_2
            a *= sgn
            fctr = alpha_0 * a + b
            np.divide(1, fctr, out=fctr, where=(fctr != 0))
            a_fctr = a * fctr
            a_fctr = np.broadcast_to(a_fctr, shape_bc)
            a_fctr = np.reshape(a_fctr, shape_bc_d)
            b_fctr = b * fctr
            b_fctr = np.broadcast_to(b_fctr, shape_bc)
            b_fctr = np.reshape(b_fctr, shape_bc_d)
            d_fctr = d * fctr
            d_fctr = np.broadcast_to(d_fctr, shape_bc)
            d_fctr = np.reshape(d_fctr, shape_bc_d)
            boundary_values[i] = d_fctr + a_fctr * (
                alpha_1 * cell_centered_values[:, idx_0, :]
                - alpha_2 * cell_centered_values[:, idx_1, :]
            )
            boundary_grads[i] = -alpha_0 * d_fctr + b_fctr * (
                alpha_1 * cell_centered_values[:, idx_0, :]
                - alpha_2 * cell_centered_values[:, idx_1, :]
            )
            if np.any(fctr == 0.0):
                fltr = np.reshape(np.broadcast_to((fctr == 0.0), shape_bc), shape_bc_d)
                boundary_values[i][fltr] = (
                    (x_c[idx_1] - x_f[idx_0]) / (x_c[idx_1] - x_c[idx_0])
                ) * cell_centered_values[:, idx_0, :][fltr] + (
                    (x_c[idx_0] - x_f[idx_0]) / (x_c[idx_0] - x_c[idx_1])
                ) * cell_centered_values[
                    :, idx_1, :
                ][
                    fltr
                ]
                boundary_grads[i][fltr] = (1.0 / (x_c[idx_1] - x_c[idx_0])) * (
                    cell_centered_values[:, idx_1, :][fltr]
                    - cell_centered_values[:, idx_0, :][fltr]
                )
            boundary_values[i] = boundary_values[i].reshape(shape_bc)
            boundary_grads[i] = boundary_grads[i].reshape(shape_bc)

    if bound_id is None:
        return (
            boundary_values[0],
            boundary_grads[0],
            boundary_values[1],
            boundary_grads[1],
        )
    else:
        return boundary_values[bound_id], boundary_grads[bound_id]
```
