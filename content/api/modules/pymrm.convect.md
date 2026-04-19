# `pymrm.convect`

[Back to modules overview](../api.md)

Convective-flux operators and TVD limiter functions.

[View module source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/0b0ac9e5d5a7ceb669718e3aafef1ebd9960b860/src/pymrm/convect.py)

## Public API

| Symbol | Type | Summary |
| ------ | ---- | ------- |
| [`clam`](../symbols/pymrm.convect.clam.md) | function | Compute the CLAM TVD correction in normalized-variable space. |
| [`construct_convflux_bc`](../symbols/pymrm.convect.construct_convflux_bc.md) | function | Construct boundary-face upwind corrections and source terms. |
| [`construct_convflux_upwind`](../symbols/pymrm.convect.construct_convflux_upwind.md) | function | Construct a first-order upwind convective-flux operator. |
| [`construct_convflux_upwind_int`](../symbols/pymrm.convect.construct_convflux_upwind_int.md) | function | Construct the internal-face upwind advection operator. |
| [`minmod`](../symbols/pymrm.convect.minmod.md) | function | Compute the Minmod TVD correction in normalized-variable space. |
| [`muscl`](../symbols/pymrm.convect.muscl.md) | function | Compute the MUSCL TVD correction in normalized-variable space. |
| [`osher`](../symbols/pymrm.convect.osher.md) | function | Compute the Osher TVD correction in normalized-variable space. |
| [`smart`](../symbols/pymrm.convect.smart.md) | function | Compute the SMART TVD correction in normalized-variable space. |
| [`stoic`](../symbols/pymrm.convect.stoic.md) | function | Compute the STOIC TVD correction in normalized-variable space. |
| [`upwind`](../symbols/pymrm.convect.upwind.md) | function | Return zero correction (first-order upwind limiter). |
| [`vanleer`](../symbols/pymrm.convect.vanleer.md) | function | Compute the van-Leer TVD correction in normalized-variable space. |

## `clam(normalized_c_c, normalized_x_c, normalized_x_d)`

[Open dedicated reference page](../symbols/pymrm.convect.clam.md)

Compute the CLAM TVD correction in normalized-variable space.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/0b0ac9e5d5a7ceb669718e3aafef1ebd9960b860/src/pymrm/convect.py#L423-L433)

## `construct_convflux_bc(shape, x_f, x_c = None, bc = (None, None), v = 1.0, axis = 0, shapes_d = (None, None), format = 'csc')`

[Open dedicated reference page](../symbols/pymrm.convect.construct_convflux_bc.md)

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
  and ``d``.

- `v` (*float or array_like, optional*)
  Face velocity field.

- `axis` (*int, optional*)
  Convection axis.

- `shapes_d` (*tuple[tuple | None, tuple | None], optional*)
  Optional source-vector shapes for inhomogeneous boundary terms.

- `format` (*{'csc', 'csr'}, optional*)
  Sparse format for returned operator matrices.

### Returns

- `tuple`
  ``(conv_matrix_bc, conv_bc)`` when ``shapes_d`` is not supplied, or
  ``(conv_matrix_left, conv_bc_left, conv_matrix_right, conv_bc_right)``
  otherwise.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/0b0ac9e5d5a7ceb669718e3aafef1ebd9960b860/src/pymrm/convect.py#L132-L386)

## `construct_convflux_upwind(shape, x_f, x_c = None, bc = (None, None), v = 1.0, axis = 0, shapes_d = (None, None), format = 'csc')`

[Open dedicated reference page](../symbols/pymrm.convect.construct_convflux_upwind.md)

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
  and ``d``.

- `v` (*float or array_like, optional*)
  Face velocity field. Scalars and broadcastable arrays are accepted.

- `axis` (*int, optional*)
  Convection axis.

- `shapes_d` (*tuple[tuple | None, tuple | None], optional*)
  Optional source-vector shapes for boundary inhomogeneities.

- `format` (*{'csc', 'csr'}, optional*)
  Sparse format for returned operator matrices.

### Returns

- `tuple`
  Without ``shapes_d``: ``(conv_matrix, conv_bc)``.
  With ``shapes_d``: ``(conv_matrix, conv_bc_left, conv_bc_right)``.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/0b0ac9e5d5a7ceb669718e3aafef1ebd9960b860/src/pymrm/convect.py#L11-L69)

## `construct_convflux_upwind_int(shape, v = 1.0, axis = 0, format = 'csc')`

[Open dedicated reference page](../symbols/pymrm.convect.construct_convflux_upwind_int.md)

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

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/0b0ac9e5d5a7ceb669718e3aafef1ebd9960b860/src/pymrm/convect.py#L72-L129)

## `minmod(normalized_c_c, normalized_x_c, normalized_x_d)`

[Open dedicated reference page](../symbols/pymrm.convect.minmod.md)

Compute the Minmod TVD correction in normalized-variable space.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/0b0ac9e5d5a7ceb669718e3aafef1ebd9960b860/src/pymrm/convect.py#L398-L407)

## `muscl(normalized_c_c, normalized_x_c, normalized_x_d)`

[Open dedicated reference page](../symbols/pymrm.convect.muscl.md)

Compute the MUSCL TVD correction in normalized-variable space.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/0b0ac9e5d5a7ceb669718e3aafef1ebd9960b860/src/pymrm/convect.py#L436-L451)

## `osher(normalized_c_c, normalized_x_c, normalized_x_d)`

[Open dedicated reference page](../symbols/pymrm.convect.osher.md)

Compute the Osher TVD correction in normalized-variable space.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/0b0ac9e5d5a7ceb669718e3aafef1ebd9960b860/src/pymrm/convect.py#L410-L420)

## `smart(normalized_c_c, normalized_x_c, normalized_x_d)`

[Open dedicated reference page](../symbols/pymrm.convect.smart.md)

Compute the SMART TVD correction in normalized-variable space.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/0b0ac9e5d5a7ceb669718e3aafef1ebd9960b860/src/pymrm/convect.py#L454-L485)

## `stoic(normalized_c_c, normalized_x_c, normalized_x_d)`

[Open dedicated reference page](../symbols/pymrm.convect.stoic.md)

Compute the STOIC TVD correction in normalized-variable space.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/0b0ac9e5d5a7ceb669718e3aafef1ebd9960b860/src/pymrm/convect.py#L488-L534)

## `upwind(normalized_c_c, normalized_x_c, normalized_x_d)`

[Open dedicated reference page](../symbols/pymrm.convect.upwind.md)

Return zero correction (first-order upwind limiter).

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/0b0ac9e5d5a7ceb669718e3aafef1ebd9960b860/src/pymrm/convect.py#L392-L395)

## `vanleer(normalized_c_c, normalized_x_c, normalized_x_d)`

[Open dedicated reference page](../symbols/pymrm.convect.vanleer.md)

Compute the van-Leer TVD correction in normalized-variable space.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/0b0ac9e5d5a7ceb669718e3aafef1ebd9960b860/src/pymrm/convect.py#L537-L546)
