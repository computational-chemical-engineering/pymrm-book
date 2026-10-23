# `pymrm.convect`

[Back to modules overview](../api)

Convective-flux operators and TVD limiter functions.

[View module source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/edd7b4da542580c2776cbb05bd6761bce4495f28/src/pymrm/convect.py)

## Public API

| Symbol | Type | Summary |
| ------ | ---- | ------- |
| [`ConvFluxTVD`](../symbols/pymrm.convect.ConvFluxTVD) | class | TVD convective face flux with its exact Jacobians, for Newton solves. |
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

## `ConvFluxTVD(shape, x_f, x_c = None, bc = (None, None), tvd_limiter = minmod, axis = 0, shapes_d = (None, None), format = 'csc')`

[Open dedicated reference page](../symbols/pymrm.convect.ConvFluxTVD)

TVD convective face flux with its exact Jacobians, for Newton solves.

Build the object once per axis, then call it with the current state in
every residual evaluation. It returns the face fluxes ``v * c_f``, with
``c_f`` the TVD face values of `interp_cntr_to_stagg_tvd`, and the
derivative of those fluxes with respect to the state: the upwind part, the
limiter part and the boundary faces together. A steady problem solved with
this Jacobian converges in a few Newton steps for every limiter; deferred
correction (the TVD correction in the residual, the upwind Jacobian)
converges only slowly with minmod and stalls with van Leer, MUSCL and
SMART (pitfalls P10).

### Parameters

- `shape` (*tuple[int, ...] or int*)
  Cell-centered field shape.

- `x_f` (*array_like*)
  Face coordinates along ``axis``.

- `x_c` (*array_like, optional*)
  Cell-center coordinates. If omitted, arithmetic midpoints are used.

- `bc` (*tuple[dict | None, dict | None], optional*)
  Left and right boundary conditions ``a * dc/dn + b * c = d`` with
  ``n`` the outward normal, or ``{"outflow": True}``, as for
  `construct_convflux_upwind`. Boundary faces carry the boundary
  value without a TVD correction.

- `tvd_limiter` (*callable, optional*)
  Limiter ``phi(c_norm, x_norm_c, x_norm_d)`` (default `minmod`).
  The built-in limiters carry an analytic ``derivative`` attribute; for
  any other limiter the derivative is a central difference in
  ``c_norm``.

- `axis` (*int, optional*)
  Convection axis.

- `shapes_d` (*tuple[tuple | None, tuple | None], optional*)
  Shapes of external vectors for the boundary data, as for
  `construct_convflux_upwind`: ``d`` is then a coefficient on that
  vector, and the call takes the vectors and also returns the Jacobians
  with respect to them.

- `format` (*{'csc', 'csr'}, optional*)
  Sparse format of the returned Jacobians.

### Notes

Call ``flux, jac = tvd(c, v)``; with ``shapes_d``,
``flux, jac, jac_bc_left, jac_bc_right = tvd(c, v, d=(ext_left, ext_right))``;
``jac_v=True`` appends the Jacobian with respect to ``v``. See
`__call__`.

The face upwind of the first interior face is the boundary value, so the
Jacobian there reaches the cells that boundary value depends on, and the
boundary data. The flow direction of each interior face follows
``v > 0``; an initial guess with ``v = 0`` everywhere gives a zero
convective Jacobian. Where ``c_D == c_U`` the face is upwind and its
derivative is the upwind one (the built-in limiters are also zero outside
``0 < c_norm < 1``). Use ``newton(..., damping="monotone")``: undamped Newton can cycle
between the pieces of MUSCL, SMART and STOIC. The
sparsity pattern covers both flow directions, so it does not change when
``v`` changes sign; it contains explicit zeros, which sparse products drop.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/edd7b4da542580c2776cbb05bd6761bce4495f28/src/pymrm/convect.py#L674-L966)

## Members

### `__init__(shape, x_f, x_c = None, bc = (None, None), tvd_limiter = minmod, axis = 0, shapes_d = (None, None), format = 'csc')`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/edd7b4da542580c2776cbb05bd6761bce4495f28/src/pymrm/convect.py#L734-L825)

### `__call__(c, v, d = None, jac_v = False)`

Evaluate the face fluxes and their Jacobians.

#### Parameters

- `c` (*array_like*)
  Cell-centered values, any array with ``prod(shape)`` elements.

- `v` (*float or array_like*)
  Face velocity (or any face weight, such as ``rho * cp * v``),
  accepted as by `construct_convflux_upwind` (through
  `create_staggered_array`): a scalar, a face-shaped or
  broadcastable array, or a 1-D array along the convection axis.
  Cell-centred values are interpolated to the faces, but not with
  ``jac_v=True``. Its sign selects the stencil of each interior face.

- `d` (*tuple, optional*)
  With ``shapes_d``: the external vectors ``(ext_left, ext_right)``
  (``None`` for a side without a shape). Required then, ignored
  otherwise.

- `jac_v` (*bool, optional*)
  Also return the Jacobian with respect to ``v``.

#### Returns

- `tuple`
  ``(flux, jac)``; with ``shapes_d``
  ``(flux, jac, jac_bc_left, jac_bc_right)``; with ``jac_v=True``
  the Jacobian with respect to ``v`` is appended. ``flux`` has the
  face shape; apply `construct_div` to ``flux.reshape(-1)``.
  ``jac`` is ``(n_faces, n_cells)``: use ``div @ jac``.
  ``jac_bc_*`` are ``(n_faces, prod(shapes_d[i]))`` derivatives only:
  ``flux`` already contains the boundary data. The Jacobian with
  respect to ``v`` is ``(n_faces, v.size)`` with its columns in the
  order of ``v``; its entries are the face values ``c_f``. For a
  velocity from a pressure gradient, chain it with that gradient
  matrix.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/edd7b4da542580c2776cbb05bd6761bce4495f28/src/pymrm/convect.py#L827-L966)

## `clam(normalized_c_c, normalized_x_c, normalized_x_d)`

[Open dedicated reference page](../symbols/pymrm.convect.clam)

Compute the CLAM TVD correction in normalized-variable space.

CLAM, van Leer's curved-line advection method, is the parabola through
(0, 0), (x_c, x_d) and (1, 1); on a uniform grid ``c_f = 2 c_c - c_c**2``.
On a uniform grid this curve is also van Leer's harmonic limiter, and
pymrm uses the same parabola, with the same cap at ``c_f = 1``, for both:
``clam`` and ``vanleer`` agree on every stencil. Before pymrm 2.5.0
``clam`` returned the Osher curve.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/edd7b4da542580c2776cbb05bd6761bce4495f28/src/pymrm/convect.py#L455-L465)

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

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/edd7b4da542580c2776cbb05bd6761bce4495f28/src/pymrm/convect.py#L138-L418)

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

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/edd7b4da542580c2776cbb05bd6761bce4495f28/src/pymrm/convect.py#L11-L75)

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

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/edd7b4da542580c2776cbb05bd6761bce4495f28/src/pymrm/convect.py#L78-L135)

## `minmod(normalized_c_c, normalized_x_c, normalized_x_d)`

[Open dedicated reference page](../symbols/pymrm.convect.minmod)

Compute the Minmod TVD correction in normalized-variable space.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/edd7b4da542580c2776cbb05bd6761bce4495f28/src/pymrm/convect.py#L430-L439)

## `muscl(normalized_c_c, normalized_x_c, normalized_x_d)`

[Open dedicated reference page](../symbols/pymrm.convect.muscl)

Compute the MUSCL TVD correction in normalized-variable space.

Uniform grid: 2 c_c up to 1/4, c_c + 1/4 up to 3/4, then 1.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/edd7b4da542580c2776cbb05bd6761bce4495f28/src/pymrm/convect.py#L468-L487)

## `osher(normalized_c_c, normalized_x_c, normalized_x_d)`

[Open dedicated reference page](../symbols/pymrm.convect.osher)

Compute the Osher TVD correction in normalized-variable space.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/edd7b4da542580c2776cbb05bd6761bce4495f28/src/pymrm/convect.py#L442-L452)

## `smart(normalized_c_c, normalized_x_c, normalized_x_d)`

[Open dedicated reference page](../symbols/pymrm.convect.smart)

Compute the SMART TVD correction in normalized-variable space.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/edd7b4da542580c2776cbb05bd6761bce4495f28/src/pymrm/convect.py#L490-L521)

## `stoic(normalized_c_c, normalized_x_c, normalized_x_d)`

[Open dedicated reference page](../symbols/pymrm.convect.stoic)

Compute the STOIC TVD correction in normalized-variable space.

Piecewise: the SMART line ``c_f = k c_c`` up to its intersection with the
central-difference line, then central differencing up to ``c_c = x_c``,
then QUICK, then ``c_f = 1``. On a uniform grid (``x_c = 1/2``,
``x_d = 3/4``) this is 3 c_c, (1 + c_c)/2, 3/8 + 3 c_c/4 and 1, with breaks
at 1/5, 1/2 and 5/6.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/edd7b4da542580c2776cbb05bd6761bce4495f28/src/pymrm/convect.py#L524-L553)

## `upwind(normalized_c_c, normalized_x_c, normalized_x_d)`

[Open dedicated reference page](../symbols/pymrm.convect.upwind)

Return zero correction (first-order upwind limiter).

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/edd7b4da542580c2776cbb05bd6761bce4495f28/src/pymrm/convect.py#L424-L427)

## `vanleer(normalized_c_c, normalized_x_c, normalized_x_d)`

[Open dedicated reference page](../symbols/pymrm.convect.vanleer)

Compute the van-Leer TVD correction in normalized-variable space.

The curve is the parabola through (0, 0), (x_c, x_d) and (1, 1), which on
a uniform grid is van Leer's harmonic limiter and also his CLAM curve
(``c_f = 2 c_c - c_c**2``); ``clam`` returns the same values. It rises
above ``c_f = 1`` when ``x_d - x_c > x_c (1 - x_c)``, for example next to a
boundary where the upstream point is a face half a cell away (x_c = 1/3,
x_d = 2/3); the correction is capped at ``1 - c_c`` to stay bounded. The
cap acts only above c_c = x_c and does not reduce the order.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/edd7b4da542580c2776cbb05bd6761bce4495f28/src/pymrm/convect.py#L556-L577)
