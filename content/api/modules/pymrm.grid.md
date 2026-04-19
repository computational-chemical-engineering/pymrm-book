# `pymrm.grid`

[Back to modules overview](../api.md)

Grid-generation utilities for one-dimensional coordinates.

[View module source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/0b0ac9e5d5a7ceb669718e3aafef1ebd9960b860/src/pymrm/grid.py)

## Public API

| Symbol | Type | Summary |
| ------ | ---- | ------- |
| [`generate_grid`](../symbols/pymrm.grid.generate_grid.md) | function | Return face coordinates and optionally cell-center coordinates. |
| [`non_uniform_grid`](../symbols/pymrm.grid.non_uniform_grid.md) | function | Generate a one-dimensional stretched face grid. |

## `generate_grid(size, x_f = None, generate_x_c = False, x_c = None)`

[Open dedicated reference page](../symbols/pymrm.grid.generate_grid.md)

Return face coordinates and optionally cell-center coordinates.

### Parameters

- `size` (*int*)
  Number of cells along the axis.

- `x_f` (*array_like, optional*)
  Face coordinates. Accepted inputs are:

  * ``None`` or an empty array: build a uniform grid on ``[0, 1]``;
  * an array of length ``size + 1``: interpreted directly as face
    coordinates;
  * an array-like of length ``2``: interpreted as ``(xmin, xmax)`` and
    used to build a uniform grid.

- `generate_x_c` (*bool, optional*)
  If ``True``, also return cell-center coordinates.

- `x_c` (*array_like, optional*)
  Explicit cell-center coordinates. When provided, length must equal
  ``size``.

### Returns

- `numpy.ndarray or tuple[numpy.ndarray, numpy.ndarray]`
  Face coordinates, and optionally cell-center coordinates.

### Raises

- `ValueError`
  If provided coordinates are inconsistent with ``size``.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/0b0ac9e5d5a7ceb669718e3aafef1ebd9960b860/src/pymrm/grid.py#L35-L87)

## `non_uniform_grid(left_bound, right_bound, num_points, dx_inf, factor)`

[Open dedicated reference page](../symbols/pymrm.grid.non_uniform_grid.md)

Generate a one-dimensional stretched face grid.

### Parameters

- `left_bound, right_bound` (*float*)
  Domain bounds.

- `num_points` (*int*)
  Number of returned face coordinates, including both boundaries.

- `dx_inf` (*float*)
  Asymptotic cell width used in the stretching expression.

- `factor` (*float*)
  Geometric stretching factor. Values larger than ``1`` stretch cells;
  values between ``0`` and ``1`` compress cells.

### Returns

- `numpy.ndarray`
  Monotonic array of face coordinates with length ``num_points``.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/0b0ac9e5d5a7ceb669718e3aafef1ebd9960b860/src/pymrm/grid.py#L6-L32)
