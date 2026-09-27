# `pymrm.operators.construct_grad`

[Back to module page](../modules/pymrm.operators) · [Back to alphabetical overview](../alphabetical_overview)

## Signature

`construct_grad(shape, x_f, x_c = None, bc = (None, None), axis = 0, shapes_d = (None, None), format = 'csc')`

## Summary

Construct the full gradient operator including boundary contributions.

## Documentation

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

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/26b1cf19019672d855d525a0001f9d3c2a650e65/src/pymrm/operators.py#L10-L71)

```python
def construct_grad(
    shape, x_f, x_c=None, bc=(None, None), axis=0, shapes_d=(None, None), format="csc"
):
    """Construct the full gradient operator including boundary contributions.

    Parameters
    ----------
    shape : tuple[int, ...] or int
        Cell-centered field shape.
    x_f : array_like
        Face coordinates along ``axis``.
    x_c : array_like, optional
        Cell-center coordinates along ``axis``. If omitted, they are generated
        as arithmetic midpoints.
    bc : tuple[dict | None, dict | None], optional
        Left and right boundary-condition dictionaries with coefficients
        ``'a'``, ``'b'``, and ``'d'`` for ``a * dc/dn + b * c = d`` with ``n``
        the outward normal. ``{"outflow": True}`` marks a pure-outflow
        boundary; for diffusion it means zero normal gradient.
    axis : int, optional
        Differentiation axis.
    shapes_d : tuple[tuple | None, tuple | None], optional
        Optional output shapes for inhomogeneous boundary source vectors. With
        ``shapes_d`` the dictionary's ``d`` is a coefficient on that external
        vector (use ``d = 1`` to pass values through the vector).
    format : {'csc', 'csr'}, optional
        Sparse format used for returned operator matrices.

    Returns
    -------
    tuple
        Without ``shapes_d``: ``(grad_matrix, grad_bc)``.
        With ``shapes_d``: ``(grad_matrix, grad_bc_left, grad_bc_right)``.
    """
    if isinstance(shape, int):
        shape = (shape,)
    else:
        shape = tuple(shape)
    x_f, x_c = generate_grid(shape[axis], x_f, generate_x_c=True, x_c=x_c)
    grad_matrix = construct_grad_int(shape, x_f, x_c, axis, format=format)
    # a pure-outflow boundary carries no diffusive flux: zero normal gradient
    bc, _ = substitute_outflow_bc(bc, {"a": 1.0, "b": 0.0, "d": 0.0})

    if bc == (None, None):
        shape_f = shape[:axis] + (shape[axis] + 1,) + shape[axis + 1:]
        grad_bc = csc_array((math.prod(shape_f), 1))
        return grad_matrix, grad_bc
    else:
        if shapes_d is None or shapes_d == (None, None):
            grad_matrix_bc, grad_bc = construct_grad_bc(
                shape, x_f, x_c, bc, axis, format=format
            )
            grad_matrix += grad_matrix_bc
            return grad_matrix, grad_bc
        else:
            grad_matrix_bc_0, grad_bc_0, grad_matrix_bc_1, grad_bc_1 = (
                construct_grad_bc(
                    shape, x_f, x_c, bc, axis, shapes_d=shapes_d, format=format
                )
            )
            grad_matrix += grad_matrix_bc_0 + grad_matrix_bc_1
            return grad_matrix, grad_bc_0, grad_bc_1
```
