# Study Subsystem

The `study/` subsystem owns reusable analytical methodology within ROOST.

It defines **what analytical investigations are available** and **how evidence should be generated**.

The study subsystem contains reusable analytical definitions.

It does **not** characterize a household, execute investigations, or interpret evidence.

Those responsibilities belong elsewhere.

This document complements the project `README.md` and `ARCHITECTURE.md` by describing the architectural responsibilities owned by the study subsystem.

---

# Architectural Role

Within the ROOST architecture, the study subsystem occupies the methodology layer.

Conceptually:

```text
Workspace Characterization
            ↓
Applicable Studies
            ↓
Study
            ↓
Experiment
            ↓
Session
            ↓
Runs
            ↓
Evidence
```

The workspace determines which studies are applicable.

The study subsystem defines those studies and the experiments that generate evidence.

Execution begins with Sessions and belongs outside the study subsystem.

---

# Responsibilities

The study subsystem owns two primary concepts.

## Studies

A study organizes a coherent analytical investigation.

Examples include:

* Market Uncertainty
* Beginning-of-Year Spending
* Social Security Claiming
* Roth Conversion
* Retirement Timing

A study answers:

> What analytical topic should be investigated?

Studies organize related experimental methodologies.

Studies do not execute analyses.

---

## Experiments

Experiments define reusable evidence-generation methodologies.

An experiment specifies:

* applicability requirements
* fixed model overrides
* variable model overrides

Experiments define *how* evidence should be generated.

Examples include:

* Bootstrap Sequence of Returns
* Historical Average Returns
* Fixed Return Models
* Historical Replay
* Social Security Age Sweep
* Retirement Date Sweep

Experiments are reusable analytical definitions.

When materialized for a household, an experiment becomes a Session.

The Session expands variable overrides into one or more Runs.

Runs are the primary analytical objects compared by ROOST.

---

# Studies

Studies organize related analytical methodologies.

Conceptually:

```text
Study

    ├── Experiment

    ├── Experiment

    └── Experiment
```

Examples:

```text
Market Uncertainty

    Bootstrap Regimes

    Historical Returns

    Fixed Returns

    DCC-GARCH
```

or

```text
Beginning-of-Year Spending

    Spending Sweep

    Spending Robustness

    Spending Sensitivity
```

Studies provide organization.

They do not generate evidence.

---

# Experiments

Experiments define reproducible analytical methodology.

Conceptually:

```text
Experiment

    Fixed Overrides

    Variable Overrides

            ↓

        Session

            ↓

         Runs

            ↓

        Evidence
```

Experiments define methodology rather than execution.

Execution belongs to Sessions.

---

# Transitions

Although transitions are not currently represented as first-class objects within ROOST, they remain an important analytical concept.

A transition represents a candidate change from the current planning situation.

Examples include:

* Delay retirement one year
* Increase annual spending
* Delay Social Security
* Convert additional retirement assets
* Reduce portfolio risk

Experiments frequently evaluate one or more implicit transitions.

For example:

```text
Social Security Age Sweep

    Claim at 62

    Claim at 63

    ...

    Claim at 70
```

or

```text
Retirement Date Sweep

    Retire Today

    Delay One Year

    Delay Two Years
```

Today these transitions are incorporated directly into experimental methodology.

Should future analytical needs require reusable transition definitions, transitions may become first-class architectural objects.

---

# Evaluation Environments

Experiments often evaluate decisions under multiple external environments.

Examples include:

* Historical market regimes
* Bootstrap sampling
* DCC-GARCH simulations
* Fixed return assumptions
* Inflation models

Evaluation environments represent assumptions about the future rather than decisions made by the retiree.

Experiments combine analytical transitions with evaluation environments to generate evidence.

---

# Relationship to Execution

The study subsystem ends where execution begins.

Conceptually:

```text
Study
        ↓
Experiment
        ↓
Session
        ↓
Run
        ↓
Trial
```

The study subsystem owns:

* Studies
* Experiments

The execution subsystem owns:

* Sessions
* Runs
* Trials

A Session represents the realization of one Experiment for one household during one planning cycle.

---

# Relationship to Other Subsystems

## Workspace

The workspace characterizes the current planning situation.

It determines which studies and experiments are applicable.

The study subsystem defines analytical methodology.

---

## Catalog

The catalog provides the semantic identity of observations referenced by experiments.

The study subsystem consumes semantic definitions.

---

## Metrics

Experiments generate evidence.

Metrics define the observations comprising that evidence.

The study subsystem does not own analytical results.

---

## Display

Display communicates generated evidence.

The study subsystem defines methodology rather than presentation.

---

# Registration

The study subsystem follows the registration-based architecture used throughout ROOST.

```text
bootstrap.py

registry.py

specs.py

studies/

experiments/
```

Studies organize analytical investigations.

Experiments contribute reusable analytical methodologies.

Registration allows new studies and experiments to be introduced without modifying existing subsystem behavior.

---

# Architectural Invariants

The following concepts should remain stable.

## Studies organize methodology.

Studies define coherent analytical investigations.

They do not execute analyses.

---

## Experiments define methodology.

Experiments describe reusable evidence-generation strategies.

They do not interpret evidence.

---

## Execution remains separate.

Studies and Experiments describe analytical intent.

Sessions, Runs, and Trials describe realized execution.

---

## Applicability belongs to the workspace.

The workspace determines which studies are currently relevant.

The study subsystem defines what those studies mean.

---

# Long-Term Direction

The study subsystem is evolving toward a reusable library of retirement-planning methodology.

Future capabilities may include:

* richer experiment libraries
* automatic study selection
* adaptive experiment selection
* comparative investigations
* research-oriented methodologies
* educational analytical workflows

Regardless of future implementation, the architectural responsibility remains unchanged.

The study subsystem answers one question:

> **What analytical investigations are available, and how should evidence for those investigations be generated?**
