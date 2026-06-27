# ROOST Source Architecture

This directory contains the implementation of the ROOST architecture.

The project-level `README.md` describes **what ROOST is**.

`ARCHITECTURE.md` describes **the enduring architectural principles** that guide its design.

This document describes **how those architectural concepts are realized by the current source tree**.

Implementation details will evolve over time.

The architectural responsibilities described here should evolve much more slowly.

---

# Source Tree Philosophy

The source tree is organized around architectural responsibilities rather than execution order.

Each major subsystem owns one conceptual responsibility.

Subsystems expose reusable services and semantic observations.

Higher-level workflows emerge through composition rather than direct coupling.

No subsystem should require knowledge of another subsystem's internal implementation.

---

# Architectural Mapping

Conceptually, ROOST follows the workflow described in `ARCHITECTURE.md`.

```text
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
Evidence Package
```

The current source tree realizes that workflow through a collection of cooperating subsystems.

---

# Subsystem Responsibilities

Each major package owns one architectural concept.

## workspace/

Owns characterization of the current analytical context.

Responsibilities include:

* workspace organization
* inventory
* semantic levers
* transition applicability
* execution materialization
* sessions, runs, and trials

The workspace understands the current planning situation.

It does not generate evidence.

---

## catalog/

Owns semantic identity.

Responsibilities include:

* canonical field definitions
* ontology
* provenance
* explainability
* semantic resolution

The catalog defines what can be observed.

---

## schema/

Owns household configuration schema.

Responsibilities include:

* configuration specifications
* validation
* defaults
* canonical household structure

The schema defines valid analytical inputs.

---

## study/

Owns reusable analytical definitions.

Responsibilities include:

* studies
* transition families
* experiments
* execution planning

Studies define analytical intent.

Experiments define evidence-generation methodologies.

---

## metrics/

Owns analytical evidence.

Responsibilities include:

* metric definitions
* derived evidence
* aggregation
* comparison metrics

Metrics describe what was learned.

---

## display/

Owns presentation.

Responsibilities include:

* display fields
* views
* formatting
* reports
* visualization support

Display determines how evidence is communicated.

It does not generate evidence.

---

## comparison/

Owns analytical comparison.

Responsibilities include:

* comparisons
* comparative metrics
* evidence organization
* comparative reporting

Comparison relates multiple evidence sets.

---

## review/

Owns workflow orchestration.

Responsibilities include:

* guidance
* workflow sequencing
* subsystem composition
* user-facing orchestration

Review coordinates subsystems.

It does not own analytical knowledge.

---

## Additional Packages

Other packages support the architectural workflow by providing specialized capabilities.

Each should own a single coherent responsibility.

Subsystem READMEs describe these responsibilities in greater detail.

---

# Subsystem Independence

Subsystems should communicate through semantic services rather than implementation details.

Subsystems should not directly manipulate another subsystem's internal state.

Ownership remains local.

Composition occurs above subsystem boundaries.

---

# Registration

Many subsystems support registration-based extension.

Typical organization includes:

```text
bootstrap.py

registry.py

specs.py

plugins/
```

Registries organize capabilities.

Plugins contribute capabilities.

Bootstraps assemble complete subsystem instances.

Registration allows new functionality to be introduced without modifying existing subsystem behavior.

---

# Subsystem READMEs

Every major subsystem should provide its own README.

Subsystem READMEs answer a single question:

> **What architectural responsibility does this subsystem own?**

Subsystem documentation should describe:

* ownership
* responsibilities
* architectural boundaries
* major concepts
* extension points

Subsystem READMEs should avoid repeating project philosophy already described by `README.md` or `ARCHITECTURE.md`.

---

# Guiding Principle

The source tree should mirror the architecture.

Packages exist because architectural responsibilities exist.

As implementation evolves, packages may change.

Architectural responsibilities should remain stable.

The preferred direction is always:

> One subsystem.
>
> One responsibility.
>
> One clear architectural owner.
