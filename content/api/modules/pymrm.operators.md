# `pymrm.operators`

[Back to modules overview](../api)

Sparse gradient and divergence operators for finite-volume discretisation.

[View module source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/26b1cf19019672d855d525a0001f9d3c2a650e65/src/pymrm/operators.py)

## Public API

| Symbol | Type | Summary |
| ------ | ---- | ------- |
| [`construct_div`](../symbols/pymrm.operators.construct_div) | function | Construct a divergence matrix that maps face fluxes to cell balances. |
| [`construct_grad`](../symbols/pymrm.operators.construct_grad) | function | Construct the full gradient operator including boundary contributions. |
| [`construct_grad_bc`](../symbols/pymrm.operators.construct_grad_bc) | function | Construct boundary-face gradient corrections and source terms. |
| [`construct_grad_int`](../symbols/pymrm.operators.construct_grad_int) | function | Construct the interior-face gradient operator. |

## `construct_div(shape, x_f, nu = 0, axis = 0, format = 'csc')`

[Open dedicated reference page](../symbols/pymrm.operators.construct_div)

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

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/26b1cf19019672d855d525a0001f9d3c2a650e65/src/pymrm/operators.py#L409-L517)

## `construct_grad(shape, x_f, x_c = None, bc = (None, None), axis = 0, shapes_d = (None, None), format = 'csc')`

[Open dedicated reference page](../symbols/pymrm.operators.construct_grad)

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
  ``'a'``, ``'b'``, and ``'d'`` for ``a * dc/dn + b * c = d`` with ``n``
  the outward normal. ``{"outflow": True}`` marks a pure-outflow
  boundary; for diffusion it means zero normal gradient.

- `axis` (*int, optional*)
  Differentiation axis.

- `shapes_d` (*tuple[tuple | None, tuple | None], optional*)
  Optional output shapes for inhomogeneous boundary source vectors. With
  ``shapes_d`` the dictionary's ``d`` is a coefficient on that external
  vector (use ``d = 1`` to pass values through the vector).

- `format` (*{'csc', 'csr'}, optional*)
  Sparse format used for returned operator matrices.

### Returns

- `tuple`
  Without ``shapes_d``: ``(grad_matrix, grad_bc)``.
  With ``shapes_d``: ``(grad_matrix, grad_bc_left, grad_bc_right)``.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/26b1cf19019672d855d525a0001f9d3c2a650e65/src/pymrm/operators.py#L10-L71)

## `construct_grad_bc(shape, x_f, x_c = None, bc = (None, None), axis = 0, shapes_d = (None, None), format = 'csc')`

[Open dedicated reference page](../symbols/pymrm.operators.construct_grad_bc)

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
  and ``d`` for ``a * dc/dn + b * c = d`` with ``n`` the outward normal;
  ``{"outflow": True}`` means zero normal gradient here.

- `axis` (*int, optional*)
  Differentiation axis.

- `shapes_d` (*tuple[tuple | None, tuple | None], optional*)
  Optional source-vector shapes for left/right boundary contributions;
  ``d`` is then a coefficient on the external vector.

- `format` (*{'csc', 'csr'}, optional*)
  Sparse format for returned operator matrices.

### Returns

- `tuple`
  ``(grad_matrix_bc, grad_bc)`` when ``shapes_d`` is not supplied, or
  ``(grad_matrix_left, grad_bc_left, grad_matrix_right, grad_bc_right)``
  otherwise.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/26b1cf19019672d855d525a0001f9d3c2a650e65/src/pymrm/operators.py#L162-L406)

## `construct_grad_int(shape, x_f, x_c = None, axis = 0, format = 'csc')`

[Open dedicated reference page](../symbols/pymrm.operators.construct_grad_int)

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

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/26b1cf19019672d855d525a0001f9d3c2a650e65/src/pymrm/operators.py#L74-L159)
