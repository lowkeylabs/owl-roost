# Household Subsystem

The `household/` subsystem owns the canonical definition, construction, and registration of households within ROOST.

Every analytical investigation performed by ROOST begins with a household.

A household represents the enduring subject of retirement planning rather than a particular point in time.

The household subsystem provides a consistent mechanism for discovering, constructing, validating, and exporting households regardless of how those households were originally created.

This document complements the project `README.md` and `ARCHITECTURE.md` by describing the architectural responsibilities owned by the household subsystem.

---

# Architectural Role

Within the overall ROOST architecture, the household subsystem provides the canonical planning context.

Conceptually:

```text
Household Provider
        ↓
Household Registry
        ↓
Household Definition
        ↓
Workspace
        ↓
Realized Planning State
        ↓
Characterization
        ↓
Levers
        ↓
Experiments
```

The household subsystem owns the definition of households.

The workspace owns the current realized planning state of a household.

The household subsystem does not own analytical methodology.

It does not generate evidence.

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

## Household Construction

The subsystem constructs canonical household definitions.

Construction is intentionally separated from storage.

A household may originate from many sources while producing an equivalent analytical definition.

Examples include:

* Programmatically generated households
* Imported OWL household definitions
* Educational examples
* Published research cases
* Future external data sources

Consumers request a household.

They do not request a particular storage representation.

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

The subsystem exports households into operational forms required by downstream workflows.

Examples include:

* ROOST workspaces
* OWL configuration files
* Household Financial Profile workbooks
* Future notebook generation
* Future graphical editors

Export is distinct from construction.

A single household definition may be exported into many different representations.

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

# Definition versus Realization

The household subsystem distinguishes between a household definition and the operational artifacts derived from it.

Conceptually:

```text
Household Definition
        ↓
Realization
```

Examples include:

```text
Household Definition
        ↓
Workspace

Household Definition
        ↓
OWL Plan

Household Definition
        ↓
Configuration File

Household Definition
        ↓
Household Financial Profile
```

The household definition represents the enduring planning subject.

Operational artifacts represent particular realizations of that household for execution, editing, persistence, or interoperability.

The workspace realizes the current planning state of a household by combining its canonical definition with the accumulated realized changes that have occurred over time.

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

The workspace realizes the current planning state of a household.

A workspace combines a canonical household definition with the accumulated realized changes describing the household at the time of review.

Characterization, lever computation, transition discovery, and execution planning operate on this realized planning state.

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

## Every investigation begins with a household.

The household is the enduring analytical context within ROOST.

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

## Household definitions are stable.

The household definition describes the enduring planning subject.

Current planning state belongs to the workspace.

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

The household subsystem is evolving toward the canonical entry point for retirement planning within ROOST.

Future capabilities are expected to include:

* Richer household metadata
* Additional household providers
* Programmatic household generation
* Improved import and export workflows
* Automated workspace creation
* Round-trip serialization
* Enhanced validation
* Executable regression suites
* Longitudinal household evolution through repeated planning reviews

The household subsystem should increasingly answer a single architectural question:

> **What households are available, how can they be constructed, and how can they serve as the enduring planning context for analytical investigation?**

Every subsequent stage of the ROOST workflow builds upon that foundation.
