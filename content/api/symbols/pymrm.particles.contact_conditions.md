# `pymrm.particles.contact_conditions`

[Back to module page](../modules/pymrm.particles) · [Back to alphabetical overview](../alphabetical_overview)

## Signature

`contact_conditions(base_ic, ibm, info, *, contact_ic = None)`

## Summary

Per-crossing ic: *base_ic* everywhere, a contact condition on contacts.

## Documentation

### Parameters

- `base_ic` (*tuple of two dicts*)
  Interface condition for the regular (fluid–solid) crossings, in the
  format of `pymrm.apply_ibm_interface`.  Coefficients may be
  scalars or ns-broadcastable arrays (no per-crossing arrays).

- `ibm` (*IBM*)

- `info` (*ParticleIBMInfo*)

- `contact_ic` (*tuple of two dicts, optional*)
  Condition imposed on the contact crossings.  Default: independent
  homogeneous Neumann on both sides (``q_out = 0`` and ``q_in = 0``) —
  no transport between the particles.

### Returns

- `tuple of two dicts with per-crossing coefficient arrays.`

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L807-L856)

```python
def contact_conditions(base_ic, ibm, info, *, contact_ic=None):
    """Per-crossing ic: *base_ic* everywhere, a contact condition on contacts.

    Parameters
    ----------
    base_ic : tuple of two dicts
        Interface condition for the regular (fluid–solid) crossings, in the
        format of :func:`pymrm.apply_ibm_interface`.  Coefficients may be
        scalars or ns-broadcastable arrays (no per-crossing arrays).
    ibm : IBM
    info : ParticleIBMInfo
    contact_ic : tuple of two dicts, optional
        Condition imposed on the contact crossings.  Default: independent
        homogeneous Neumann on both sides (``q_out = 0`` and ``q_in = 0``) —
        no transport between the particles.

    Returns
    -------
    tuple of two dicts with per-crossing coefficient arrays.
    """
    if contact_ic is None:
        contact_ic = ({"a": (1.0, 0.0), "b": (0.0, 0.0), "d": 0.0},
                      {"a": (0.0, 1.0), "b": (0.0, 0.0), "d": 0.0})
    if not np.any(info.contact):
        return base_ic

    npnt = ibm.n_crossings
    m = info.contact.astype(float)              # (npnt,): 1 on contacts

    def blend_values(vb, vc):
        """Per-crossing mix of two scalar/ns-broadcastable coefficients."""
        vb = np.asarray(vb, dtype=float)
        vc = np.asarray(vc, dtype=float)
        trailing = np.broadcast_shapes(vb.shape, vc.shape)
        m_e = m.reshape((npnt,) + (1,) * len(trailing))
        return (np.broadcast_to(vb, trailing) * (1.0 - m_e)
                + np.broadcast_to(vc, trailing) * m_e)

    def blend(eq_base, eq_contact):
        out = {}
        for key in ("a", "b"):
            base_pair = (eq_base or {}).get(key, (0.0, 0.0))
            cont_pair = (eq_contact or {}).get(key, (0.0, 0.0))
            out[key] = tuple(blend_values(base_pair[s], cont_pair[s])
                             for s in range(2))
        out["d"] = blend_values((eq_base or {}).get("d", 0.0),
                                (eq_contact or {}).get("d", 0.0))
        return out

    return (blend(base_ic[0], contact_ic[0]), blend(base_ic[1], contact_ic[1]))
```
