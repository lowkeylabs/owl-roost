# ROOST Architecture

This document describes the enduring architectural principles of ROOST.

Unlike `README.md`, which introduces the project, and `FUTURE-README.md`, which describes the long-term product vision, this document captures the software architecture philosophies that guide implementation decisions.

The goal is not to describe the current codebase.

The goal is to describe how ROOST should be built.

As the implementation evolves, the principles in this document should remain relatively stable.

---

# Architectural Philosophy

ROOST is designed as a collection of independent, deterministic subsystems that cooperate through well-defined interfaces.

Each subsystem owns a single area of responsibility.

Subsystems expose semantic observations and services rather than implementation details.

Higher-level workflows compose these subsystems without taking ownership of their knowledge.

This separation supports:

* deterministic behavior
* reproducibility
* explainability
* extensibility
* multiple user interfaces
* long-term maintainability

---

# Architectural Principles

## Separation of Responsibilities

Every major subsystem should own one concept.

Examples include:

* Workspace
* Study
* Comparison
* Display
* Metrics
* Review

Ownership should remain local.

Composition should occur at higher levels.

Subsystems should avoid reaching into each other's internal structures.

---

## Thin Interfaces

ROOST should support multiple user interfaces without duplicating implementation.

Interfaces may include:

* Command-line interface (CLI)
* Python API
* Jupyter notebooks
* Quarto documents
* Future graphical interfaces
* Future web services

Conceptually:

```text
CLI

Notebook

Quarto

GUI

        ↓

Common Python Service Layer

        ↓

ROOST Subsystems

        ↓

OWL
```

No interface should contain business logic.

The CLI should remain a thin wrapper around reusable Python services.

---

## Service-Oriented Design

Subsystems should expose Python services rather than requiring invocation through command-line interfaces.

For example:

```python
build(...)

run(...)

results(...)

review(...)
```

should be directly callable from Python.

The CLI should invoke these same services.

This ensures that:

* notebooks
* Quarto
* automation
* testing
* future interfaces

all share identical implementations.

---

## Determinism

ROOST prioritizes deterministic execution.

Given identical:

* household
* assumptions
* execution plans
* software versions

ROOST should generate identical evidence.

Automation should never obscure how evidence was generated.

---

## Reproducibility

Every analytical artifact should be reproducible.

Users should always be able to determine:

* what was executed
* why it was executed
* what assumptions were used
* what evidence was generated

Reproducibility is considered a first-class architectural objective.

---

## Provenance

ROOST maintains provenance throughout the analytical workflow.

Examples include:

* household inputs
* execution plans
* overrides
* generated evidence
* reports
* comparison artifacts

Artifacts should preserve sufficient metadata to reconstruct how they were created.

---

## Explainability

Every meaningful observation should be explainable.

ROOST prefers semantic observations over opaque implementation details.

Where possible, observations should include:

* descriptions
* provenance
* definitions
* rationale

Explainability supports:

* users
* educators
* researchers
* advisors
* LLMs

---

## Definitions and Realizations

ROOST distinguishes reusable definitions from realized artifacts.

Examples include:

```text
Study
    ↓
Evidence Package

Execution Plan
    ↓
Runs

Display View
    ↓
Rendered Table
```

Definitions describe intent.

Realizations describe execution.

This distinction improves reuse while preserving provenance.

---

## Composability

ROOST favors composition over monolithic implementations.

Small reusable capabilities should be combined into larger workflows.

Examples include:

```text
Review

    Phase

        Activity

            Checks

            Actions
```

Each level has a single responsibility.

Complex workflows should emerge from composing simple pieces.

---

## Extensibility

Subsystems should be extended through registration rather than modification.

Typical subsystem organization includes:

```text
bootstrap.py

registry.py

specs.py

plugins/
```

Plugins contribute capabilities.

Registries organize capabilities.

Bootstraps assemble complete subsystems.

Hard-coded lists should be avoided whenever practical.

---

## Semantic Resolution

Subsystems should communicate through semantic observations rather than direct access to implementation details.

Conceptually:

```text
Observation

        ↓

Resolution

        ↓

Workspace

Metrics

Comparison

Inputs

Display Functions
```

Consumers should request observations.

They should not need to know where those observations originate.

This decouples workflows from storage.

---

## Review as Orchestration

Review is responsible for orchestrating retirement planning workflows.

Review does not own analytical knowledge.

Instead, Review composes capabilities from other subsystems.

Examples include:

* Workspace checks
* Study levers
* Execution planning
* Evidence generation
* Comparison
* Reporting

Review owns sequence.

Subsystems own expertise.

---

## Power Users and Guided Users

ROOST supports multiple styles of interaction.

Power users may invoke individual tools directly.

For example:

```text
roost workspace

roost build

roost run

roost results

roost reports
```

Other users may prefer guided workflows.

For example:

```text
roost review
```

Both interaction styles should use the same underlying services.

No functionality should exist exclusively within the CLI.

---

## Evidence Before Interpretation

ROOST generates evidence.

Interpretation is intentionally separate.

Interpretation may be performed by:

* users
* advisors
* researchers
* educators
* LLMs

ROOST should clearly distinguish generated evidence from subsequent interpretation.

---

# Architectural Goal

ROOST should evolve as a coherent collection of independent, composable, deterministic subsystems.

Every subsystem should remain understandable in isolation.

Higher-level workflows should emerge through composition rather than duplication.

The architecture should support future interfaces, future workflows, and future analytical capabilities without requiring fundamental redesign.

The guiding philosophy is simple:

> Define capabilities once.
>
> Compose them many ways.
>
> Preserve provenance always.
