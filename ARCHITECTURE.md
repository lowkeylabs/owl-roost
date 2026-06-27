# ROOST Architecture

This document describes the enduring software architecture of ROOST.

Unlike `README.md`, which explains **what ROOST is**, this document explains **how ROOST is organized** and the architectural principles that guide its implementation.

This document intentionally avoids describing the current package layout or implementation details.

Its purpose is to capture the architectural ideas that should remain stable even as the implementation evolves.

Subsystem READMEs describe how these ideas are realized within the current codebase.

---

# Architectural Philosophy

ROOST is an evidence-generation system composed of independent, deterministic subsystems with well-defined responsibilities.

Each subsystem owns a distinct concept.

Subsystems expose semantic observations and reusable services rather than implementation details.

Higher-level workflows emerge through composition rather than duplication.

This architecture emphasizes:

* Determinism
* Explainability
* Reproducibility
* Extensibility
* Composability
* Long-term maintainability

---

# The Architectural Boundary

ROOST deliberately separates evidence generation from decision making.

Conceptually:

```text
Outside ROOST

Questions
Interpretation
Recommendations
Decisions

──────────────────────────────────────────

ROOST

Household
    ↓
Characterization
    ↓
Levers
    ↓
Transition Discovery
    ↓
Experiments
    ↓
Evidence
    ↓
Evidence Packages

──────────────────────────────────────────
```

ROOST owns evidence generation.

Interpretation and recommendation belong to people, advisors, educators, researchers, or future AI systems built on top of ROOST.

This separation is fundamental.

---

# Architectural Workflow

Conceptually, every investigation follows the same workflow.

```text
Household
    ↓
Characterization
    ↓
Levers
    ↓
Applicable Transition Families
    ↓
Transitions
    ↓
Experiments
    ↓
Evidence
    ↓
Evidence Package
```

Every subsystem contributes to one or more stages of this workflow.

No subsystem owns the entire workflow.

---

# Characterization

Characterization is the process of understanding the current planning situation.

Rather than exposing raw inputs directly, ROOST computes semantic observations describing the household and analytical context.

These observations are called **Levers**.

Levers may be:

* Boolean
* Categorical
* Continuous
* Derived

Levers characterize the current planning situation.

They determine which transition families are applicable and constrain the valid transitions available for exploration.

Levers are computed rather than manually maintained.

---

# Transitions

ROOST evaluates change.

A transition represents a meaningful change from the current planning situation.

Examples include:

* Retire one year later
* Increase spending
* Delay Social Security
* Perform Roth conversions
* Change asset allocation

Transitions represent candidate actions.

ROOST evaluates transitions.

ROOST does not recommend them.

Related transitions may be organized into Transition Families.

---

# Evaluation Environments

Transitions are evaluated within one or more future environments.

Evaluation environments describe assumptions about the future rather than choices made by the retiree.

Examples include:

* Historical markets
* Bootstrap markets
* Inflation assumptions
* Longevity assumptions
* Tax assumptions

Evaluation environments remain independent from transitions.

Experiments combine transitions with evaluation environments to generate evidence.

---

# Evidence Generation

Experiments generate evidence.

An experiment defines a deterministic methodology for evaluating one or more transitions under one or more evaluation environments.

Evidence generation should always be:

* Deterministic
* Reproducible
* Explainable
* Inspectable

Experiments define methodology.

Evidence packages describe results.

---

# Definitions and Realizations

ROOST distinguishes reusable analytical definitions from realized execution artifacts.

Conceptually:

```text
Definition
        ↓
Realization
```

Examples include:

```text
Transition Family
        ↓
Transitions

Experiment
        ↓
Session

Display View
        ↓
Rendered Presentation
```

Definitions describe analytical intent.

Realizations preserve execution history.

Maintaining this distinction improves reuse while preserving provenance.

---

# Separation of Responsibilities

Every major subsystem owns one architectural responsibility.

Subsystems should own knowledge rather than workflows.

Higher-level workflows emerge through composition.

Subsystems should communicate through semantic interfaces rather than implementation details.

Ownership should remain local.

Composition should occur above subsystem boundaries.

---

# Semantic Communication

Subsystems communicate through semantic observations rather than storage structures or implementation details.

Consumers request meaning rather than location.

Conceptually:

```text
Semantic Observation
        ↓
Resolution
        ↓
Consumer
```

Consumers should not require knowledge of:

* Filesystem layout
* Storage representation
* Runtime implementation
* Internal subsystem organization

Semantic communication promotes loose coupling and explainability.

---

# Explainability

Every meaningful observation should be explainable.

Explainability should include:

* Description
* Provenance
* Lineage
* Rationale
* Dependencies

Explainability is considered a first-class architectural concern rather than a reporting feature.

---

# Provenance

ROOST preserves provenance throughout the analytical lifecycle.

Provenance explains:

* What was evaluated
* How it was evaluated
* Why it was evaluated
* Which assumptions were used
* Which evidence was produced

Artifacts should preserve sufficient information to reproduce and explain their creation.

---

# Determinism

Given identical:

* Household
* Levers
* Transition definitions
* Evaluation environments
* Execution configuration
* Software versions

ROOST should generate identical evidence.

Automation should never obscure reproducibility.

---

# Service-Oriented Architecture

ROOST functionality should be exposed through reusable Python services.

User interfaces should remain thin orchestration layers.

Interfaces may include:

* Command-line tools
* Python APIs
* Jupyter notebooks
* Quarto documents
* Future graphical interfaces
* Future web services

All interfaces should invoke the same underlying services.

Business logic should not reside within user interfaces.

---

# Composability

Complex analytical workflows should emerge by composing simple capabilities.

Subsystems should provide focused responsibilities that can be reused in many workflows.

Composition should be preferred over duplication.

---

# Extensibility

Subsystems should be extended through registration rather than modification.

Architectural extension points should remain open while subsystem responsibilities remain stable.

New analytical capabilities should normally be introduced without modifying existing subsystem behavior.

---

# Documentation

Documentation is considered an architectural outcome.

ROOST should generate evidence that is understandable, reviewable, reproducible, and shareable.

Documentation should explain both:

* Analytical intent
* Generated evidence

Documentation is part of the evidence-generation process rather than an afterthought.

---

# Architectural Invariants

The following concepts are foundational to ROOST.

These concepts should remain stable unless intentionally redesigned.

## Households are the primary analytical context.

Every investigation begins with a household.

---

## Characterization precedes analysis.

ROOST first understands the current planning situation before determining applicable analytical workflows.

---

## Levers characterize the planning situation.

Levers are semantic observations that determine analytical applicability and constrain available transitions.

---

## Transitions represent candidate change.

ROOST evaluates transitions.

ROOST does not recommend them.

---

## Evaluation environments represent possible futures.

Transitions are evaluated under one or more future environments.

Environments remain independent of retiree decisions.

---

## Experiments generate evidence.

Experiments define reproducible methodologies.

Evidence packages describe their results.

---

## Definitions remain distinct from realizations.

Analytical definitions describe intent.

Execution artifacts record realized evidence.

---

## Evidence generation and interpretation remain separate.

ROOST generates evidence.

Consumers interpret evidence.

Recommendation logic remains outside the architectural boundary.

---

## Subsystems own concepts.

Subsystems own knowledge.

Higher-level workflows compose subsystem capabilities.

Subsystems should avoid owning each other's responsibilities.

---

## Semantic interfaces are preferred.

Subsystems communicate through semantic observations rather than implementation details.

---

## Documentation is a first-class architectural artifact.

Generated evidence should remain understandable, reproducible, and explainable.

---

# Architectural Goal

ROOST should evolve as a coherent collection of independent, composable subsystems that together form a deterministic evidence-generation engine.

Each subsystem should remain understandable in isolation.

The architecture should support new workflows, new analytical methodologies, and new user interfaces without requiring fundamental redesign.

The guiding philosophy is simple:

> Characterize the present.
>
> Evaluate meaningful transitions.
>
> Generate trustworthy evidence.
>
> Preserve explainability always.
