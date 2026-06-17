# ROOST Architecture

This directory contains the current implementation of ROOST.

The architecture described in this document represents the current implementation of ROOST.

The top-level README describes the
conceptual model, scientific philosophy,
and long-term direction of the project.

This document describes how those concepts
are realized within the current codebase,
including subsystem boundaries, data flow,
registry integration, execution structure,
and implementation responsibilities.

Subsystem-specific details are documented
within their respective README files.

# Core Principles

## Catalog integrates semantic registries

ROOST separates semantic concerns across
multiple specialized registries.

Examples include:

    schema
    metrics
    display
    study

Each registry owns a distinct semantic
domain.

The catalog subsystem integrates metadata,
relationships, provenance, lineage, and
introspection across these registries.

Conceptually:

```
Schema
Metrics
Study
     ↓
  Catalog
     ↓
  Display
     ↓
  Renderers
```

The catalog does not replace registry
ownership.

Instead it provides a unified semantic
identity graph spanning the system.

## Display is layered on top of semantic entities.

Display consumes semantic entities from:

    schema
    metrics
    study
    catalog

and projects them into human-oriented
analytical presentations.

Conceptually:

```
Schema
Metrics
Study
     ↓
  Catalog
     ↓
  Display
     ↓
  Renderers
```

Display owns presentation behavior.

Catalog remains the authoritative source
for semantic identity, provenance,
lineage, and explainability.


## Execution and Analysis Layers

Roost operates across multiple semantic layers:

```text
Case
  ↓
Session
  ↓
Run
  ↓
Trial
```

Each layer represents a different dataset abstraction:

| Layer      | Row Represents            |
| ---------- | ------------------------- |
| case       | one TOML case file        |
| session    | one session directory     |
| run        | one parameterized run     |
| trial      | one stochastic simulation |

Views are registered against a specific layer.

We also introduce two additional layers.

```text
Experiment
    ↓
Related Runs
```

Experiments are logical scientific
overlays and are independent of
filesystem organization.


## Pure data pipeline

The system is a pipeline:

```text
Case
    ↓
Session Materialization
    ↓
Run Generation
    ↓
Trial Execution
    ↓
Metrics
    ↓
Aggregation
    ↓
Display
    ↓
Reporting

```

Each stage:

* consumes structured data
* produces structured data
* does not depend on presentation concerns

## Functional core, thin orchestration

* Core logic is pure and testable
* Side effects (filesystem, CLI, Hydra, rendering) are isolated
* CLI commands are orchestration layers only

## Test-driven development (TDD)

All features are introduced via tests:

1. write failing test
2. implement minimal code
3. make test pass
4. refactor
5. repeat

Legacy tests are used as behavioral references only.

# Top-Level Modules

```text
owlroost/
    catalog/     ← semantic metadata and introspection
    schema/      ← executable inputs
    metrics/     ← modeled outputs and aggregation
    display/     ← presentation overlays
    study/       ← analytical guidance
    hydra/       ← Hydra-facing experiment generation
    core/        ← execution + metrics extraction
    cli/         ← command-line interface (thin wrappers)
    tools/       ← validation and developer tooling

```

Conceptually:

    Schema
    Metrics
    Study
         ↓
      Catalog
         ↓
      Display
         ↓
      Renderers

Responsibilities are intentionally
separated.

Schema
    executable inputs

Metrics
    modeled outputs

Study
    analytical guidance

Catalog
    identity, lineage,
    provenance, explainability

Display
    presentation and analytical views

# Registry Layering

ROOST currently distinguishes between major semantic registry domains:

| Registry            | Primary Responsibility                         |
| ------------------- | ---------------------------------------------- |
| `schema/`           | Executable configuration ontology              |
| `metrics/`          | Modeled runtime output ontology                |
| `study/`            | Executable configuration ontology              |
| `catalog/`          | Identity, provenance, lineage, explainability  |
| `display/`          | Presentation and analytical overlays           |

These registries intentionally represent different semantic domains rather than duplicated metadata systems.

# Registry Relationships

Conceptually:

    Schema
    Metrics
    Study
         ↓
      Catalog
         ↓
      Display
         ↓
      Reports
      Dashboards
      CLI Views

Schema, metrics, and study define
semantic entities.

Catalog integrates semantic metadata.

Display projects those entities into
human-oriented analytical views.


# Module Responsibilities

## schema/

The schema registry defines the authoritative executable configuration ontology for ROOST and OWL integration.

Responsibilities include:

* OWL input variable discovery
* Runtime configuration semantics
* Runtime-default discovery
* Hydra configuration generation
* Hydra sweepability
* Runtime materialization support
* Compatibility and helper fields
* Executable configuration validation

The schema registry is intentionally exhaustive across the executable OWL input domain.

This is a critical architectural requirement.

Complete schema coverage ensures that:

* Hydra sweep generation remains complete
* All executable configuration variables remain discoverable
* Study templates can enumerate valid parameter spaces
* Runtime materialization remains reproducible
* Users are not forced to rely on ad hoc Hydra `+variable=value` syntax

The schema registry therefore functions as:

```text
the executable configuration ontology of ROOST
```

rather than merely a documentation or validation system.

Schema fields may originate from:

* OWL Pydantic models
* OWL runtime-discovered defaults
* ROOST runtime extensions
* Compatibility overlays
* Helper and derived runtime variables

See schema/README.md.


## catalog/

Provides semantic identity,
provenance, lineage, introspection,
and explainability infrastructure.

Catalog integrates metadata across:

    schema
    metrics
    display
    study

Catalog owns:

    ontology dimensions
    semantic relationships
    lineage
    provenance integration
    explainability

Catalog does not replace registry
ownership.

Schema, metrics, study, and display
remain authoritative within their
domains.

Catalog integrates semantic identity,
relationships, provenance, and
introspection across registries.

See catalog/README.md.

## metrics/

The metrics registry defines the authoritative ontology for modeled runtime outputs and statistical aggregation semantics.

Responsibilities include:

* Canonical output metric definitions
* Statistical aggregation semantics
* Metric typing and interpretation
* Aggregation-level compatibility
* Output-level provenance semantics
* Runtime observation interpretation

Metrics represent modeled evidence generated by runs and trials.

Examples include:

* Spending outcomes
* Bequest distributions
* Success probabilities
* Runtime durations
* Convergence metrics
* Computational complexity metrics
* Sampling stability measurements



See metrics/README.md.

## display/

The display registry defines the analytical projection and presentation layer used by reporting, CLI rendering, views, tables, and comparative analysis workflows.


Display owns:

    fields
    profiles
    groups
    views
    dashboards

Display consumes semantic entities from:

    schema
    metrics
    catalog

See display/README.md.

## study/

Provides analytical guidance above the
execution architecture.

Study owns:

    decisions
    choice templates
    levers

Study helps users move from:

    What question should I investigate?

to:

    What experiments should I run?

See study/README.md.

## hydra/

> Experiment/run/trial generation.

Transforms:

```text
case.toml + overrides → experiments → runs → trials
```

### Responsibilities

* interpret override space
* expand experiments into runs
* generate trial configurations
* manage Hydra integration
* write effective configuration artifacts

### Notes

Hydra is an implementation tool—not the core architecture model.

## core/

> Trial execution and metrics extraction.

### Responsibilities

* execute OWL planner
* normalize outputs
* capture metrics
* enforce consistent failure handling
* produce structured outputs

### Output

```text
trial_result = {
  inputs: {...},
  outputs: {...},
  metadata: {...}
}
```

## cli/

> Thin orchestration layer.

### Responsibilities

* parse commands/options
* select datasets
* select views
* invoke display/materialization
* invoke execution pipeline

### No business logic

CLI commands should contain minimal logic.

# Execution Architecture

ROOST currently organizes execution
through:

    Case
        ↓
    Session
        ↓
    Run
        ↓
    Trial

Scientific interpretation remains
logically distinct:

    Experiment
        ↓
    Related Runs

# Filesystem Provenance

ROOST separates:

    scientific organization

from

    operational organization

Operational provenance follows:

    Case
        ↓
    Session
        ↓
    Run
        ↓
    Trial

Filesystem paths are the canonical
operational provenance identifiers.

Experiments provide logical scientific
organization and may span multiple:

    sessions
    dates
    cases
    execution environments



# Operational Realization Layer

ROOST separates semantic variable definition from runtime operational realization.

Operational realization occurs during dataset loading and execution discovery.

Canonical runtime dataset rows currently distinguish between:

| Dataset Component | Responsibility                              |
| ----------------- | ------------------------------------------- |
| `_inputs`         | Materialized executable configuration       |
| `_metrics`        | Runtime results and aggregations            |
| `_meta`           | Operational metadata and transient identity |
| `_paths`          | Filesystem provenance and execution lineage |

This distinction allows ROOST to preserve separation between:

* Semantic ontologies
* Runtime execution state
* Modeled runtime evidence
* Filesystem provenance
* Analytical overlays

Filesystem paths remain the canonical operational provenance identifiers throughout the system.

# Data Flow

```text
case.toml
   ↓
hydra/planner
   ↓
experiments / runs / trials
   ↓
trial execution
   ↓
trial outputs + metrics
   ↓
aggregation
   ↓
display materialization
   ↓
RoostTable
   ↓
renderers / reports / CLI
```

# Semantic Projection vs Hierarchical Projection

ROOST currently distinguishes between two different forms of projection.

## Semantic Projection

Semantic projection maps canonical semantic registries into analytical display overlays.

Conceptually:

```text
schema ontology
metrics ontology
        ↓
display ontology
```

This projection stage synthesizes renderer-facing analytical representations while preserving canonical semantic ownership in the underlying registries.

## Hierarchical Projection

Hierarchical projection maps runtime entities across operational aggregation levels.

Examples include:

```text
trial → run
run → session
session → case
```

These projections aggregate operational observations and statistical evidence across the canonical execution hierarchy defined elsewhere in this document.

The distinction between semantic projection and hierarchical projection is intentional and architecturally important.


# Provenance and Introspection

ROOST treats provenance as a first-class architectural concern.

Provenance includes both:

* Operational execution provenance
  and
* Semantic variable provenance

Examples include:

* Variable origin registry
* Runtime storage location
* Materialized execution paths
* Aggregation lineage
* Display override lineage
* Hydra generation provenance
* Runtime discovery provenance
* Report and view usage

ROOST is evolving toward a dedicated catalog and introspection architecture capable of tracing:

Catalog provides provenance,
lineage, introspection, and
explainability infrastructure.

Conceptually:

```
    semantic variable
        ↓
    runtime materialization
        ↓
    aggregation
        ↓
    display projection
        ↓
    report usage
```

The catalog subsystem records and
exposes these relationships.

across the entire analytical pipeline.

This provenance architecture is foundational to:

* Explainability
* Reproducibility
* Study generation
* QA/QC validation
* Structural comparison
* Merge compatibility analysis
* Runtime debugging
* Reporting and publication workflows

See catalog/README.md

# Command Model

Commands naturally operate at different dataset layers.

| Command       | Primary Layer            |
| ------------- | ------------------------ |
| `cmd_build`   | case                     |
| `cmd_run`     | run                      |
| `cmd_results` | run / trial / experiment |
| `cmd_report`  | any                      |

Each command defines default views appropriate for its layer.

# Testing Strategy

## Active tests

Located in:

```text
tests/
```

Focus on:

* schema correctness
* display materialization
* aggregation correctness
* renderer behavior
* experiment generation
* execution correctness
* end-to-end golden tests


# Design Non-Goals

ROOST is NOT intended to:

* Optimize only for deterministic single-plan analysis
* Restrict experiments to single-case analysis

* Collapse experiments directly into filesystem structure
* Conflate execution provenance with scientific interpretation
* Treat sessions as primary scientific result entities
* Treat all hierarchy levels as semantically identical
* Treat transient operational IDs as stable scientific identifiers
* Conflate runtime observations with structural run identity
