# Study Subsystem

The `study/` subsystem owns reusable analytical methodology within ROOST.

A study defines **what should be investigated** and **how evidence should be generated**.

Studies organize related transition families, experiments, analytical methodology, and evidence-generation strategies.

The study subsystem does **not** characterize the current planning situation.

The workspace determines applicability.

The study subsystem defines the analytical investigations that may be performed.

This document complements the project `README.md` and `ARCHITECTURE.md` by describing the architectural responsibilities owned by the study subsystem.

---

# Architectural Role

Within the ROOST architecture, the study subsystem occupies the methodological stage of the evidence-generation workflow.

Conceptually:

```text
Characterization
        ↓
Applicable Transition Families
        ↓
Study
        ↓
Transitions
        ↓
Experiments
        ↓
Evidence
```

The workspace determines which transition families are applicable.

The study subsystem defines those transition families and the experiments used to evaluate them.

---

# Responsibilities

The study subsystem owns four primary responsibilities.

## Studies

A study organizes a coherent analytical investigation.

A study groups related planning concepts into a reusable analytical framework.

Examples include:

* Spending analysis
* Retirement timing
* Social Security
* Roth conversion
* Asset allocation
* Withdrawal strategies

A study defines analytical intent.

It does not generate evidence.

---

## Transition Families

Transition families organize related planning transitions.

Examples include:

* Retirement Timing
* Spending Level
* Social Security Claiming
* Roth Conversion
* Housing Decisions

A transition family defines a decision space.

The workspace determines whether that decision space is currently applicable.

---

## Transitions

A transition represents a meaningful change from the current planning situation.

Examples include:

* Delay retirement one year
* Increase annual spending
* Delay Social Security
* Convert additional retirement assets
* Reduce portfolio risk

Transitions represent candidate changes.

ROOST evaluates transitions.

ROOST does not recommend them.

Transition generation should be deterministic and reproducible.

---

## Experiments

Experiments define methodologies for generating evidence.

Experiments specify how one or more transitions should be evaluated.

Examples include:

* Parameter sweeps
* Comparative analysis
* Sensitivity studies
* Robustness evaluation
* Uncertainty analysis

Experiments describe methodology.

They do not interpret evidence.

---

# Studies

Studies provide reusable analytical organization.

Studies answer questions such as:

* Which transition families belong together?
* Which experiments should be available?
* How should investigations be organized?
* Which evidence packages should be produced?

Studies organize methodology rather than execution.

---

# Transition Families

Transition families organize related planning decisions.

Conceptually:

```text
Transition Family

        ↓

Transitions
```

Examples include:

```text
Spending

    Maintain

    Increase

    Reduce
```

or

```text
Retirement Timing

    Retire Now

    Delay One Year

    Delay Two Years
```

Transition families define analytical possibility.

They do not determine applicability.

---

# Transitions

Transitions describe candidate changes from the current planning situation.

Conceptually:

```text
Current State

        ↓

Transition

        ↓

Candidate Future State
```

Transitions should remain:

* Deterministic
* Explainable
* Reproducible

Transitions are analytical definitions rather than execution artifacts.

---

# Evaluation Environments

Experiments evaluate transitions under one or more evaluation environments.

Evaluation environments describe assumptions about the future rather than decisions made by the retiree.

Examples include:

* Historical market returns
* Bootstrap market models
* Inflation assumptions
* Longevity assumptions
* Future tax assumptions

Evaluation environments remain independent from transition families.

A single transition may be evaluated under many environments.

---

# Experiments

Experiments define reproducible evidence-generation methodologies.

Conceptually:

```text
Transitions

        +

Evaluation Environments

        ↓

Evidence
```

Experiments may define:

* Parameter selection
* Sweep generation
* Sampling methodology
* Aggregation strategy
* Comparison methodology

Experiments define analytical methodology rather than execution.

Execution is materialized by the workspace.

---

# Execution Planning

Execution planning transforms analytical definitions into executable investigations.

Conceptually:

```text
Study
        ↓
Experiment
        ↓
Execution Plan
```

Execution plans describe:

* Which transitions will be evaluated
* Which environments will be used
* Which evidence will be generated

Execution plans remain reusable analytical definitions.

Sessions, runs, and trials belong to execution materialization within the workspace subsystem.

---

# Relationship to Other Subsystems

The study subsystem cooperates closely with other architectural subsystems.

### Workspace

The workspace characterizes the current planning situation.

It determines which transition families are applicable.

The study subsystem defines those transition families.

---

### Catalog

The catalog defines the semantic identity of observations referenced by studies and experiments.

The study subsystem consumes semantic definitions.

---

### Metrics

Experiments generate evidence.

Metrics define that evidence.

The study subsystem does not own analytical results.

---

### Display

Display communicates generated evidence.

The study subsystem defines methodology rather than presentation.

---

# Registration

The study subsystem follows the registration-based architecture used throughout ROOST.

Typical organization includes:

```text
bootstrap.py

registry.py

specs.py

transition_families/

experiments/

studies/
```

Studies organize methodology.

Transition families organize related transitions.

Experiments contribute evidence-generation strategies.

Registration allows new analytical methodologies to be introduced without modifying existing subsystem behavior.

---

# Architectural Invariants

The following concepts should remain stable.

## Studies own analytical methodology.

Studies define reusable analytical organization.

They do not generate evidence.

---

## Transition families organize decision spaces.

Transition families define related planning transitions.

Applicability belongs to the workspace.

---

## Transitions represent candidate change.

Transitions describe meaningful changes from the current planning situation.

ROOST evaluates transitions.

ROOST does not recommend them.

---

## Evaluation environments remain independent.

Future assumptions remain orthogonal to retiree decisions.

Experiments combine transitions with environments.

---

## Experiments generate evidence.

Experiments define deterministic methodologies for producing evidence.

Interpretation belongs elsewhere.

---

## Execution remains separate from methodology.

Studies, transition families, transitions, experiments, and execution plans describe analytical intent.

Sessions, runs, and trials describe realized execution.

---

# Long-Term Direction

The study subsystem is evolving toward a reusable library of retirement planning methodology.

Future capabilities are expected to include:

* Richer transition families
* Automatic transition generation
* Adaptive experiment selection
* Multi-stage investigations
* Comparative study composition
* Environment-aware experimentation
* Research-oriented methodologies
* Educational analytical workflows

Regardless of future implementation, the architectural responsibility remains unchanged.

The study subsystem should answer one question:

> **What analytical transitions should be evaluated, and how should evidence for those transitions be generated?**

The workspace determines when a study is applicable.

The study subsystem defines what that study means.
