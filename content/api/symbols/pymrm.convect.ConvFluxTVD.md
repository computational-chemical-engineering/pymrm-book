# `pymrm.convect.ConvFluxTVD`

[Back to module page](../modules/pymrm.convect) · [Back to alphabetical overview](../alphabetical_overview)

## Signature

`ConvFluxTVD(shape, x_f, x_c = None, bc = (None, None), tvd_limiter = minmod, axis = 0, shapes_d = (None, None), format = 'csc')`

## Summary

TVD convective face flux with its exact Jacobians, for Newton solves.

## Documentation

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

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/edd7b4da542580c2776cbb05bd6761bce4495f28/src/pymrm/convect.py#L674-L966)

```python
class ConvFluxTVD:
    """TVD convective face flux with its exact Jacobians, for Newton solves.

    Build the object once per axis, then call it with the current state in
    every residual evaluation. It returns the face fluxes ``v * c_f``, with
    ``c_f`` the TVD face values of :func:`interp_cntr_to_stagg_tvd`, and the
    derivative of those fluxes with respect to the state: the upwind part, the
    limiter part and the boundary faces together. A steady problem solved with
    this Jacobian converges in a few Newton steps for every limiter; deferred
    correction (the TVD correction in the residual, the upwind Jacobian)
    converges only slowly with minmod and stalls with van Leer, MUSCL and
    SMART (pitfalls P10).

    Parameters
    ----------
    shape : tuple[int, ...] or int
        Cell-centered field shape.
    x_f : array_like
        Face coordinates along ``axis``.
    x_c : array_like, optional
        Cell-center coordinates. If omitted, arithmetic midpoints are used.
    bc : tuple[dict | None, dict | None], optional
        Left and right boundary conditions ``a * dc/dn + b * c = d`` with
        ``n`` the outward normal, or ``{"outflow": True}``, as for
        :func:`construct_convflux_upwind`. Boundary faces carry the boundary
        value without a TVD correction.
    tvd_limiter : callable, optional
        Limiter ``phi(c_norm, x_norm_c, x_norm_d)`` (default :func:`minmod`).
        The built-in limiters carry an analytic ``derivative`` attribute; for
        any other limiter the derivative is a central difference in
        ``c_norm``.
    axis : int, optional
        Convection axis.
    shapes_d : tuple[tuple | None, tuple | None], optional
        Shapes of external vectors for the boundary data, as for
        :func:`construct_convflux_upwind`: ``d`` is then a coefficient on that
        vector, and the call takes the vectors and also returns the Jacobians
        with respect to them.
    format : {'csc', 'csr'}, optional
        Sparse format of the returned Jacobians.

    Notes
    -----
    Call ``flux, jac = tvd(c, v)``; with ``shapes_d``,
    ``flux, jac, jac_bc_left, jac_bc_right = tvd(c, v, d=(ext_left, ext_right))``;
    ``jac_v=True`` appends the Jacobian with respect to ``v``. See
    :meth:`__call__`.

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
    """

    def __init__(
        self, shape, x_f, x_c=None, bc=(None, None), tvd_limiter=minmod, axis=0,
        shapes_d=(None, None), format="csc"
    ):
        shape = (shape,) if isinstance(shape, int) else tuple(shape)
        if axis < 0:
            axis += len(shape)
        x_f, x_c = generate_grid(shape[axis], x_f, generate_x_c=True, x_c=x_c)
        if bc is None:
            bc = (None, None)
        self.shape = shape
        self.axis = axis
        self.shape_f = shape[:axis] + (shape[axis] + 1,) + shape[axis + 1:]
        self._x_f, self._x_c = x_f, x_c
        self.tvd_limiter = upwind if tvd_limiter is None else tvd_limiter
        self.format = format
        n0, n1, n2 = math.prod(shape[:axis]), shape[axis], math.prod(shape[axis + 1:])
        self._shape_t = (n0, n1, n2)
        self._shape_f_t = (n0, n1 + 1, n2)

        if shapes_d is None:
            shapes_d = (None, None)
        self.shapes_d = tuple(shapes_d)
        self._with_d = any(s is not None for s in self.shapes_d)
        ones = (1,) * len(shape)
        shapes_ext = tuple(ones if s is None else tuple(s) for s in self.shapes_d)
        self._n_ext = tuple(math.prod(s) for s in shapes_ext)

        # Boundary faces: value maps with the outflow face set to its cell. As
        # the upwind point of the neighbouring face, an outflow boundary takes
        # the zero-gradient value, as in interp_cntr_to_stagg_tvd.
        bc_upwind, _ = substitute_outflow_bc(bc, {"a": 1.0, "b": 0.0, "d": 0.0})
        m_0, e_0, m_1, e_1 = construct_convflux_bc(
            shape, x_f, x_c, bc, 1.0, axis, shapes_d=shapes_ext, format="csr")
        self._m_face, self._e_face = (m_0 + m_1).tocsr(), (e_0.tocsr(), e_1.tocsr())
        m_0, e_0, m_1, e_1 = construct_convflux_bc(
            shape, x_f, x_c, bc_upwind, 1.0, axis, shapes_d=shapes_ext, format="csr")
        self._m_up, self._e_up = (m_0 + m_1).tocsr(), (e_0.tocsr(), e_1.tocsr())

        def coefficient(matrix, cell):
            """Coefficient of cell ``cell`` (along the axis) in each face row."""
            indicator = np.zeros(self._shape_t)
            indicator[:, cell, :] = 1.0
            return (matrix @ indicator.ravel()).reshape(self._shape_f_t)

        # band[:, face, o + 2, :]: dependence of a boundary face on cell face + o
        self._offsets = np.arange(-2, 2)
        self._band_bnd = np.zeros((n0, 2, 4, n2))
        for side, face in enumerate((0, n1)):
            for o in self._offsets:
                if 0 <= face + o < n1:
                    self._band_bnd[:, side, o + 2, :] = coefficient(self._m_face, face + o)[:, face, :]
        if n1 > 1:
            self._up_left = [coefficient(self._m_up, j)[:, 0, :] for j in (0, 1)]
            self._up_right = [coefficient(self._m_up, j)[:, n1, :] for j in (n1 - 1, n1 - 2)]

            # normalized positions of the interior faces 1 .. n1-1, per direction
            x_d = x_f[1:-1]
            x_U = np.concatenate((x_f[:1], x_c[:-2]))
            x_norm = {}
            for positive, x_up, x_C, x_D in (
                (True, x_U, x_c[:-1], x_c[1:]),
                (False, np.concatenate((x_c[2:], x_f[-1:])), x_c[1:], x_c[:-1]),
            ):
                x_norm[positive] = (
                    ((x_C - x_up) / (x_D - x_up)).reshape(1, -1, 1),
                    ((x_d - x_up) / (x_D - x_up)).reshape(1, -1, 1),
                )
            self._x_norm = x_norm

        # fixed sparsity pattern: face k, cell k + o, for o = -2 .. 1
        k = np.arange(n1 + 1).reshape(1, -1, 1, 1)
        cells = k + self._offsets.reshape(1, 1, -1, 1)
        valid = (cells >= 0) & (cells < n1)
        self._valid = np.broadcast_to(valid, (n0, n1 + 1, 4, n2))
        i0 = np.arange(n0).reshape(-1, 1, 1, 1)
        i2 = np.arange(n2).reshape(1, 1, 1, -1)
        rows = ((i0 * (n1 + 1) + k) * n2 + i2) + 0 * cells
        cols = ((i0 * n1 + np.clip(cells, 0, n1 - 1)) * n2 + i2)
        rows, cols = rows[self._valid], cols[self._valid]
        shape_jac = (math.prod(self._shape_f_t), math.prod(self._shape_t))
        tag = _sparse_array((np.arange(1, rows.size + 1, dtype=float), (rows, cols)),
                            shape=shape_jac, format=format)
        tag.sort_indices()
        self._perm = tag.data.astype(np.intp) - 1
        self._indices, self._indptr, self._shape_jac = tag.indices, tag.indptr, shape_jac

        # boundary faces and the interior faces next to them, as flat face indices
        f_t = np.arange(math.prod(self._shape_f_t)).reshape(self._shape_f_t)
        self._faces_left, self._faces_right = f_t[:, 0, :], f_t[:, n1, :]
        if n1 > 1:
            self._faces_second, self._faces_penult = f_t[:, 1, :], f_t[:, n1 - 1, :]

    def __call__(self, c, v, d=None, jac_v=False):
        """Evaluate the face fluxes and their Jacobians.

        Parameters
        ----------
        c : array_like
            Cell-centered values, any array with ``prod(shape)`` elements.
        v : float or array_like
            Face velocity (or any face weight, such as ``rho * cp * v``),
            accepted as by :func:`construct_convflux_upwind` (through
            :func:`create_staggered_array`): a scalar, a face-shaped or
            broadcastable array, or a 1-D array along the convection axis.
            Cell-centred values are interpolated to the faces, but not with
            ``jac_v=True``. Its sign selects the stencil of each interior face.
        d : tuple, optional
            With ``shapes_d``: the external vectors ``(ext_left, ext_right)``
            (``None`` for a side without a shape). Required then, ignored
            otherwise.
        jac_v : bool, optional
            Also return the Jacobian with respect to ``v``.

        Returns
        -------
        tuple
            ``(flux, jac)``; with ``shapes_d``
            ``(flux, jac, jac_bc_left, jac_bc_right)``; with ``jac_v=True``
            the Jacobian with respect to ``v`` is appended. ``flux`` has the
            face shape; apply :func:`construct_div` to ``flux.reshape(-1)``.
            ``jac`` is ``(n_faces, n_cells)``: use ``div @ jac``.
            ``jac_bc_*`` are ``(n_faces, prod(shapes_d[i]))`` derivatives only:
            ``flux`` already contains the boundary data. The Jacobian with
            respect to ``v`` is ``(n_faces, v.size)`` with its columns in the
            order of ``v``; its entries are the face values ``c_f``. For a
            velocity from a pressure gradient, chain it with that gradient
            matrix.
        """
        n0, n1, n2 = self._shape_t
        c = np.asarray(c, dtype=float).reshape(self._shape_t)
        v_in = np.asarray(v, dtype=float)
        try:
            v_aligned = _align_to_axes(v_in, self.shape, self.axis)
            v_t = create_staggered_array(v_in, self.shape, self.axis, x_f=self._x_f, x_c=self._x_c)
        except ValueError:
            raise ValueError(
                f"v with shape {v_in.shape} does not fit the face shape {self.shape_f}"
            ) from None
        centred = (v_in.size > 1 and self.shape[self.axis] > 1 and v_aligned.ndim == len(self.shape)
                   and v_aligned.shape[self.axis] == self.shape[self.axis])
        if jac_v and centred:
            raise ValueError("jac_v=True needs v on the faces, not at the cell centres")
        v_t = v_t.reshape(self._shape_f_t)
        ext = [np.ones(1), np.ones(1)]
        if self._with_d:
            if d is None:
                raise ValueError("built with shapes_d: pass d=(ext_left, ext_right)")
            for i in range(2):
                if self.shapes_d[i] is not None:
                    ext[i] = np.asarray(d[i], dtype=float).reshape(-1)
                    if ext[i].size != self._n_ext[i]:
                        raise ValueError(f"d[{i}] has {ext[i].size} values, shapes_d[{i}] needs {self._n_ext[i]}")

        c_flat = c.ravel()
        face_bnd = (self._m_face @ c_flat + self._e_face[0] @ ext[0]
                    + self._e_face[1] @ ext[1]).reshape(self._shape_f_t)
        face = np.zeros(self._shape_f_t)
        face[:, 0, :], face[:, n1, :] = face_bnd[:, 0, :], face_bnd[:, n1, :]
        band = np.zeros((n0, n1 + 1, 4, n2))       # d c_f / d c, before the velocity
        band[:, 0], band[:, n1] = self._band_bnd[:, 0], self._band_bnd[:, 1]
        g_left = g_right = None

        if n1 > 1:
            up = (self._m_up @ c_flat + self._e_up[0] @ ext[0]
                  + self._e_up[1] @ ext[1]).reshape(self._shape_f_t)
            pos = v_t[:, 1:-1, :] > 0
            c_U = np.where(pos, np.concatenate((up[:, :1], c[:, :-2]), axis=1),
                           np.concatenate((c[:, 2:], up[:, n1:]), axis=1))
            c_C = np.where(pos, c[:, :-1], c[:, 1:])
            c_D = np.where(pos, c[:, 1:], c[:, :-1])
            x_norm_c = np.where(pos, self._x_norm[True][0], self._x_norm[False][0])
            x_norm_d = np.where(pos, self._x_norm[True][1], self._x_norm[False][1])
            dc_DU = c_D - c_U
            c_norm = np.zeros_like(c_C)
            np.divide(c_C - c_U, dc_DU, out=c_norm, where=(dc_DU != 0))
            phi = self.tvd_limiter(c_norm, x_norm_c, x_norm_d)
            face[:, 1:-1, :] = c_C + phi * dc_DU
            active = dc_DU != 0
            dphi = np.zeros_like(c_norm)
            if np.any(active):
                dphi[active] = _limiter_derivative(
                    self.tvd_limiter, c_norm[active], x_norm_c[active], x_norm_d[active])
            w_C = 1 + dphi
            w_D = phi - c_norm * dphi
            w_U = -phi + (c_norm - 1) * dphi

            inner = band[:, 1:-1]                    # faces 1 .. n1-1, offsets -2 .. 1
            neg = ~pos
            # v > 0: U = k-2, C = k-1, D = k; v <= 0: U = k+1, C = k, D = k-1
            inner[:, :, 1] += np.where(pos, w_C, w_D)
            inner[:, :, 2] += np.where(pos, w_D, w_C)
            inner[:, 1:, 0] += np.where(pos[:, 1:], w_U[:, 1:], 0.0)
            inner[:, :-1, 3] += np.where(neg[:, :-1], w_U[:, :-1], 0.0)
            # the upwind point of face 1 (v > 0) and face n1-1 (v <= 0) is a boundary value
            g_left = np.where(pos[:, 0], w_U[:, 0], 0.0)
            inner[:, 0, 1] += g_left * self._up_left[0]
            inner[:, 0, 2] += g_left * self._up_left[1]
            g_right = np.where(neg[:, -1], w_U[:, -1], 0.0)
            inner[:, -1, 2] += g_right * self._up_right[0]
            inner[:, -1, 1] += g_right * self._up_right[1]

        flux = (v_t * face).reshape(self.shape_f)
        data = (band * v_t[:, :, None, :])[self._valid][self._perm]
        jac = _sparse_array((data, self._indices.copy(), self._indptr.copy()),
                            shape=self._shape_jac, format=self.format)
        out = [flux, jac]

        if self._with_d:
            n_f = math.prod(self._shape_f_t)
            v_flat = v_t.ravel()
            on_bnd = np.zeros(n_f)
            on_bnd[self._faces_left.ravel()] = 1.0
            on_bnd[self._faces_right.ravel()] = 1.0
            scale_bnd = csr_array((v_flat * on_bnd, (np.arange(n_f), np.arange(n_f))), shape=(n_f, n_f))
            for i, g, rows, cols in (
                (0, g_left, "_faces_second", "_faces_left"),
                (1, g_right, "_faces_penult", "_faces_right"),
            ):
                jac_bc = scale_bnd @ self._e_face[i]
                if g is not None:
                    r, k = getattr(self, rows).ravel(), getattr(self, cols).ravel()
                    chain = csr_array(((v_flat[r] * g.ravel()), (r, k)), shape=(n_f, n_f))
                    jac_bc = jac_bc + chain @ self._e_up[i]
                out.append(jac_bc.asformat(self.format))

        if jac_v:
            n_f = math.prod(self._shape_f_t)
            v_cols = create_staggered_array(np.arange(v_in.size).reshape(v_in.shape), self.shape,
                                            self.axis, x_f=self._x_f, x_c=self._x_c).ravel()
            out.append(_sparse_array((face.ravel(), (np.arange(n_f), v_cols)),
                                     shape=(n_f, v_in.size), format=self.format))
        return tuple(out)
```

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
