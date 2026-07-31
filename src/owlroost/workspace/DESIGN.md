# Workspace Design Notes

This document captures the current architectural direction of the Workspace subsystem.

Unlike `README.md`, which describes the enduring responsibilities of the Workspace subsystem, this document records the current design evolution and implementation strategy.

The ideas described here are intentionally forward-looking and may evolve as implementation proceeds.

The architectural invariants described below should change much more slowly than the implementation.

---

# Design Direction

The Workspace subsystem is evolving beyond simple filesystem discovery.

The Workspace is becoming the semantic integration point for an entire retirement planning investigation.

Conceptually, the Workspace connects:

* the filesystem
* canonical household definitions
* study methodology
* execution artifacts
* planning activities
* published evidence

into a single coherent planning context.

The Workspace therefore answers one architectural question:

> **What retirement planning situation currently exists?**

Every other subsystem either contributes information to that answer or consumes the resulting characterization.

---

# Top-Down Development

The current implementation strategy intentionally proceeds from the top down.

Rather than beginning with low-level workspace observations and gradually constructing user-facing objects, the Workspace first defines the semantic objects that users, advisors, reports, and LLMs ultimately consume.

The implementation then works backwards, identifying the semantic observations required to materialize those objects.

This approach intentionally mirrors the development of other major ROOST subsystems, where semantic objects are defined before the underlying implementation.

---

# Planning Context

The next major Workspace responsibility is the construction of planning context objects.

These objects describe the current retirement planning situation.

They are semantic summaries rather than filesystem observations.

Planning context objects consume Workspace observations but are not themselves Workspace observations.

---

# Household Planning Context

Each household participating in a planning investigation produces one Household Planning Context.

Conceptually:

```text
Canonical Household
        +
Workspace Characterization
        +
Applicable Studies
        ↓
Household Planning Context
```

A Household Planning Context should communicate:

* the current retirement situation
* planning objectives
* planning opportunities
* planning constraints
* applicable scenario families
* overall planning summary

This object intentionally contains no execution artifacts, analytical evidence, or recommendations.

Its purpose is to describe the planning situation rather than interpret it.

---

# Workspace Planning Context

A Workspace may contain one or more households.

Accordingly, the Workspace produces a Workspace Planning Context describing the planning investigation as a whole.

Conceptually:

```text
Workspace

    ├── Household Planning Context

    ├── Household Planning Context

    └── Household Planning Context

            ↓

    Workspace Planning Context
```

The Workspace Planning Context provides the semantic entry point into the planning investigation.

It may eventually summarize:

* participating households
* current planning cycle
* applicable studies
* evidence coverage
* publication status
* planning progress

The Workspace Planning Context should become the primary object displayed by:

```text
roost .
```

---

# Relationship to Workspace Observations

Workspace observations remain the canonical semantic API describing the planning investigation.

Each observation represents one independently computable fact.

Examples include:

* workspace identity
* workspace inventory
* household characterization
* execution state
* evidence state

Planning Context objects consume those observations.

They should never duplicate the underlying computations.

Instead they provide higher-level semantic organization.

Conceptually:

```text
Filesystem

        ↓

Workspace Inventory

        ↓

Workspace Observations

        ↓

Household Planning Context

        ↓

Workspace Planning Context
```

---

# Relationship to Activities

Planning Activities should consume Planning Context rather than directly inspecting workspace observations.

Activities answer:

> What prevents this planning goal from already being complete?

Planning Context answers:

> What planning situation currently exists?

The Activity subsystem therefore operates at a higher semantic level while remaining completely explainable through the underlying Workspace observations.

---

# Relationship to the Published Evidence Package

The published evidence package represents the eventual product of a planning investigation.

The Planning Context becomes the opening portion of that package.

Subsequent sections include:

* household specification
* analytical evidence
* comparative analysis
* execution provenance

Planning Context therefore provides the semantic bridge between the Workspace and published evidence.

---

# Explainability

Explainability remains a fundamental architectural invariant.

Every statement appearing within a Planning Context should ultimately be traceable back to one or more Workspace observations.

Planning Context objects should contain no hidden reasoning.

They are deterministic semantic syntheses of observable planning facts.

---

# Current Scope

The initial implementation intentionally focuses on scaffolding.

Planning Context objects will initially contain placeholders and gradually acquire additional semantic sections as Workspace observations become richer.

The implementation should evolve by repeatedly asking:

> What information should appear in the Planning Context?

Only after answering that question should additional Workspace observations be introduced.

This ensures that every new semantic observation serves a clearly identifiable planning purpose.

---

# Architectural Invariants

The following principles should guide future implementation.

* The Workspace owns characterization of the current planning situation.
* Planning Context objects are semantic syntheses rather than primitive observations.
* Planning Context objects are semantic documents rather than projections.
* Workspace observations remain the canonical semantic API.
* Planning Context objects consume the effective Workspace observations (after configuration has been applied).
* Planning Context contains no execution logic.
* Planning Context contains no analytical interpretation or recommendations.
* Every Planning Context statement should remain explainable through underlying Workspace observations.
* Development should continue from the top down by refining the semantic objects first and introducing new Workspace observations only as needed to materialize them.
