# Household Subsystem

The `household/` subsystem owns the lifecycle of canonical households within ROOST.

Every analytical investigation begins with one or more canonical households.

A canonical household represents the financial state of an individual or family at a particular point in time independently of how that state was produced.

Internally, canonical households may be constructed, imported, discovered, generated programmatically, or restored from previous planning activities.

Externally, every canonical household presents the same analytical interface.

The household subsystem provides consistent discovery, registration, construction, import, export, and lifecycle management for canonical households while remaining independent of analytical methodology.

This document complements the project `README.md` and `ARCHITECTURE.md` by describing the architectural responsibilities owned by the household subsystem.
---

# Architectural Role

Within the overall ROOST architecture, the household subsystem owns canonical planning subjects.

Conceptually:

```text
Household Sources
        │
        ▼
Canonical Household
        │
        ▼
Planning Investigation
        │
        ▼
Characterization
        │
        ▼
Evidence Generation
```

The household subsystem owns canonical household definitions.

It does not own planning investigations.

It does not characterize households.

It does not generate evidence.

Its responsibility ends once a canonical household has been produced.

---

# Responsibilities

The household subsystem owns four primary responsibilities.

## Household Registration

The subsystem maintains a registry of households available to ROOST.

The registry provides a uniform view of all known households regardless of their origin.

Each registered household is represented by a `HouseholdSpec`.

A `HouseholdSpec` describes:

* Identity
* Metadata
* Provenance
* Construction method

The registry owns household discovery.

Consumers should not inspect the filesystem directly.

---

## Canonical Household Lifecycle

The household subsystem manages the lifecycle of canonical households.

Canonical households may originate from many sources while presenting a consistent analytical interface.

Examples include:

* programmatically generated households
* imported OWL household definitions
* household library snapshots
* educational examples
* published research cases
* future external providers

Construction is one mechanism within the lifecycle.

Import, export, registration, storage, and discovery are equally important responsibilities.

Consumers request canonical households.

They do not request particular construction mechanisms.

---

## Household Providers

Households are contributed through **Household Providers**.

A provider contributes one or more `HouseholdSpec` instances to the registry.

Examples include:

* Synthetic providers
* Imported household providers
* Tutorial providers
* Future Quicken providers
* Future web service providers

Each provider owns the mechanics required to construct its households.

The registry aggregates providers into a single semantic collection.

---

## Household Export

The household subsystem exports canonical households into forms required by downstream workflows.

Today the canonical export consists of:

* OWL `case.toml`
* optional Household Financial Profile (`HFP.xlsx`)

Future export formats may include notebooks, editors, or additional interchange formats.

Export remains independent of household construction.

---

# Household Providers

Household providers isolate the source of household information from its analytical use.

Conceptually:

```text
Synthetic Household
                │
Imported Household
                │
Tutorial Household
                │
Future Provider
                ▼
        HouseholdSpec
                ▼
      Household Registry
```

Consumers interact only with the registry.

The registry hides provider implementation details.

---

# Household Specifications

A `HouseholdSpec` is the canonical description of a registered household.

It contains metadata describing the household together with the mechanism required to construct it.

A `HouseholdSpec` is intentionally lightweight.

It should describe a household rather than contain instantiated runtime state.

Construction occurs on demand.

This allows households to remain reproducible while avoiding unnecessary duplication of runtime state.

---

# Canonical Households and Realizations

The household subsystem distinguishes canonical household definitions from their realizations.

Conceptually:

```text
Canonical Household
        ↓
Realization
```

Examples include:

```text
Canonical Household
        ↓
Planning Investigation

Canonical Household
        ↓
OWL Plan

Canonical Household
        ↓
Execution Artifacts
```

Canonical households describe financial state.

Realizations apply that state within a particular analytical context.

The household subsystem owns canonical households.

Other subsystems own their respective realizations.

---

# Relationship to OWL

ROOST builds upon OWL rather than replacing it.

OWL remains responsible for retirement modeling, optimization, simulation, and financial calculations.

Whenever practical, ROOST should leverage OWL's Python object model rather than introducing duplicate financial representations.

The household subsystem therefore serves primarily as an orchestration layer that discovers, constructs, and exports households while delegating financial behavior to OWL.

---

# Registry-Based Architecture

The household subsystem follows the same registration architecture used throughout ROOST.

Typical organization includes:

```text
bootstrap.py

registry.py

specs.py

providers/
```

Providers contribute households.

The registry organizes them.

The bootstrap assembles the complete registry.

New household sources should normally be introduced through additional providers rather than modifications to existing subsystem behavior.

---

# Testing and Validation

Registered households provide more than user-facing examples.

Each registered household is also an executable analytical fixture.

The registry enables consistent validation of household construction, serialization, workspace generation, execution planning, and evidence generation.

A single registered household may therefore support:

* Educational examples
* Documentation
* Integration testing
* Regression testing
* Performance benchmarking

Executable examples should be preferred over duplicated test fixtures whenever practical.

---

# Relationship to Other Subsystems

### Workspace

The workspace organizes planning investigations around one or more canonical households.

Workspaces preserve planning intent, characterization, analytical organization, and reproducibility.

The household subsystem provides canonical households.

The workspace determines how those households are investigated.

---

### Schema

The schema subsystem defines valid household configuration.

The household subsystem constructs households that satisfy that schema.

---

### Catalog

The catalog provides semantic identity for household observations.

The household subsystem provides the analytical inputs from which those observations are derived.

---

### Study

Studies define analytical methodology.

Households define the planning situations to which that methodology is applied.

---

### Metrics

Metrics describe evidence produced from household evaluations.

The household subsystem does not generate evidence.

---

# Architectural Invariants

The following concepts should remain stable.

## Every investigation begins with one or more canonical households.

Canonical households are the enduring planning subjects within ROOST.

Planning investigations, execution artifacts, and evidence are derived from canonical households without modifying their definition.

---

## Construction is independent of representation.

Households may originate from many sources while producing equivalent analytical definitions.

Consumers should not depend upon storage formats.

---

## Providers own acquisition.

Providers know how households are obtained.

The registry knows which households exist.

Consumers request households from the registry.

---

## Registration enables extensibility.

New household sources should normally be introduced through additional providers rather than modification of existing subsystem behavior.

---

## Canonical households remain independent of planning investigations.

Canonical households describe financial state.

Planning investigations organize analytical intent.

Execution artifacts preserve realized analyses.

Each concept has a distinct architectural owner.

---

## Households are reusable analytical assets.

A registered household may support education, documentation, experimentation, validation, benchmarking, and regression testing.

The same canonical household should be reused whenever practical.

---

## ROOST leverages OWL.

ROOST should prefer OWL's Python object model and analytical capabilities over reimplementing financial concepts.

The household subsystem coordinates household construction while OWL remains responsible for financial behavior.

---

# Long-Term Direction

The household subsystem is evolving toward the canonical lifecycle manager for households within ROOST.

Future capabilities are expected to include:

* richer household metadata
* additional import providers
* additional export providers
* programmatic household generation
* household library management
* improved validation
* snapshot creation
* longitudinal household histories
* enhanced reproducibility

Regardless of internal implementation, the subsystem should continue to answer one architectural question:

> **Which canonical households exist, how are they obtained, and how can they be represented consistently for analytical investigation?**

Everything beyond the canonical household belongs to other architectural subsystems.
