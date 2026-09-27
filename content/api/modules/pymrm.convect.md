# `pymrm.convect`

[Back to modules overview](../api)

Convective-flux operators and TVD limiter functions.

[View module source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/b40fd3f7ac82d247ea864dca2aec0b8aa53589a1/src/pymrm/convect.py)

## Public API

| Symbol | Type | Summary |
| ------ | ---- | ------- |
| [`clam`](../symbols/pymrm.convect.clam) | function | Compute the CLAM TVD correction in normalized-variable space. |
| [`construct_convflux_bc`](../symbols/pymrm.convect.construct_convflux_bc) | function | Construct boundary-face upwind corrections and source terms. |
| [`construct_convflux_upwind`](../symbols/pymrm.convect.construct_convflux_upwind) | function | Construct a first-order upwind convective-flux operator. |
| [`construct_convflux_upwind_int`](../symbols/pymrm.convect.construct_convflux_upwind_int) | function | Construct the internal-face upwind advection operator. |
| [`minmod`](../symbols/pymrm.convect.minmod) | function | Compute the Minmod TVD correction in normalized-variable space. |
| [`muscl`](../symbols/pymrm.convect.muscl) | function | Compute the MUSCL TVD correction in normalized-variable space. |
| [`osher`](../symbols/pymrm.convect.osher) | function | Compute the Osher TVD correction in normalized-variable space. |
| [`smart`](../symbols/pymrm.convect.smart) | function | Compute the SMART TVD correction in normalized-variable space. |
| [`stoic`](../symbols/pymrm.convect.stoic) | function | Compute the STOIC TVD correction in normalized-variable space. |
| [`upwind`](../symbols/pymrm.convect.upwind) | function | Return zero correction (first-order upwind limiter). |
| [`vanleer`](../symbols/pymrm.convect.vanleer) | function | Compute the van-Leer TVD correction in normalized-variable space. |

## `clam(normalized_c_c, normalized_x_c, normalized_x_d)`

[Open dedicated reference page](../symbols/pymrm.convect.clam)

Compute the CLAM TVD correction in normalized-variable space.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/b40fd3f7ac82d247ea864dca2aec0b8aa53589a1/src/pymrm/convect.py#L443-L453)

## `construct_convflux_bc(shape, x_f, x_c = None, bc = (None, None), v = 1.0, axis = 0, shapes_d = (None, None), format = 'csc')`

[Open dedicated reference page](../symbols/pymrm.convect.construct_convflux_bc)

Construct boundary-face upwind corrections and source terms.

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
  ``{"outflow": True}`` marks a pure-outflow boundary.

- `v` (*float or array_like, optional*)
  Face velocity field.

- `axis` (*int, optional*)
  Convection axis.

- `shapes_d` (*tuple[tuple | None, tuple | None], optional*)
  Optional source-vector shapes for inhomogeneous boundary terms; ``d``
  is then a coefficient on the external vector.

- `format` (*{'csc', 'csr'}, optional*)
  Sparse format for returned operator matrices.

### Returns

- `tuple`
  ``(conv_matrix_bc, conv_bc)`` when ``shapes_d`` is not supplied, or
  ``(conv_matrix_left, conv_bc_left, conv_matrix_right, conv_bc_right)``
  otherwise.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/b40fd3f7ac82d247ea864dca2aec0b8aa53589a1/src/pymrm/convect.py#L138-L406)

## `construct_convflux_upwind(shape, x_f, x_c = None, bc = (None, None), v = 1.0, axis = 0, shapes_d = (None, None), format = 'csc')`

[Open dedicated reference page](../symbols/pymrm.convect.construct_convflux_upwind)

Construct a first-order upwind convective-flux operator.

### Parameters

- `shape` (*tuple[int, ...] or int*)
  Cell-centered field shape.

- `x_f` (*array_like*)
  Face coordinates along ``axis``.

- `x_c` (*array_like, optional*)
  Cell-center coordinates. If omitted, arithmetic midpoints are used.

- `bc` (*tuple[dict | None, dict | None], optional*)
  Left and right boundary-condition dictionaries with keys ``a``, ``b``,
  and ``d`` for ``a * dc/dn + b * c = d`` with ``n`` the outward normal
  (at the left end ``dc/dn = -dc/dx``). ``{"outflow": True}`` marks a pure-outflow boundary: the
  face value is the adjacent cell value (a stirred volume's exit). It is
  meant for faces where material leaves; if flow enters there, the face
  still carries the adjacent cell value.

- `v` (*float or array_like, optional*)
  Face velocity field. Scalars and broadcastable arrays are accepted.

- `axis` (*int, optional*)
  Convection axis.

- `shapes_d` (*tuple[tuple | None, tuple | None], optional*)
  Optional source-vector shapes for boundary inhomogeneities. With
  ``shapes_d`` the dictionary's ``d`` is a coefficient on that external
  vector (use ``d = 1`` to pass the values through the vector).

- `format` (*{'csc', 'csr'}, optional*)
  Sparse format for returned operator matrices.

### Returns

- `tuple`
  Without ``shapes_d``: ``(conv_matrix, conv_bc)``.
  With ``shapes_d``: ``(conv_matrix, conv_bc_left, conv_bc_right)``.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/b40fd3f7ac82d247ea864dca2aec0b8aa53589a1/src/pymrm/convect.py#L11-L75)

## `construct_convflux_upwind_int(shape, v = 1.0, axis = 0, format = 'csc')`

[Open dedicated reference page](../symbols/pymrm.convect.construct_convflux_upwind_int)

Construct the internal-face upwind advection operator.

### Parameters

- `shape` (*tuple[int, ...]*)
  Cell-centered field shape.

- `v` (*float or array_like, optional*)
  Face velocity field.

- `axis` (*int, optional*)
  Convection axis.

- `format` (*{'csc', 'csr'}, optional*)
  Sparse format of the returned matrix.

### Returns

- `scipy.sparse.csc_array or scipy.sparse.csr_array`
  Sparse matrix mapping cell-centered values to interior face fluxes.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/b40fd3f7ac82d247ea864dca2aec0b8aa53589a1/src/pymrm/convect.py#L78-L135)

## `minmod(normalized_c_c, normalized_x_c, normalized_x_d)`

[Open dedicated reference page](../symbols/pymrm.convect.minmod)

Compute the Minmod TVD correction in normalized-variable space.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/b40fd3f7ac82d247ea864dca2aec0b8aa53589a1/src/pymrm/convect.py#L418-L427)

## `muscl(normalized_c_c, normalized_x_c, normalized_x_d)`

[Open dedicated reference page](../symbols/pymrm.convect.muscl)

Compute the MUSCL TVD correction in normalized-variable space.

Uniform grid: 2 c_c up to 1/4, c_c + 1/4 up to 3/4, then 1.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/b40fd3f7ac82d247ea864dca2aec0b8aa53589a1/src/pymrm/convect.py#L456-L475)

## `osher(normalized_c_c, normalized_x_c, normalized_x_d)`

[Open dedicated reference page](../symbols/pymrm.convect.osher)

Compute the Osher TVD correction in normalized-variable space.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/b40fd3f7ac82d247ea864dca2aec0b8aa53589a1/src/pymrm/convect.py#L430-L440)

## `smart(normalized_c_c, normalized_x_c, normalized_x_d)`

[Open dedicated reference page](../symbols/pymrm.convect.smart)

Compute the SMART TVD correction in normalized-variable space.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/b40fd3f7ac82d247ea864dca2aec0b8aa53589a1/src/pymrm/convect.py#L478-L509)

## `stoic(normalized_c_c, normalized_x_c, normalized_x_d)`

[Open dedicated reference page](../symbols/pymrm.convect.stoic)

Compute the STOIC TVD correction in normalized-variable space.

Piecewise: the SMART line ``c_f = k c_c`` up to its intersection with the
central-difference line, then central differencing up to ``c_c = x_c``,
then QUICK, then ``c_f = 1``. On a uniform grid (``x_c = 1/2``,
``x_d = 3/4``) this is 3 c_c, (1 + c_c)/2, 3/8 + 3 c_c/4 and 1, with breaks
at 1/5, 1/2 and 5/6.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/b40fd3f7ac82d247ea864dca2aec0b8aa53589a1/src/pymrm/convect.py#L512-L541)

## `upwind(normalized_c_c, normalized_x_c, normalized_x_d)`

[Open dedicated reference page](../symbols/pymrm.convect.upwind)

Return zero correction (first-order upwind limiter).

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/b40fd3f7ac82d247ea864dca2aec0b8aa53589a1/src/pymrm/convect.py#L412-L415)

## `vanleer(normalized_c_c, normalized_x_c, normalized_x_d)`

[Open dedicated reference page](../symbols/pymrm.convect.vanleer)

Compute the van-Leer TVD correction in normalized-variable space.

The curve is the parabola through (0, 0), (x_c, x_d) and (1, 1). It rises
above ``c_f = 1`` when ``x_d - x_c > x_c (1 - x_c)``, for example next to a
boundary where the upstream point is a face half a cell away (x_c = 1/3,
x_d = 2/3); the correction is capped at ``1 - c_c`` to stay bounded. The
cap acts only above c_c = x_c and does not reduce the order.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/b40fd3f7ac82d247ea864dca2aec0b8aa53589a1/src/pymrm/convect.py#L544-L563)
