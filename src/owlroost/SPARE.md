

----------------- MOVE SOMEWHERE ELSE ---------------------------







---

# Canonical Operational Structure

ROOST distinguishes between:

* Operational execution structure
* Scientific interpretation structure

The canonical operational provenance hierarchy is:

```text
Case → Session → Run → Trial
```

This hierarchy defines:

* Filesystem organization
* Runtime provenance
* Recovery and continuation state
* Execution metadata
* Trial execution outputs
* Aggregated statistical results

All operational discovery, cleanup, reporting, and execution management are rooted in this hierarchy.

Scientific interpretation operates as a logical overlay on top of this operational structure.


---

# Structural Run Identity

ROOST distinguishes between:

* Structural run identity
* Session provenance
* Observed runtime behavior

Two runs may be considered structurally equivalent when they share:

* Decision variables
* Sampling variables
* Resolved execution configuration

while differing only in:

* Session provenance
* Execution timestamps
* Runtime observations
* Execution durations
* Throughput metrics

This distinction supports workflows such as:

* Operational deduplication
* Structural comparison
* Merge compatibility analysis
* Reproducible experiment organization
* Runtime performance analysis

Filesystem paths preserve immutable execution provenance, while structural comparison operates over resolved run configuration.

---

# Run Materialization and Execution

ROOST distinguishes between:

* Declarative configuration intent
* Resolved executable runtime configuration
* Observed runtime outcomes

Conceptually:

```text
Case Configuration
    ↓
Decision / Sampling Expansion
    ↓
Runtime Resolution
    ↓
Materialized Run Configuration
    ↓
Trial Execution
    ↓
Metrics and Aggregation
```

Examples of runtime resolution include:

* Solver auto-selection
* Worker auto-selection
* Thread allocation
* Runtime execution mode selection

The persisted `run.toml` file therefore represents:

```text
a frozen executable run contract
```

rather than merely a partially specified execution template.

A fully materialized run configuration supports:

* Reproducibility
* Stable structural comparison
* Deterministic replay behavior
* Operational provenance integrity
* Consistent purge and cleanup semantics
* Stable experiment organization

---

# Sessions

A **session** represents a specific execution event in which ROOST generates and/or evaluates runs for a case.

Conceptually:

```text
Case × Session → Runs
```

Sessions are operational rather than scientific.

They organize:

* Generated outputs
* Logs and metadata
* Runtime provenance
* Execution history
* Recovery and continuation state
* Incremental execution work

A session answers the question:

> *“What execution work was performed during this event?”*

Sessions provide:

* Immutable execution provenance
* Timestamp-oriented organization of outputs
* Incremental extension of larger experiments
* Separation of execution management from scientific interpretation
* Repeatable and reproducible execution history

For example, a worker-scaling experiment might be executed across multiple sessions:

* Session A: `workers_per_run=2..5`
* Session B: `workers_per_run=6..10`

Scientifically, these sessions may belong to the same experiment even though they were executed separately.

Sessions are associated with individual cases and execution events, while experiments may span multiple sessions and multiple cases.

This distinction allows ROOST to separate:

* **Scientific organization** (*experiments*)
  from
* **Execution and storage organization** (*sessions*)

while preserving a stable hierarchy of runs and trials.

---

# Execution Provenance

Execution provenance refers to the complete operational context in which runs and trials were generated.

Examples include:

* Runtime configuration
* Solver selection
* Parallelism configuration
* Thread allocation
* Sampling strategy
* Session organization
* Execution timestamps
* Recovery and continuation state
* Execution environment details

ROOST treats provenance as operational metadata distinct from scientific interpretation.

Filesystem paths serve as the canonical provenance identifiers for generated execution artifacts.


---

# Filesystem vs Scientific Structure

ROOST intentionally separates:

* Operational filesystem organization
  from
* Scientific experiment organization

Filesystem hierarchy reflects operational execution provenance:

```text
Case → Session → Run → Trial
```

Scientific organization is logical and overlay-based:

```text
Experiment → Related Runs
```

Experiments may span:

* Sessions
* Dates
* Execution environments
* Multiple cases/households

Experiments are therefore not tied directly to filesystem structure.

---

# Scientific and Operational Architecture

ROOST distinguishes between four major entity types:

| Entity     | Primary Role                               |
| ---------- | ------------------------------------------ |
| Trial      | Primitive stochastic observation           |
| Run        | Statistical policy evaluation              |
| Session    | Execution provenance container             |
| Experiment | Scientific organization and interpretation |

These entities are intentionally asymmetric.

Trials and runs contain numerical observations and statistical evidence.

Sessions and experiments primarily organize, contextualize, and interpret those results.


## Sessions are operational rather than scientific

Sessions preserve execution provenance, filesystem organization, runtime metadata, and execution history.

Sessions SHOULD NOT become primary scientific result entities.

## Run configurations are fully materialized before execution

Persisted run configurations SHOULD represent resolved executable runtime contracts rather than partially specified execution templates.

Runtime auto-resolution SHOULD occur before execution begins.

## Filesystem paths are canonical provenance identifiers

Filesystem paths preserve immutable operational provenance.

Transient operational IDs SHOULD remain convenience handles rather than canonical scientific identifiers.

# Relationship to Sessions

Studies and sessions serve fundamentally different purposes.

| Concept | Primary Role                             |
| ------- | ---------------------------------------- |
| Session | Operational execution provenance         |
| Study   | Scientific and analytical interpretation |

Sessions preserve:

* Execution history
* Runtime provenance
* Recovery and continuation state
* Materialized execution outputs

Studies organize:

* Analytical intent
* Scientifically related runs
* Comparative methodologies
* Aggregated interpretation

A single study may span:

* Multiple sessions
* Multiple dates
* Multiple execution environments
* Multiple cases/households

while a single session may contribute evidence to multiple studies.

Studies therefore operate as logical analytical overlays on top of the canonical operational hierarchy:

```text
Case → Session → Run → Trial
```

without altering filesystem provenance structure.

## Operational IDs and Selection Handles

ROOST may assign transient operational IDs to sessions, runs, and trials for:

* Interactive selection
* CLI workflows
* Filtering and display
* Operational management
* Cleanup and maintenance workflows

These IDs are:

* Ephemeral
* Context-dependent
* Operational rather than scientific
* Intended for CLI convenience

Filesystem paths remain the canonical provenance identifiers.

Experiments and persistent scientific overlays SHOULD reference canonical paths or structurally equivalent run definitions rather than transient operational IDs.
