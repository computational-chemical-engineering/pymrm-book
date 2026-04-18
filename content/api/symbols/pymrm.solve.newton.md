# `pymrm.solve.newton`

## Signature

`pymrm.solve.newton(function, initial_guess, args=(), tol=1.49012e-08, maxfev=100, solver=None, lin_solver_kwargs=None, callback=None)`

## Docstring

```text
Solve ``function(x) = 0`` with Newton iterations.

Parameters
----------
function : callable
    Callable with signature ``function(x, *args) -> (residual, jacobian)``.
initial_guess : numpy.ndarray
    Starting point of the iterations.
args : tuple, optional
    Extra positional arguments passed to ``function``.
tol : float, optional
    Stopping tolerance on the infinity norm of the Newton update.
maxfev : int, optional
    Maximum number of Newton iterations.
solver : {'spsolve', 'cg', 'bicgstab'} or callable, optional
    Linear solver used for each Newton step. If ``None``, the routine picks
    ``'spsolve'`` for smaller systems and ``'bicgstab'`` for larger systems.
    A callable solver must accept ``(jac_matrix, rhs, **kwargs)`` and return
    the solution vector.
lin_solver_kwargs : dict, optional
    Keyword arguments forwarded to the selected linear solver.
callback : callable, optional
    Optional hook called as ``callback(x, residual)`` after each iteration.

Returns
-------
scipy.optimize.OptimizeResult
    Result object with fields ``x``, ``success``, ``nit``, ``fun``, and
    ``message``.

Raises
------
ValueError
    If ``solver`` is not one of the supported names and is not callable.
RuntimeError
    If an iterative linear solver fails to converge.
```

## Implementation

```python
def newton(
    function,
    initial_guess,
    args=(),
    tol=1.49012e-08,
    maxfev=100,
    solver=None,
    lin_solver_kwargs=None,
    callback=None,
):
    """Solve ``function(x) = 0`` with Newton iterations.

    Parameters
    ----------
    function : callable
        Callable with signature ``function(x, *args) -> (residual, jacobian)``.
    initial_guess : numpy.ndarray
        Starting point of the iterations.
    args : tuple, optional
        Extra positional arguments passed to ``function``.
    tol : float, optional
        Stopping tolerance on the infinity norm of the Newton update.
    maxfev : int, optional
        Maximum number of Newton iterations.
    solver : {'spsolve', 'cg', 'bicgstab'} or callable, optional
        Linear solver used for each Newton step. If ``None``, the routine picks
        ``'spsolve'`` for smaller systems and ``'bicgstab'`` for larger systems.
        A callable solver must accept ``(jac_matrix, rhs, **kwargs)`` and return
        the solution vector.
    lin_solver_kwargs : dict, optional
        Keyword arguments forwarded to the selected linear solver.
    callback : callable, optional
        Optional hook called as ``callback(x, residual)`` after each iteration.

    Returns
    -------
    scipy.optimize.OptimizeResult
        Result object with fields ``x``, ``success``, ``nit``, ``fun``, and
        ``message``.

    Raises
    ------
    ValueError
        If ``solver`` is not one of the supported names and is not callable.
    RuntimeError
        If an iterative linear solver fails to converge.
    """
    n = initial_guess.size
    if solver is None:
        solver = "spsolve" if n < 50000 else "bicgstab"

    if lin_solver_kwargs is None:
        lin_solver_kwargs = {}

    # Select linear solver
    if solver == "spsolve":

        def linsolver(jac_matrix, g, **kwargs):
            return linalg.spsolve(jac_matrix, g, **kwargs)

    elif solver == "cg":

        def linsolver(jac_matrix, g, **kwargs):
            Jac_iLU = linalg.spilu(jac_matrix)
            M = linalg.LinearOperator((n, n), Jac_iLU.solve)
            dx_neg, info = linalg.cg(jac_matrix, g, M=M, **kwargs)
            if info != 0:
                raise RuntimeError(f"CG did not converge, info={info}")
            return dx_neg

    elif solver == "bicgstab":

        def linsolver(jac_matrix, g, **kwargs):
            Jac_iLU = linalg.spilu(jac_matrix)
            M = linalg.LinearOperator((n, n), Jac_iLU.solve)
            dx_neg, info = linalg.bicgstab(jac_matrix, g, M=M, **kwargs)
            if info != 0:
                raise RuntimeError(f"BICGSTAB did not converge, info={info}")
            return dx_neg

    elif callable(solver):

        def linsolver(jac_matrix, g, **kwargs):
            return solver(jac_matrix, g, **kwargs)

    else:
        raise ValueError("Unsupported solver method.")

    x = initial_guess.copy()
    for it in range(int(maxfev)):
        g, jac_matrix = function(x, *args)
        dx_neg = linsolver(jac_matrix, g, **lin_solver_kwargs)
        defect = norm(dx_neg, ord=np.inf)
        x -= dx_neg.reshape(x.shape)
        if callback:
            callback(x, g)
        if defect < tol:
            return OptimizeResult(
                x=x, success=True, nit=it + 1, fun=g, message="Converged"
            )

    return OptimizeResult(
        x=x, success=False, nit=maxfev, fun=g, message="Did not converge"
    )

```
