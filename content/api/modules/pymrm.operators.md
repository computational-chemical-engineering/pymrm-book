# `pymrm.operators`

[Back to modules overview](../api.md)

Sparse gradient and divergence operators for finite-volume discretisation.

[View module source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/0b0ac9e5d5a7ceb669718e3aafef1ebd9960b860/src/pymrm/operators.py)

## Public API

| Symbol | Type | Summary |
| ------ | ---- | ------- |
| [`construct_div`](../symbols/pymrm.operators.construct_div.md) | function | Construct a divergence matrix that maps face fluxes to cell balances. |
| [`construct_grad`](../symbols/pymrm.operators.construct_grad.md) | function | Construct the full gradient operator including boundary contributions. |
| [`construct_grad_bc`](../symbols/pymrm.operators.construct_grad_bc.md) | function | Construct boundary-face gradient corrections and source terms. |
| [`construct_grad_int`](../symbols/pymrm.operators.construct_grad_int.md) | function | Construct the interior-face gradient operator. |

## `construct_div(shape, x_f, nu = 0, axis = 0, format = 'csc')`

[Open dedicated reference page](../symbols/pymrm.operators.construct_div.md)

Construct a divergence matrix that maps face fluxes to cell balances.

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

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/0b0ac9e5d5a7ceb669718e3aafef1ebd9960b860/src/pymrm/operators.py#L400-L508)

## `construct_grad(shape, x_f, x_c = None, bc = (None, None), axis = 0, shapes_d = (None, None), format = 'csc')`

[Open dedicated reference page](../symbols/pymrm.operators.construct_grad.md)

Construct the full gradient operator including boundary contributions.

### Parameters

- `shape` (*tuple[int, ...] or int*)
  Cell-centered field shape.

- `x_f` (*array_like*)
  Face coordinates along ``axis``.

- `x_c` (*array_like, optional*)
  Cell-center coordinates along ``axis``. If omitted, they are generated
  as arithmetic midpoints.

- `bc` (*tuple[dict | None, dict | None], optional*)
  Left and right boundary-condition dictionaries with coefficients
  ``'a'``, ``'b'``, and ``'d'``.

- `axis` (*int, optional*)
  Differentiation axis.

- `shapes_d` (*tuple[tuple | None, tuple | None], optional*)
  Optional output shapes for inhomogeneous boundary source vectors.

- `format` (*{'csc', 'csr'}, optional*)
  Sparse format used for returned operator matrices.

### Returns

- `tuple`
  Without ``shapes_d``: ``(grad_matrix, grad_bc)``.
  With ``shapes_d``: ``(grad_matrix, grad_bc_left, grad_bc_right)``.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/0b0ac9e5d5a7ceb669718e3aafef1ebd9960b860/src/pymrm/operators.py#L10-L65)

## `construct_grad_bc(shape, x_f, x_c = None, bc = (None, None), axis = 0, shapes_d = (None, None), format = 'csc')`

[Open dedicated reference page](../symbols/pymrm.operators.construct_grad_bc.md)

Construct boundary-face gradient corrections and source terms.

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

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/0b0ac9e5d5a7ceb669718e3aafef1ebd9960b860/src/pymrm/operators.py#L156-L397)

## `construct_grad_int(shape, x_f, x_c = None, axis = 0, format = 'csc')`

[Open dedicated reference page](../symbols/pymrm.operators.construct_grad_int.md)

Construct the interior-face gradient operator.

### Parameters

- `shape` (*tuple[int, ...]*)
  Cell-centered field shape.

- `x_f` (*array_like*)
  Face coordinates along ``axis``.

- `x_c` (*array_like, optional*)
  Cell-center coordinates. If omitted, arithmetic midpoints are used.

- `axis` (*int, optional*)
  Differentiation axis.

- `format` (*{'csc', 'csr'}, optional*)
  Output sparse format.

### Returns

- `scipy.sparse.csc_array or scipy.sparse.csr_array`
  Matrix that maps cell-centered values to face-normal gradients.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/0b0ac9e5d5a7ceb669718e3aafef1ebd9960b860/src/pymrm/operators.py#L68-L153)
