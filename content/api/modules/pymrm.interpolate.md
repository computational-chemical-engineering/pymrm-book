# `pymrm.interpolate`

[Back to modules overview](../api.md)

Interpolation utilities between cell-centered and staggered grids.

[View module source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/0b0ac9e5d5a7ceb669718e3aafef1ebd9960b860/src/pymrm/interpolate.py)

## Public API

| Symbol | Type | Summary |
| ------ | ---- | ------- |
| [`compute_boundary_values`](../symbols/pymrm.interpolate.compute_boundary_values.md) | function | Compute boundary values and boundary-normal gradients. |
| [`construct_boundary_value_matrices`](../symbols/pymrm.interpolate.construct_boundary_value_matrices.md) | function | Build matrices that evaluate boundary values from cell-centered unknowns. |
| [`create_staggered_array`](../symbols/pymrm.interpolate.create_staggered_array.md) | function | Create a face/staggered field from scalar, centered, or staggered input. |
| [`interp_cntr_to_stagg`](../symbols/pymrm.interpolate.interp_cntr_to_stagg.md) | function | Interpolate cell-centered values to face/staggered locations. |
| [`interp_cntr_to_stagg_tvd`](../symbols/pymrm.interpolate.interp_cntr_to_stagg_tvd.md) | function | Perform TVD interpolation from cell centers to faces. |
| [`interp_stagg_to_cntr`](../symbols/pymrm.interpolate.interp_stagg_to_cntr.md) | function | Interpolate face/staggered values to cell centers. |

## `compute_boundary_values(cell_centered_values, x_f, x_c = None, bc = None, axis = 0, bound_id = None)`

[Open dedicated reference page](../symbols/pymrm.interpolate.compute_boundary_values.md)

Compute boundary values and boundary-normal gradients.

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

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/0b0ac9e5d5a7ceb669718e3aafef1ebd9960b860/src/pymrm/interpolate.py#L363-L574)

## `construct_boundary_value_matrices(shape, x_f, x_c = None, bc = None, axis = 0, bound_id = 0, shape_d = None, format = 'csc')`

[Open dedicated reference page](../symbols/pymrm.interpolate.construct_boundary_value_matrices.md)

Build matrices that evaluate boundary values from cell-centered unknowns.

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

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/0b0ac9e5d5a7ceb669718e3aafef1ebd9960b860/src/pymrm/interpolate.py#L577-L722)

## `create_staggered_array(array, shape, axis, x_f = None, x_c = None)`

[Open dedicated reference page](../symbols/pymrm.interpolate.create_staggered_array.md)

Create a face/staggered field from scalar, centered, or staggered input.

### Parameters

- `array` (*array_like*)
  Input values. May be scalar, centered, or already staggered.

- `shape` (*tuple[int, ...] or int*)
  Target centered-field shape.

- `axis` (*int*)
  Staggering axis.

- `x_f, x_c` (*array_like, optional*)
  Face and center coordinates used when centered input must be
  interpolated to faces.

### Returns

- `numpy.ndarray`
  Broadcasted/interpolated array with staggered shape.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/0b0ac9e5d5a7ceb669718e3aafef1ebd9960b860/src/pymrm/interpolate.py#L306-L360)

## `interp_cntr_to_stagg(cell_centered_values, x_f, x_c = None, axis = 0)`

[Open dedicated reference page](../symbols/pymrm.interpolate.interp_cntr_to_stagg.md)

Interpolate cell-centered values to face/staggered locations.

### Parameters

- `cell_centered_values` (*numpy.ndarray*)
  Values defined at cell centers.

- `x_f` (*array_like*)
  Face coordinates along ``axis``.

- `x_c` (*array_like, optional*)
  Cell-center coordinates. If omitted, midpoint locations are used.

- `axis` (*int, optional*)
  Interpolation axis.

### Returns

- `numpy.ndarray`
  Staggered values with one additional element along ``axis``.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/0b0ac9e5d5a7ceb669718e3aafef1ebd9960b860/src/pymrm/interpolate.py#L53-L104)

## `interp_cntr_to_stagg_tvd(cell_centered_values, x_f, x_c = None, bc = None, v = 0, tvd_limiter = None, axis = 0)`

[Open dedicated reference page](../symbols/pymrm.interpolate.interp_cntr_to_stagg_tvd.md)

Perform TVD interpolation from cell centers to faces.

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

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/0b0ac9e5d5a7ceb669718e3aafef1ebd9960b860/src/pymrm/interpolate.py#L107-L303)

## `interp_stagg_to_cntr(staggered_values, x_f, x_c = None, axis = 0)`

[Open dedicated reference page](../symbols/pymrm.interpolate.interp_stagg_to_cntr.md)

Interpolate face/staggered values to cell centers.

### Parameters

- `staggered_values` (*numpy.ndarray*)
  Values defined on staggered (face) locations.

- `x_f` (*array_like*)
  Face coordinates along ``axis``.

- `x_c` (*array_like, optional*)
  Cell-center coordinates. If omitted, midpoint interpolation is used.

- `axis` (*int, optional*)
  Interpolation axis.

### Returns

- `numpy.ndarray`
  Cell-centered values with one fewer element along ``axis``.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/0b0ac9e5d5a7ceb669718e3aafef1ebd9960b860/src/pymrm/interpolate.py#L9-L50)
