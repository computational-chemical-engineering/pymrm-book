# Coding Agents

:::{note} Status: September 2026, pymrm 2.4.0
Coding agents change quickly. This page describes what they can do with pymrm
and how to check their work; those parts should age slowly. The exact install
commands live in the pymrm README, section
[Developing pymrm models with a coding agent](https://github.com/computational-chemical-engineering/pymrm#developing-pymrm-models-with-a-coding-agent),
which is kept up to date.
:::

A coding agent (Claude Code, Codex CLI, Gemini CLI and similar tools) is a
language model that reads files, writes code and runs it in your own Python
environment. Given a description of a process, it can set up a pymrm model,
run it, and report the result.

## How an agent learns pymrm

An agent that works in an environment with pymrm installed reads the package
itself: `help(pymrm)`, the docstrings and the source. Since version 2.4.0 the
docstrings state the conventions that are easiest to get wrong: the outward
normal in boundary-condition dictionaries, the trailing field axis for
`NumJac`, the absolute step tolerance of `newton` and where to read outlet
values. `help(pymrm)` summarises them together with a minimal model.

In our tests, current strong models built correct models for well-posed
problems with or without further guidance. The errors that did occur were
rarely numerical: the typical one was a condition stated in the problem that
the code did not implement as stated, for example an assumption about the gas
density.

## The pymrm plugin

The pymrm repository contains a plugin with skills for coding agents. It adds
the house conventions, a list of known pitfalls with tested examples, and a
workflow. You describe what you want in plain words; the plugin picks the
mode.

| You want | The plugin |
|---|---|
| a checked model and its answer (default) | builds the model, runs its own checks, reports the answer |
| a quick estimate: does a phenomenon matter? | evaluates the dimensionless criteria before any model is built |
| advice on modelling choices | discusses, for example, monolithic versus segregated coupling or the level of detail |
| a documented, independently verified model | writes a specification for your approval, has a separate agent verify the model, and writes a model card |
| teaching material | writes a flat notebook that builds the operators step by step |

The plugin installs in Claude Code and Codex CLI as a plugin, and in Gemini CLI
as a set of skills; the commands are in the
[pymrm README](https://github.com/computational-chemical-engineering/pymrm#developing-pymrm-models-with-a-coding-agent).
The skills are plain text files, so you can also read them as a compact guide
to writing pymrm models: start with the
[conventions skill](https://github.com/computational-chemical-engineering/pymrm/tree/main/plugins/pymrm/skills/conventions)
and its list of pitfalls.

## Checking what an agent gives you

Treat an agent's model like any model you did not write yourself: its
numbers are a claim until they are checked. The checks are the same ones this
book teaches for your own models, and pymrm has tools for several of them.

- **Boundary conditions.** Print what each dictionary imposes with
  [`describe_bc`](../api/symbols/pymrm.helpers.describe_bc.md) and compare it
  with the physical condition.
- **Grid and time-step refinement.** Refine and look at the observed order of
  convergence, for example with
  [`pymrm.checks.observed_orders`](../api/symbols/pymrm.checks.observed_orders.md).
- **The Jacobian.** Compare an analytical or assembled Jacobian with finite
  differences using
  [`pymrm.checks.check_jacobian`](../api/symbols/pymrm.checks.check_jacobian.md).
- **The solution.** `newton` reports success when its step is small, which is
  not the same as a small residual. Judge the result with
  [`pymrm.checks.residual_check`](../api/symbols/pymrm.checks.residual_check.md).
- **Thresholds and multiple steady states.** Locate them with a root finder,
  such as [`pymrm.checks.find_roots`](../api/symbols/pymrm.checks.find_roots.md),
  rather than reading them off a plotted curve.
- **An independent route.** Compare at least one headline number with a closed
  form, a limiting case, or a different method (for example `solve_bvp`).
- **A deliberate break.** Change something that must change the answer, such
  as the sign of a flux, and confirm that it does. A check that cannot fail
  proves nothing.
- **The problem statement.** Go through every condition in the problem (geometry,
  assumptions, boundary conditions, units, the definition of each reported
  quantity) and find the line of code that implements it.

## Learning with an agent

The exercises in this book train you to set up, discretise and check a model
yourself. That skill is what lets you judge an agent's output, so an agent is
most useful once you can do the exercise without it: to review your code, to
explore a variation, or to explain an error. Follow your course's rules on the
use of AI tools.
