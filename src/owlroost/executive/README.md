# Execution Subsystem

The `execution/` subsystem owns the lifecycle of execution plans within ROOST.

Execution plans transform canonical households together with planning intent into reproducible analytical investigations.

The subsystem realizes execution plans, executes those plans, and maintains the execution artifacts that document every analytical investigation.

This document complements the project `README.md` and `ARCHITECTURE.md` by describing the architectural responsibilities owned by the execution subsystem.

---

# Architectural Role

Within the overall ROOST architecture, the execution subsystem bridges planning and evidence generation.

Conceptually:

```text
Canonical Household(s)
        +
Planning Decisions
        +
Execution Policy
        │
        ▼
Execution Plan
        │
        ▼
Sessions
        │
        ▼
Runs
        │
        ▼
Trials
        │
        ▼
Execution Artifacts
        │
        ▼
Analytical Evidence
```

Execution plans describe exactly what analytical work will be performed.

Executing those plans produces analytical evidence while preserving complete execution provenance.

---

# Responsibilities

The execution subsystem owns:

* execution plan realization
* configuration composition
* override application
* sweep expansion
* execution topology
* session creation
* run creation
* trial creation
* trial scheduling
* trial execution
* stochastic seed generation
* execution provenance
* execution artifact maintenance
* execution artifact promotion
* execution artifact deletion
* execution artifact cleanup

The execution subsystem owns the complete lifecycle of execution plans and the execution artifacts that realize those plans.

---

# Architectural Boundaries

The execution subsystem does not own:

* canonical household definitions
* household libraries
* planning investigations
* household characterization
* transition discovery
* experiment selection
* analytical metrics
* comparison
* reporting
* presentation

Those responsibilities belong to other architectural subsystems.

---

# Relationship to the Household Subsystem

The household subsystem owns canonical household definitions.

Execution consumes canonical households but never modifies them.

Before execution begins, the required household state is snapshotted into the execution plan to ensure complete reproducibility.

Execution plans remain reproducible even if the originating household library subsequently changes.

---

# Relationship to the Workspace Subsystem

The workspace subsystem organizes planning investigations.

A workspace may:

* organize one or more households
* characterize planning situations
* identify applicable planning levers
* discover feasible transitions
* assemble execution plans

The execution subsystem realizes those plans into executable analytical artifacts.

Execution plans may also be created directly from canonical households without using a workspace.

The execution subsystem therefore remains completely independent of the workspace subsystem.

---

# Execution Artifacts

Execution artifacts are organized beneath the `results/` directory.

A typical execution hierarchy is:

```text
results/
    household/
        session/
            run/
                trial/
```

Each execution artifact contains sufficient information to reproduce the analytical investigation independently of the originating workspace or household library.

The `results/` directory is therefore an implementation of the execution subsystem rather than an independent architectural subsystem.

---

# Reproducibility

Execution establishes the reproducibility boundary of an analytical investigation.

Execution plans preserve:

* canonical household snapshots
* realized configuration
* planning overrides
* stochastic seeds
* runtime configuration
* execution topology
* execution provenance

Once an execution plan has been realized, future execution depends only upon the execution artifacts stored within the execution hierarchy.

Neither the originating workspace nor the household library is required to rerun the investigation.

---

# Current Implementation

The current implementation uses Hydra to compose configuration, apply overrides, and realize execution plans.

Hydra is an implementation technology rather than an architectural concept.

The architectural responsibility of this subsystem remains the realization, execution, and management of execution plans regardless of future implementation choices.

---

# Future Directions

Future revisions may support:

* distributed execution
* cloud execution backends
* adaptive scheduling
* incremental execution
* execution validation
* execution repair
* execution migration
* execution caching
* execution checkpointing

Regardless of implementation, this subsystem should continue to answer one architectural question:

> **How are planning decisions transformed into reproducible analytical investigations?**
