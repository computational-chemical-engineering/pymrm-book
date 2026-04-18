# `pymrm.operators.construct_grad`

## Signature

`pymrm.operators.construct_grad(shape, x_f, x_c=None, bc=(None, None), axis=0, shapes_d=(None, None), format='csc')`

## Docstring

```text
Construct the full gradient operator including boundary contributions.

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
    ``'a'``, ``'b'``, and ``'d'``.
axis : int, optional
    Differentiation axis.
shapes_d : tuple[tuple | None, tuple | None], optional
    Optional output shapes for inhomogeneous boundary source vectors.
format : {'csc', 'csr'}, optional
    Sparse format used for returned operator matrices.

Returns
-------
tuple
    Without ``shapes_d``: ``(grad_matrix, grad_bc)``.
    With ``shapes_d``: ``(grad_matrix, grad_bc_left, grad_bc_right)``.
```

## Implementation

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
        ``'a'``, ``'b'``, and ``'d'``.
    axis : int, optional
        Differentiation axis.
    shapes_d : tuple[tuple | None, tuple | None], optional
        Optional output shapes for inhomogeneous boundary source vectors.
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
