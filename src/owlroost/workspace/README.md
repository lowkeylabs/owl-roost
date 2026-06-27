# Workspace Subsystem

The `workspace/` subsystem owns the current analytical context within ROOST.

A workspace represents a self-contained retirement planning environment containing the information required to characterize a household, organize analytical artifacts, discover applicable investigations, and materialize evidence.

The workspace does **not** define analytical methodology.

The workspace provides the context in which analytical methodology is applied.

This document complements the project `README.md` and `ARCHITECTURE.md` by describing the architectural responsibilities owned by the workspace subsystem.

---

# Architectural Role

Within the overall ROOST architecture, the workspace occupies the earliest stage of the analytical workflow.

Conceptually:

```text
Household
    ↓
Workspace
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
```

The workspace understands the current planning situation.

It does not generate evidence.

---

# Responsibilities

The workspace owns four primary responsibilities.

## Organization

The workspace organizes analytical content.

Typical workspace contents include:

* Household definitions
* Workspace configuration
* Results
* Reports
* Supporting documentation

A workspace answers:

> What analytical material exists for this planning context?

---

## Characterization

The workspace characterizes the current planning situation.

Characterization begins with inventory.

Inventory identifies resources available within the workspace.

Examples include:

* Household definitions
* Household Financial Profiles (HFPs)
* Previous results
* Reports
* Supporting files

Characterization then computes semantic observations describing the current planning situation.

These observations are called **Levers**.

---

## Discovery

The workspace determines which analytical workflows are currently applicable.

Rather than exposing every possible investigation, the workspace computes which transition families may be explored for the current planning situation.

Examples include:

* Spending transitions
* Retirement timing
* Social Security claiming
* Roth conversions

Discovery depends upon the computed lever values.

---

## Materialization

The workspace owns execution materialization.

Analytical definitions become execution artifacts through materialization.

Conceptually:

```text
Experiment
        ↓
Session
        ↓
Run
        ↓
Trial
```

Materialized artifacts preserve operational provenance and generated evidence.

---

# Workspaces

A workspace is the primary organizational unit within ROOST.

Workspaces are intended to be:

* Portable
* Reproducible
* Self-documenting
* Shareable
* Rebuildable

A workspace may be distributed as:

* A directory
* A Git repository
* An educational example
* A research artifact
* A published study

The workspace itself remains independent from any particular analytical methodology.

---

# Characterization

Characterization is the primary responsibility of the workspace subsystem.

Rather than requiring other subsystems to inspect files or household configuration directly, the workspace computes semantic observations describing the current analytical context.

Characterization answers questions such as:

* Is a valid household available?
* Have results been generated?
* Which planning capabilities exist?
* Which analytical workflows are applicable?

Characterization produces levers.

Other subsystems consume them.

---

# Levers

Levers are semantic observations describing the current planning situation.

Levers are computed.

They are never manually maintained.

Levers may be:

* Boolean
* Categorical
* Continuous

Examples include:

* Workspace initialized
* Household validated
* Current retirement status
* Social Security status
* Current spending
* Current asset allocation

Levers do not represent recommendations.

They describe the current state of the planning environment.

---

# Transition Discovery

Levers determine which transition families are applicable.

Conceptually:

```text
Current Household
        ↓
Characterization
        ↓
Levers
        ↓
Applicable Transition Families
```

For example:

* Social Security investigations require Social Security eligibility.

* Roth conversion investigations require tax-deferred assets.

* Housing transitions require home ownership.

The workspace determines applicability.

The study subsystem defines the transitions themselves.

---

# Inventory

Workspace inventory describes the resources currently available within a workspace.

Examples include:

* Household definitions
* HFP workbooks
* Results
* Reports
* Generated documentation

Inventory is descriptive rather than analytical.

Characterization builds upon inventory.

---

# Materialization

The workspace owns the realization of analytical execution.

Execution artifacts include:

* Sessions
* Runs
* Trials

Conceptually:

```text
Analytical Definition
        ↓
Materialization
        ↓
Execution Artifact
```

Materialization preserves provenance without modifying the analytical definitions from which execution originated.

---

# Generated Content

Generated content belongs to the workspace.

Examples include:

```text
results/

reports/

figures/

dashboards/
```

Generated artifacts represent evidence.

Whenever practical they should remain reproducible rather than authoritative.

The authoritative sources remain:

* Household definitions
* Workspace configuration
* Analytical definitions

Generated evidence should always be rebuildable.

---

# Minimal Workspace

The minimal workspace remains intentionally small.

```text
workspace/
├── workspace.toml
└── Makefile
```

Additional organization should emerge naturally as analytical needs increase.

Simple planning workflows should remain simple.

---

# Public Workflow

The workspace provides a consistent public interface for common analytical workflows.

Typical operations include:

```text
validate

inventory

characterize

build

run

results

reports
```

The implementation may evolve.

The conceptual workflow should remain stable.

---

# Relationship to Other Subsystems

The workspace cooperates closely with other architectural subsystems.

### Study

The study subsystem defines reusable analytical methodology.

The workspace determines when that methodology is applicable.

---

### Catalog

The catalog provides semantic identity and explainability.

The workspace computes observations consumed by the catalog.

---

### Display

The display subsystem presents workspace observations and generated evidence.

The workspace does not own presentation.

---

### Metrics

Metrics describe generated evidence.

The workspace owns execution context rather than analytical results.

---

# Architectural Invariants

The following concepts should remain stable.

## The workspace owns analytical context.

The workspace describes the current planning environment.

It does not define analytical methodology.

---

## Characterization precedes analysis.

The current planning situation should be understood before analytical workflows are selected.

---

## Levers characterize the planning situation.

Levers describe the current analytical context.

They determine applicability.

They do not represent recommendations.

---

## Discovery follows characterization.

Applicable transition families are determined from computed levers rather than direct inspection of household inputs.

---

## Materialization preserves provenance.

Execution artifacts preserve how evidence was generated without modifying the analytical definitions from which they originated.

---

## Generated evidence is reproducible.

Results, reports, dashboards, and other generated artifacts should remain rebuildable whenever practical.

---

## The workspace owns organization.

Analytical methodology belongs elsewhere.

Presentation belongs elsewhere.

Semantic identity belongs elsewhere.

The workspace owns the organization and characterization of the current analytical context.

---

# Long-Term Direction

The workspace is evolving toward the semantic entry point for retirement planning within ROOST.

Future capabilities are expected to include:

* Richer characterization
* Continuous and categorical levers
* Automatic transition discovery
* Adaptive analytical workflows
* Household readiness assessment
* Workspace diagnostics
* Evidence lifecycle management

The workspace should increasingly answer a single architectural question:

> **What is the current planning situation, and which analytical investigations are appropriate for it?**

Every subsequent stage of the ROOST workflow builds upon that characterization.
