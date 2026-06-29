# Workspace Subsystem

The `workspace/` subsystem owns the current realized planning state within ROOST.

A workspace represents a self-contained retirement planning environment containing the information required to realize the current state of a household, characterize that planning situation, discover applicable investigations, organize analytical artifacts, and materialize evidence.

The workspace does **not** define the household.

The workspace realizes the household at a particular point in time.

The workspace does **not** define analytical methodology.

The workspace provides the context in which analytical methodology is applied.

This document complements the project `README.md` and `ARCHITECTURE.md` by describing the architectural responsibilities owned by the workspace subsystem.

---

# Architectural Role

Within the overall ROOST architecture, the workspace realizes the current planning state of a household.

Conceptually:

```text
Household Definition
        ↓
Realized Overrides
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

## Realization

The workspace realizes the current planning state of a household.

A workspace combines:

* A canonical household definition
* Realized changes since the household was originally defined
* Workspace configuration

Realized changes represent events that have actually occurred.

Examples include:

* Updated account balances
* Spending changes
* Household Financial Profile updates
* Claimed Social Security
* New pensions
* Major purchases
* Other realized transitions

The resulting planning state becomes the starting point for subsequent analytical investigations.

---

## Characterization

The workspace characterizes the current planning situation.

Characterization begins with inventory.

Inventory identifies the resources available within the realized planning environment.

Examples include:

* Household definition
* Realized overrides
* Household Financial Profile
* Previous results
* Reports
* Supporting files

Characterization computes semantic observations describing the current planning situation.

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

Execution begins from the realized planning state represented by the workspace.

Experimental overrides describe hypothetical future transitions.

Materialized artifacts preserve operational provenance and generated evidence.

---

# Workspaces

A workspace is the primary operational unit within ROOST.

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

A workspace represents one planning review of one household.

Subsequent reviews naturally produce new workspaces representing later realized planning states.

---

# Realized Planning State

The realized planning state is the primary responsibility of the workspace subsystem.

Rather than modifying the canonical household definition, the workspace realizes the household by applying the accumulated changes that have actually occurred since the household was originally defined.

Conceptually:

```text
Household Definition
        +
Realized Overrides
        ↓
Current Planning State
```

The resulting planning state becomes the basis for characterization, transition discovery, experimentation, and evidence generation.

---

# Characterization

Characterization computes semantic observations describing the realized planning state.

Characterization answers questions such as:

* Is a valid household available?
* What changes have been realized?
* Have results previously been generated?
* Which planning capabilities currently exist?
* Which analytical workflows are applicable?

Characterization produces levers.

Other subsystems consume them.

---

# Levers

Levers are semantic observations describing the realized planning situation.

Levers are computed.

They are never manually maintained.

Levers may be:

* Boolean
* Categorical
* Continuous

Examples include:

* Household validated
* Current retirement status
* Social Security status
* Current spending
* Current asset allocation

Levers do not represent recommendations.

They describe the current planning environment.

---

# Transition Discovery

Levers determine which transition families are applicable.

Conceptually:

```text
Current Planning State
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

# Realized and Experimental Transitions

The workspace distinguishes between two classes of transitions.

**Realized transitions** describe events that have already occurred.

**Experimental transitions** describe hypothetical future changes explored through analytical execution.

Both are represented using the same override semantics.

They differ only in provenance.

This common representation allows historical household evolution and future scenario exploration to share a consistent analytical model.

---

# Inventory

Workspace inventory describes the resources currently available within a workspace.

Examples include:

* Household definitions
* Realized overrides
* Household Financial Profiles
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
Current Planning State
        +
Experimental Overrides
        ↓
Execution Artifact
```

Materialization preserves provenance without modifying the realized planning state from which execution originated.

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

* Household definition
* Realized overrides
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

### Household

The household subsystem defines the enduring planning subject.

The workspace realizes its current planning state.

---

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

## The workspace owns realized planning state.

The household defines the planning subject.

The workspace realizes its current state.

---

## Characterization precedes analysis.

The current planning situation should be understood before analytical workflows are selected.

---

## Levers characterize the current planning state.

Levers describe the realized analytical context.

They determine applicability.

They do not represent recommendations.

---

## Discovery follows characterization.

Applicable transition families are determined from computed levers rather than direct inspection of household inputs.

---

## Realized and experimental transitions share a common representation.

Historical household evolution and future analytical exploration should use the same override semantics whenever practical.

They differ by provenance rather than representation.

---

## Materialization preserves provenance.

Execution artifacts preserve how evidence was generated without modifying the realized planning state from which execution originated.

---

## Generated evidence is reproducible.

Results, reports, dashboards, and other generated artifacts should remain rebuildable whenever practical.

---

## The workspace owns current analytical context.

Household definition belongs elsewhere.

Analytical methodology belongs elsewhere.

Presentation belongs elsewhere.

Semantic identity belongs elsewhere.

The workspace owns realization, characterization, and organization of the current planning environment.

---

# Long-Term Direction

The workspace is evolving toward the semantic entry point for ongoing retirement planning within ROOST.

Future capabilities are expected to include:

* Richer characterization
* Continuous and categorical levers
* Automatic transition discovery
* Adaptive analytical workflows
* Household readiness assessment
* Longitudinal review support
* Workspace diagnostics
* Evidence lifecycle management

The workspace should increasingly answer a single architectural question:

> **What is the household's current realized planning state, and which analytical investigations are appropriate today?**

Every subsequent stage of the ROOST workflow builds upon that characterization.
