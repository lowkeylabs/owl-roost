# Workspace Subsystem

The `workspace/` subsystem owns planning investigations within ROOST.

A workspace organizes one or more canonical households into a reproducible planning investigation.

The workspace preserves planning intent, characterizes the planning situation, identifies applicable analytical methodologies, and assembles execution plans.

The workspace explains **why** an analytical investigation exists.

It does not define canonical households, execute analytical investigations, or own execution artifacts.

This document complements the project `README.md` and `ARCHITECTURE.md` by describing the architectural responsibilities owned by the workspace subsystem.

---

# Architectural Role

Within the overall ROOST architecture, the workspace bridges canonical household definitions and analytical execution.

Conceptually:

```text
Canonical Household(s)
        │
        ▼
Planning Investigation
        │
        ▼
Characterization
        │
        ▼
Levers
        │
        ▼
Applicable Methodologies
        │
        ▼
Execution Plan
        │
        ▼
Execution Subsystem
```

The workspace understands the current planning situation.

It determines which investigations should be performed.

It does not execute those investigations.

---

# Responsibilities

The workspace owns four primary responsibilities.

## Planning Investigation

The workspace organizes one or more canonical households into a coherent planning investigation.

A planning investigation combines:

* Canonical household definitions
* Realized planning state
* Planning intent
* Workspace configuration
* Supporting documentation

The workspace preserves the context explaining why the investigation exists.

That context should remain understandable long after analytical execution has completed.

---

## Characterization

The workspace characterizes the current planning situation.

Characterization begins with inventory.

Inventory identifies the resources available within the planning investigation.

Examples include:

* Canonical households
* Realized planning state
* Household Financial Profiles
* Previous execution artifacts
* Reports
* Supporting documentation

Characterization computes semantic observations describing the planning situation.

These observations are called **Levers**.

Characterization is performed whenever the workspace subsystem observes a planning context.

A persisted `workspace.toml` is not required.

The same inventory, characterization, and lever-computation pipeline may be applied to:

* an initialized workspace
* a directory containing canonical households
* a directory containing execution artifacts
* an empty directory
* a household library

The persisted workspace stores planning intent and documentation.

Inventory, characterization, and levers are computed observations rather than stored state.

---

## Discovery

The workspace determines which analytical methodologies are applicable.

Rather than exposing every possible investigation, the workspace identifies those appropriate for the current planning situation.

Examples include:

* Spending investigations
* Retirement timing
* Social Security claiming
* Roth conversions
* Asset allocation studies

Discovery depends upon computed lever values.

The workspace determines applicability.

The study subsystem defines the analytical methodologies themselves.

---

## Execution Planning

The workspace assembles execution plans.

Execution plans combine:

* One or more canonical households
* Planning intent
* Analytical methodologies
* Experimental overrides

into reproducible analytical investigations.

The execution subsystem realizes and executes those plans.

The workspace preserves the planning context from which those execution plans were derived.

---

# Workspaces

A workspace is the primary planning unit within ROOST.

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

A workspace represents one planning investigation involving one or more canonical households.

As households evolve over time, new workspaces naturally capture new planning investigations while preserving previous planning context.

---

# Realized Planning State

A workspace preserves the current realized planning state of every participating household.

Rather than modifying canonical household definitions, the workspace records changes that have actually occurred since those households were originally defined.

Conceptually:

```text
Canonical Household
        +
Realized Changes
        │
        ▼
Current Planning State
```

The resulting planning state becomes the basis for characterization, methodology selection, and execution planning.

Canonical households remain unchanged.

---

# Characterization

Characterization computes semantic observations describing the planning investigation.

Characterization answers questions such as:

* Which households participate?
* What planning changes have been realized?
* Which planning capabilities exist?
* Which analytical methodologies are applicable?
* Which previous investigations already exist?

Characterization produces levers.

Other architectural subsystems consume them.

---

# Levers

Levers are semantic observations describing the planning investigation.

Levers are computed.

They are never maintained manually.

Levers are transient semantic observations.

They are derived from the current planning context each time characterization is performed rather than persisted within a workspace.

This allows identical analytical workflows to operate on both persistent workspaces and transient directory contexts.

Levers may be:

* Boolean
* Categorical
* Continuous

Examples include:

* Social Security eligibility
* Retirement status
* Tax-deferred assets available
* Home ownership
* Pension availability

Levers describe the planning environment.

They do not represent recommendations.

---

# Applicable Methodologies

Computed levers determine which analytical methodologies are appropriate.

Conceptually:

```text
Planning Investigation
        │
        ▼
Characterization
        │
        ▼
Levers
        │
        ▼
Applicable Methodologies
```

For example:

* Social Security investigations require eligible participants.
* Roth conversion investigations require tax-deferred assets.
* Housing investigations require home ownership.

The workspace determines applicability.

The study subsystem defines the methodologies.

---

# Realized and Experimental Changes

The workspace distinguishes between two classes of change.

**Realized changes** describe events that have already occurred.

**Experimental changes** describe hypothetical future scenarios explored analytically.

Both use the same override semantics.

They differ only by provenance.

This shared representation allows historical household evolution and future analytical exploration to use a consistent analytical model.

---

# Inventory

Workspace inventory describes the resources available within a planning investigation.

Examples include:

* Canonical households
* Realized planning state
* Household Financial Profiles
* Workspace configuration
* Previous execution artifacts
* Documentation
* Supporting files

Inventory is descriptive rather than analytical.

Characterization builds upon inventory.

---

# Generated Artifacts

A workspace may reference generated execution artifacts, reports, figures, dashboards, and documentation.

These artifacts are owned by the execution and display subsystems.

The workspace preserves the planning context required to regenerate them.

Generated artifacts should remain reproducible rather than authoritative.

The authoritative planning sources remain:

* Canonical households
* Realized planning state
* Planning intent
* Workspace configuration

---

# Minimal Workspace

The minimal workspace remains intentionally small.

```text
workspace/
├── workspace.toml
└── Makefile
```

Additional organization should emerge naturally as analytical requirements increase.

Simple planning investigations should remain simple.

---

# Public Workflow

The workspace provides a consistent public interface for planning investigations.

Typical operations include:

```text
inventory

characterize

discover

assemble execution plans

document planning intent
```

The execution subsystem realizes and executes those plans.

The display subsystem communicates the resulting evidence.

---

# Relationship to Other Subsystems

The workspace cooperates closely with other architectural subsystems.

### Household

The household subsystem owns canonical household definitions.

The workspace organizes one or more canonical households into a planning investigation.

---

### Study

The study subsystem defines reusable analytical methodologies.

The workspace determines which methodologies are applicable.

---

### Execution

The workspace assembles execution plans.

The execution subsystem realizes and executes those plans while preserving execution artifacts.

---

### Catalog

The catalog provides semantic identity and explainability.

The workspace computes observations consumed by the catalog.

---

### Display

The display subsystem communicates planning investigations and execution artifacts.

The workspace does not own presentation.

---

### Metrics

Metrics describe analytical evidence generated through execution.

The workspace owns planning context rather than analytical evidence.

---

# Architectural Invariants

The following concepts should remain stable.

## The workspace owns planning investigations.

Canonical households belong to the household subsystem.

Execution plans belong to the execution subsystem.

The workspace preserves the planning context connecting them.

---

## Characterization precedes analysis.

The planning situation should be understood before analytical methodologies are selected.

---

## Characterization is independent of persistence.

Inventory, characterization, and lever computation are services provided by the workspace subsystem.

They may be applied to either transient directory contexts or persisted workspaces.

Persisted workspaces record planning intent rather than computed observations.

---

## Levers characterize planning investigations.

Levers describe the planning context.

They determine applicability.

They do not represent recommendations.

---

## Discovery follows characterization.

Applicable analytical methodologies are determined from computed levers rather than direct inspection of household definitions.

---

## Realized and experimental changes share a common representation.

Historical household evolution and future analytical exploration should use the same override semantics whenever practical.

They differ only by provenance.

---

## Execution plans preserve planning intent.

The workspace assembles execution plans.

The execution subsystem realizes and executes them.

Planning intent remains independent of execution artifacts.

---

## Planning investigations are reproducible.

Execution artifacts should be regenerable from canonical households, planning intent, realized planning state, and workspace configuration whenever practical.

---

## The workspace owns planning context.

Canonical households belong elsewhere.

Analytical methodologies belong elsewhere.

Execution belongs elsewhere.

Presentation belongs elsewhere.

Analytical evidence belongs elsewhere.

The workspace owns the organization, characterization, and documentation of planning investigations.

---

# Long-Term Direction

The workspace is evolving toward the semantic entry point for retirement planning within ROOST.

Future capabilities are expected to include:

* Richer characterization
* Additional semantic levers
* Automatic methodology discovery
* Adaptive planning workflows
* Household readiness assessment
* Multi-household investigations
* Longitudinal planning support
* Workspace diagnostics
* Improved planning reproducibility

Regardless of implementation, the workspace should continue to answer one architectural question:

> **How should one or more canonical households be organized into a reproducible planning investigation, and which analytical investigations should be performed?**

Every subsequent stage of the ROOST workflow builds upon that planning investigation.
