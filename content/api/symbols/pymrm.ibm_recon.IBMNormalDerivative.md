# `pymrm.ibm_recon.IBMNormalDerivative`

[Back to module page](../modules/pymrm.ibm_recon) · [Back to alphabetical overview](../alphabetical_overview)

## Signature

`IBMNormalDerivative()`

## Summary

One-sided normal-derivative operators and diagnostics per IBM crossing.

## Documentation

The outward normal derivative on each side of crossing ``k`` is

    ``q_side[k] = alpha_side[k] * c_gamma_side[k] + (D_side @ c_spatial)[k]``

with ``c_spatial`` the field on the spatial grid (flattened, C-order) and
the *outward per side* sign convention described in the module docstring.

### Attributes

- `normals` (*ndarray, shape (n_crossings, ndim_s)*)
  Unit normals, pointing from solid to fluid.

- `alpha_out, alpha_in` (*ndarray, shape (n_crossings,)*)
  Weight of the one-sided interface value in ``q_side``.

- `D_out, D_in` (*csr_array, shape (n_crossings, n_spatial_cells)*)
  Weights of the same-side cell values in ``q_side``.

- `degree_out, degree_in` (*ndarray of int*)
  Polynomial degree actually used: 2 or 1 (GFD), 0 (two-point normal
  formula), -1 (degenerate axis-direction two-point fallback).

- `n_stencil_out, n_stencil_in` (*ndarray of int*)
  Number of cell points in the stencil.

- `radius_out, radius_in` (*ndarray*)
  Physical search radius of the accepted stencil.

- `cond_out, cond_in` (*ndarray*)
  Conditioning of the GFD moment matrix (1 for two-point formulas).

- `moment_residual_out, moment_residual_in` (*ndarray*)
  Max-norm residual of the polynomial moment conditions.

- `weight_norm_out, weight_norm_in` (*ndarray*)
  ``h``-scaled 1-norm of the weights, O(1) for a healthy formula.

- `unresolved_out, unresolved_in` (*ndarray of bool*)
  True where only the degenerate axis-direction fallback was possible.

### Shape information

n_crossings : int
    Number of wall crossings (matches ``ibm.n_crossings``).
spatial_shape : tuple
    Spatial grid shape.
shape : tuple
    Full field shape (spatial + non-spatial axes).
axes : tuple of int
    Which axes of ``shape`` are spatial.
ns_size : int
    Product of the non-spatial dimensions (1 when purely spatial).
n_cells : int
    Total number of cells, ``prod(shape)``.
n_spatial_cells : int
    Number of spatial cells, ``prod(spatial_shape)``.
h_ref : ndarray, shape (ndim_spatial,)
    Median cell-centre spacing along each spatial axis (reference scale
    for the GFD weights).

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_recon.py#L70-L154)

```python
class IBMNormalDerivative:
    """One-sided normal-derivative operators and diagnostics per IBM crossing.

    The outward normal derivative on each side of crossing ``k`` is

        ``q_side[k] = alpha_side[k] * c_gamma_side[k] + (D_side @ c_spatial)[k]``

    with ``c_spatial`` the field on the spatial grid (flattened, C-order) and
    the *outward per side* sign convention described in the module docstring.

    Attributes
    ----------
    normals : ndarray, shape (n_crossings, ndim_s)
        Unit normals, pointing from solid to fluid.
    alpha_out, alpha_in : ndarray, shape (n_crossings,)
        Weight of the one-sided interface value in ``q_side``.
    D_out, D_in : csr_array, shape (n_crossings, n_spatial_cells)
        Weights of the same-side cell values in ``q_side``.
    degree_out, degree_in : ndarray of int
        Polynomial degree actually used: 2 or 1 (GFD), 0 (two-point normal
        formula), -1 (degenerate axis-direction two-point fallback).
    n_stencil_out, n_stencil_in : ndarray of int
        Number of cell points in the stencil.
    radius_out, radius_in : ndarray
        Physical search radius of the accepted stencil.
    cond_out, cond_in : ndarray
        Conditioning of the GFD moment matrix (1 for two-point formulas).
    moment_residual_out, moment_residual_in : ndarray
        Max-norm residual of the polynomial moment conditions.
    weight_norm_out, weight_norm_in : ndarray
        ``h``-scaled 1-norm of the weights, O(1) for a healthy formula.
    unresolved_out, unresolved_in : ndarray of bool
        True where only the degenerate axis-direction fallback was possible.

    Shape information
    -----------------
    n_crossings : int
        Number of wall crossings (matches ``ibm.n_crossings``).
    spatial_shape : tuple
        Spatial grid shape.
    shape : tuple
        Full field shape (spatial + non-spatial axes).
    axes : tuple of int
        Which axes of ``shape`` are spatial.
    ns_size : int
        Product of the non-spatial dimensions (1 when purely spatial).
    n_cells : int
        Total number of cells, ``prod(shape)``.
    n_spatial_cells : int
        Number of spatial cells, ``prod(spatial_shape)``.
    h_ref : ndarray, shape (ndim_spatial,)
        Median cell-centre spacing along each spatial axis (reference scale
        for the GFD weights).
    """

    normals: np.ndarray

    alpha_out: np.ndarray
    alpha_in: np.ndarray
    D_out: csr_array
    D_in: csr_array

    degree_out: np.ndarray
    degree_in: np.ndarray
    n_stencil_out: np.ndarray
    n_stencil_in: np.ndarray
    radius_out: np.ndarray
    radius_in: np.ndarray
    cond_out: np.ndarray
    cond_in: np.ndarray
    moment_residual_out: np.ndarray
    moment_residual_in: np.ndarray
    weight_norm_out: np.ndarray
    weight_norm_in: np.ndarray
    unresolved_out: np.ndarray
    unresolved_in: np.ndarray

    n_crossings: int
    spatial_shape: tuple
    shape: tuple
    axes: tuple
    ns_size: int
    n_cells: int
    n_spatial_cells: int
    h_ref: np.ndarray
```

## Members

### `D_in`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_recon.py#L130-L130)

### `D_out`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_recon.py#L129-L129)

### `alpha_in`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_recon.py#L128-L128)

### `alpha_out`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_recon.py#L127-L127)

### `axes`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_recon.py#L150-L150)

### `cond_in`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_recon.py#L139-L139)

### `cond_out`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_recon.py#L138-L138)

### `degree_in`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_recon.py#L133-L133)

### `degree_out`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_recon.py#L132-L132)

### `h_ref`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_recon.py#L154-L154)

### `moment_residual_in`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_recon.py#L141-L141)

### `moment_residual_out`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_recon.py#L140-L140)

### `n_cells`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_recon.py#L152-L152)

### `n_crossings`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_recon.py#L147-L147)

### `n_spatial_cells`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_recon.py#L153-L153)

### `n_stencil_in`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_recon.py#L135-L135)

### `n_stencil_out`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_recon.py#L134-L134)

### `normals`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_recon.py#L125-L125)

### `ns_size`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_recon.py#L151-L151)

### `radius_in`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_recon.py#L137-L137)

### `radius_out`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_recon.py#L136-L136)

### `shape`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_recon.py#L149-L149)

### `spatial_shape`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_recon.py#L148-L148)

### `unresolved_in`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_recon.py#L145-L145)

### `unresolved_out`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_recon.py#L144-L144)

### `weight_norm_in`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_recon.py#L143-L143)

### `weight_norm_out`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_recon.py#L142-L142)
