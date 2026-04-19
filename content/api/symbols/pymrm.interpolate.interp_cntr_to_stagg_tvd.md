# `pymrm.interpolate.interp_cntr_to_stagg_tvd`

[Back to module page](../modules/pymrm.interpolate) · [Back to alphabetical overview](../alphabetical_overview)

## Signature

`interp_cntr_to_stagg_tvd(cell_centered_values, x_f, x_c = None, bc = None, v = 0, tvd_limiter = None, axis = 0)`

## Summary

Perform TVD interpolation from cell centers to faces.

## Documentation

### Parameters

- `cell_centered_values` (*numpy.ndarray*)
  Cell-centered values.

- `x_f` (*array_like*)
  Face coordinates along ``axis``.

- `x_c` (*array_like, optional*)
  Cell-center coordinates. If omitted, midpoint locations are used.

- `bc` (*tuple[dict | None, dict | None], optional*)
  Left and right boundary-condition dictionaries with keys ``a``, ``b``,
  and ``d``.

- `v` (*float or array_like, optional*)
  Face velocity used to determine upwind/downwind directions.

- `tvd_limiter` (*callable, optional*)
  Limiter function with signature ``phi(c_norm, x_norm_c, x_norm_d)``. If
  ``None``, the routine returns linear upwind interpolation without TVD
  correction.

- `axis` (*int, optional*)
  Interpolation axis.

### Returns

- `tuple[numpy.ndarray, numpy.ndarray]`
  Interpolated staggered values and TVD correction term.

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/0b0ac9e5d5a7ceb669718e3aafef1ebd9960b860/src/pymrm/interpolate.py#L107-L303)

```python
def interp_cntr_to_stagg_tvd(
    cell_centered_values, x_f, x_c=None, bc=None, v=0, tvd_limiter=None, axis=0
):
    """Perform TVD interpolation from cell centers to faces.

    Parameters
    ----------
    cell_centered_values : numpy.ndarray
        Cell-centered values.
    x_f : array_like
        Face coordinates along ``axis``.
    x_c : array_like, optional
        Cell-center coordinates. If omitted, midpoint locations are used.
    bc : tuple[dict | None, dict | None], optional
        Left and right boundary-condition dictionaries with keys ``a``, ``b``,
        and ``d``.
    v : float or array_like, optional
        Face velocity used to determine upwind/downwind directions.
    tvd_limiter : callable, optional
        Limiter function with signature ``phi(c_norm, x_norm_c, x_norm_d)``. If
        ``None``, the routine returns linear upwind interpolation without TVD
        correction.
    axis : int, optional
        Interpolation axis.

    Returns
    -------
    tuple[numpy.ndarray, numpy.ndarray]
        Interpolated staggered values and TVD correction term.
    """
    shape = list(cell_centered_values.shape)
    if axis < 0:
        axis += len(shape)
    shape_t = [
        math.prod(shape[:axis]),
        math.prod(shape[axis: axis + 1]),
        math.prod(shape[axis + 1:]),
    ]  # reshape as a triplet
    shape_f = shape.copy()
    shape_f[axis] = shape[axis] + 1
    shape_f_t = shape_t.copy()
    shape_f_t[1] = shape_f[axis]
    shape_bc = shape_f.copy()
    shape_bc[axis] = 1
    shape_bc_d = [shape_t[0], shape_t[2]]

    if x_c is None:
        x_c = 0.5 * (x_f[:-1] + x_f[1:])
    cell_centered_values = cell_centered_values.reshape(shape_t)
    staggered_values = np.empty(shape_f_t)

    if shape_t[1] == 1:
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
        alpha_2_left = (x_c[0] - x_f[0]) / ((x_f[1] - x_f[0]) * (x_f[1] - x_c[0]))
        alpha_0_left = alpha_1 - alpha_2_left
        alpha_2_right = -(x_c[0] - x_f[1]) / ((x_f[0] - x_f[1]) * (x_f[0] - x_c[0]))
        alpha_0_right = alpha_1 - alpha_2_right
        fctr = (b[0] + alpha_0_left * a[0]) * (
            b[1] + alpha_0_right * a[1]
        ) - alpha_2_left * alpha_2_right * a[0] * a[1]
        np.divide(1, fctr, out=fctr, where=(fctr != 0))
        fctr_m = alpha_1 * a[0] * (a[1] * (alpha_0_right - alpha_2_left) + b[1]) * fctr
        fctr_m = fctr_m + np.zeros(shape_bc)
        fctr_m = np.reshape(fctr_m, shape_bc_d)
        staggered_values[:, 0, :] = fctr_m * cell_centered_values[:, 0, :]
        fctr_m = alpha_1 * a[1] * (a[0] * (alpha_0_left - alpha_2_right) + b[0]) * fctr
        fctr_m = fctr_m + np.zeros(shape_bc)
        fctr_m = np.reshape(fctr_m, shape_bc_d)
        staggered_values[:, 1, :] = fctr_m * cell_centered_values[:, 0, :]
        fctr_m = (
            (a[1] * alpha_0_right + b[1]) * d[0] - alpha_2_left * a[0] * d[1]
        ) * fctr
        fctr_m = fctr_m + np.zeros(shape_bc)
        fctr_m = np.reshape(fctr_m, shape_bc_d)
        staggered_values[:, 0, :] += fctr_m
        fctr_m = (
            (a[0] * alpha_0_left + b[0]) * d[1] - alpha_2_right * a[1] * d[0]
        ) * fctr
        fctr_m = fctr_m + np.zeros(shape_bc)
        fctr_m = np.reshape(fctr_m, shape_bc_d)
        staggered_values[:, 1, :] += fctr_m
        staggered_values.reshape(shape_f)
        delta_staggered_values = np.zeros(shape_f)
    else:
        # bc 0
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
        a_fctr = a_fctr + np.zeros(shape_bc)
        a_fctr = np.reshape(a_fctr, shape_bc_d)
        d_fctr = d * fctr
        d_fctr = d_fctr + np.zeros(shape_bc)
        d_fctr = np.reshape(d_fctr, shape_bc_d)
        staggered_values[:, 0, :] = d_fctr + a_fctr * (
            alpha_1 * cell_centered_values[:, 0, :]
            - alpha_2 * cell_centered_values[:, 1, :]
        )
        # bc 1
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
        a_fctr = a_fctr + np.zeros(shape_bc)
        a_fctr = np.reshape(a_fctr, shape_bc_d)
        d_fctr = d * fctr
        d_fctr = d_fctr + np.zeros(shape_bc)
        d_fctr = np.reshape(d_fctr, shape_bc_d)
        staggered_values[:, -1, :] = d_fctr + a_fctr * (
            alpha_1 * cell_centered_values[:, -1, :]
            - alpha_2 * cell_centered_values[:, -2, :]
        )

        v = np.broadcast_to(np.asarray(v), shape_f)
        v_t = v.reshape(shape_f_t)
        fltr_v_pos = v_t > 0

        x_f = x_f.reshape((1, -1, 1))
        x_c = x_c.reshape((1, -1, 1))
        x_d = x_f[:, 1:-1, :]
        x_C = (
            fltr_v_pos[:, 1:-1, :] * x_c[:, :-1, :]
            + ~fltr_v_pos[:, 1:-1, :] * x_c[:, 1:, :]
        )
        x_U = fltr_v_pos[:, 1:-1, :] * np.concatenate(
            (x_f[:, 0:1, :], x_c[:, 0:-2, :]), axis=1
        ) + ~fltr_v_pos[:, 1:-1, :] * np.concatenate(
            (x_c[:, 2:, :], x_f[:, -1:, :]), axis=1
        )
        x_D = (
            fltr_v_pos[:, 1:-1, :] * x_c[:, 1:, :]
            + ~fltr_v_pos[:, 1:-1, :] * x_c[:, :-1, :]
        )
        x_norm_C = (x_C - x_U) / (x_D - x_U)
        x_norm_d = (x_d - x_U) / (x_D - x_U)
        c_C = (
            fltr_v_pos[:, 1:-1, :] * cell_centered_values[:, :-1, :]
            + ~fltr_v_pos[:, 1:-1, :] * cell_centered_values[:, 1:, :]
        )
        c_U = fltr_v_pos[:, 1:-1, :] * np.concatenate(
            (staggered_values[:, 0:1, :], cell_centered_values[:, 0:-2, :]), axis=1
        ) + ~fltr_v_pos[:, 1:-1, :] * np.concatenate(
            (cell_centered_values[:, 2:, :], staggered_values[:, -1:, :]), axis=1
        )
        c_D = (
            fltr_v_pos[:, 1:-1, :] * cell_centered_values[:, 1:, :]
            + ~fltr_v_pos[:, 1:-1, :] * cell_centered_values[:, :-1, :]
        )
        c_norm_C = np.zeros_like(c_C)
        dc_DU = c_D - c_U
        np.divide((c_C - c_U), dc_DU, out=c_norm_C, where=(dc_DU != 0))
        staggered_values = np.concatenate(
            (staggered_values[:, 0:1, :], c_C, staggered_values[:, -1:, :]), axis=1
        )
        if tvd_limiter is None:
            delta_staggered_values = np.zeros(shape_f)
            staggered_values = staggered_values.reshape(shape_f)
        else:
            delta_staggered_values = np.zeros(shape_f_t)
            delta_staggered_values[:, 1:-1, :] = (
                tvd_limiter(c_norm_C, x_norm_C, x_norm_d) * dc_DU
            )
            staggered_values += delta_staggered_values
            delta_staggered_values = delta_staggered_values.reshape(shape_f)
            staggered_values = staggered_values.reshape(shape_f)
    return staggered_values, delta_staggered_values
```
