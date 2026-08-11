# Workspace Design Notes

This document captures the current architectural direction of the Workspace subsystem.

Unlike `README.md`, which describes the enduring responsibilities and public role of the Workspace subsystem, this document records the current design model and the principles guiding its continued implementation.

Implementation details may evolve.

The architectural invariants described here should change much more slowly.

---

# Design Direction

The Workspace subsystem is the semantic integration point for a retirement planning investigation.

It connects:

* the filesystem
* workspace configuration
* household libraries
* canonical household definitions
* study methodology
* execution artifacts
* planning activities
* published evidence

into a coherent semantic representation of the current planning environment.

The subsystem distinguishes two closely related concepts:

```text
Context
    │
    └── optionally contains
            │
            ▼
        Workspace
```

This distinction is fundamental to the architecture.

---

# Context

A Context is the planning environment rooted at a filesystem location.

A Context always exists.

It does not require an initialized Workspace.

Conceptually:

```text
Directory
    │
    ▼
Context
```

A Context describes facts that ROOST can determine about the current planning environment.

Examples include:

* filesystem root
* workspace initialization state
* workspace directory name
* effective paths
* available household libraries
* other resources visible from the current location

Context observations use the canonical namespace:

```text
context.*
```

Examples include:

```text
context.workspace.initialized
context.workspace.directory_name

context.paths.workspace
context.paths.cases
context.paths.results

context.household.libraries
```

The Context therefore answers:

> **What planning environment currently exists?**

The top-level command:

```text
roost .
```

operates on this semantic level.

---

# Workspace

A Workspace is an initialized planning investigation within a Context.

A Workspace exists when the Context contains a valid:

```text
workspace.toml
```

Conceptually:

```text
Directory
    │
    ▼
Context
    │
    ├── uninitialized
    │
    └── initialized
            │
            ▼
        Workspace
```

Workspace observations use the canonical namespace:

```text
workspace.*
```

Examples include:

```text
workspace.name
workspace.overrides
```

The Workspace therefore answers:

> **What persisted planning investigation has been initialized in this Context?**

The command:

```text
roost workspace
```

operates on this semantic level.

---

# Context and Workspace Are Not Parallel Concepts

Context and Workspace should not be treated as two unrelated semantic models.

A Workspace exists within a Context.

The Context establishes the planning environment.

The Workspace adds persisted configuration describing the initialized planning investigation.

This relationship should remain explicit throughout the implementation.

Conceptually:

```text
Context
│
├── filesystem environment
├── path resolution
├── available resources
├── household libraries
│
└── workspace state
        │
        ├── not initialized
        │
        └── initialized
                │
                └── Workspace
```

This distinction allows ROOST to characterize a directory before a Workspace has been initialized.

---

# Workspace Configuration

Workspace configuration is represented by:

```text
workspace.toml
```

The canonical packaged `workspace.toml` template defines:

* recognized configuration
* default configuration
* configuration structure

A local `workspace.toml` selectively overrides those defaults.

Conceptually:

```text
Packaged workspace.toml
        +
Local workspace.toml
        │
        ▼
Effective Workspace Definition
```

The Workspace loader owns this composition.

The resulting effective definition is stored in:

```text
row["_workspace"]["definition"]
```

The effective definition is configuration.

It is not itself the semantic observation model.

---

# Configuration Versus Semantic Observations

Workspace configuration and semantic observations intentionally remain separate concepts.

For example, configuration may contain:

```toml
[context.paths]

cases = "."
results = "./results"
```

These values participate in the materialization of semantic observations such as:

```text
context.paths.cases
context.paths.results
```

Similarly:

```toml
[workspace]

overrides = []
```

may contribute to:

```text
workspace.overrides
```

The configuration file therefore provides inputs to semantic materialization.

It does not define the semantic ontology.

---

# Dynamic Configuration

Dynamic Workspace configuration belongs in `workspace.toml`.

It should not be duplicated in the Workspace Registry.

The Workspace Registry should remain intentionally small and stable.

`WorkspaceSpec` exists only for canonical semantic observations that require registration with the catalog and display infrastructure.

The registry should not attempt to model every configurable value in `workspace.toml`.

This produces an important architectural separation:

```text
workspace.toml
    │
    │ dynamic configuration
    ▼
Workspace Loader
    │
    ▼
Effective Definition
    │
    ▼
Semantic Materialization
    │
    ▼
Canonical Observations
```

The Workspace Registry describes the final semantic observations.

The Workspace configuration describes how the current Workspace should behave.

---

# Materialized Context

The principal semantic representation used by ROOST is the materialized row.

Conceptually:

```python
row = {
    "_path": ...,
    "_meta": ...,
    "_context": ...,
    "_workspace": ...,
}
```

Materialization adds canonical observations to this representation.

The resulting row may contain observations from multiple semantic domains:

```text
context.*
workspace.*
household.*
study.*
experiment.*
run.*
...
```

depending on the level being materialized.

This materialized representation is the semantic API consumed by downstream subsystems.

---

# No Separate Planning Context Object

The Workspace subsystem does not require a second semantic object representing a "Planning Context."

The materialized Context already provides that representation.

Introducing another hierarchy such as:

```text
HouseholdPlanningContext
WorkspacePlanningContext
```

would create a parallel semantic model containing information already available through materialized observations.

That duplication should be avoided.

Instead:

```text
Filesystem
    +
Configuration
        │
        ▼
     Loaders
        │
        ▼
   Context Row
        │
        ▼
  Materializers
        │
        ▼
Materialized Context
```

The Materialized Context becomes the common semantic input to downstream consumers.

---

# Household Libraries

Household Library search policy belongs to the Workspace Context.

The effective Workspace configuration determines which Household Libraries are visible and their search order.

For example:

```toml
[[context.households]]
name = "workspace"
location = "./library/households"

[[context.households]]
name = "user"
location = "~/.roost/library/households"

[[context.households]]
name = "builtin"
location = "library/households"
```

These declarations establish the effective Household Library search path.

Conceptually:

```text
Workspace Configuration
        │
        ▼
Context Household Libraries
        │
        ▼
Household Bootstrap
        │
        ▼
HouseholdLibrarySpec
        │
        ▼
Household Discovery
        │
        ▼
Household Registry
```

Workspace owns the search policy.

The Household subsystem interprets that policy and performs household discovery.

This preserves the boundary:

```text
Workspace
    decides where to search

Household
    decides how to discover households
```

---

# Search Order

Household Library ordering is significant.

The normal search order is:

```text
1. workspace
   ./library/households

2. user
   ~/.roost/library/households

3. builtin
   packaged library/households
```

The Workspace Context owns this ordering through its effective configuration.

The Household subsystem should not independently recreate or hard-code this search policy.

---

# Relationship to Households

The Workspace does not own Household Projects.

It owns the Context in which Household Projects are discovered.

Conceptually:

```text
Context
    │
    └── household library configuration
            │
            ▼
      Household Libraries
            │
            ▼
      Household Registry
            │
            ▼
       HouseholdSpec
```

The Household subsystem owns:

* `HouseholdLibrarySpec`
* `HouseholdSpec`
* manifest loading
* project discovery
* household registration

The Workspace subsystem owns:

* which libraries are visible
* their configured locations
* their search order

---

# Relationship to Studies

Studies describe analytical methodology.

The Workspace provides the planning environment in which those studies are realized.

Study configuration and materialization may therefore consume information from the materialized Context, but the Workspace should not duplicate Study semantics.

Conceptually:

```text
Materialized Context
        +
Study Definitions
        │
        ▼
Study Realization
        │
        ▼
Experiments
        │
        ▼
Runs
```

The Workspace provides context.

The Study subsystem owns methodology.

---

# Relationship to Activities

Activities consume the materialized Context.

They should not independently inspect the filesystem or reconstruct Workspace configuration.

The distinction is:

```text
Context:
    What planning environment exists?

Workspace:
    What planning investigation is initialized?

Activity:
    What work remains to accomplish a planning goal?
```

Activities may therefore depend upon observations from:

```text
context.*
workspace.*
household.*
study.*
run.*
```

without owning the computation of those observations.

---

# Relationship to Evidence Packages

Published evidence packages consume the same materialized semantic state used by the rest of ROOST.

There should not be a special intermediate Workspace planning object created solely for publication.

Conceptually:

```text
Materialized Context
        +
Materialized Runs
        +
Study Definitions
        │
        ▼
Evidence Package Builder
        │
        ▼
Evidence Package
        │
        ▼
Publisher
```

The evidence package builder selects and organizes semantic information according to the publication narrative.

It does not create a second Workspace semantic model.

---

# Explainability

Explainability remains a fundamental architectural invariant.

User-visible semantic values should be traceable to their sources.

Depending upon the observation, those sources may include:

* filesystem state
* packaged configuration defaults
* local `workspace.toml`
* household manifests
* registered ontology specifications
* study definitions
* execution results

The semantic materialization pipeline should make these relationships inspectable rather than hiding them inside higher-level synthesized objects.

---

# Loaders

Workspace loaders own filesystem and configuration loading.

Their responsibilities include:

```text
* Context row construction
* Workspace discovery
* packaged workspace.toml loading
* local workspace.toml loading
* configuration validation
* recursive configuration composition
* effective Workspace definition construction
```

They do not own:

```text
* semantic display
* analytical execution
* Household Project discovery
* Study realization
* evidence interpretation
```

---

# Materializers

Workspace materializers convert loaded state into canonical semantic observations.

Conceptually:

```text
Loaded Context
        +
Workspace Registry
        │
        ▼
Materialized Context
```

Materializers should consume existing configuration and filesystem state.

They should not redefine configuration defaults.

Configuration defaults belong exclusively to the packaged `workspace.toml` template.

---

# Registry

The Workspace Registry exists to register stable semantic observations.

It should remain deliberately small.

The registry owns:

```text
* canonical observation registration
* observation lookup
* observation enumeration
```

It does not own:

```text
* workspace configuration
* configuration defaults
* filesystem discovery
* path search policy
* local configuration overrides
```

This separation prevents configuration structure from becoming unnecessarily encoded into Python ontology metadata.

---

# Top-Down Development

Workspace development should continue from the semantic interface downward.

The useful question is:

> **What does ROOST need to know about the current Context or Workspace?**

If the answer represents a reusable semantic fact required by display, resolution, activities, execution, or publication, it may justify a canonical observation.

If the value is simply configurable behavior, it should generally remain configuration in `workspace.toml`.

This distinction helps prevent uncontrolled growth of the Workspace Registry.

---

# Architectural Flow

The overall Workspace architecture is:

```text
Filesystem
    │
    ├───────────────┐
    │               │
    ▼               ▼
Packaged         Local
workspace.toml   workspace.toml
    │               │
    └───────┬───────┘
            │
            ▼
      Workspace Loader
            │
            ▼
     Effective Definition
            │
            +
      Filesystem Context
            │
            ▼
       Context Row
            │
            ▼
       Materializers
            │
            ▼
    Materialized Context
            │
    ┌───────┼─────────┬───────────┐
    │       │         │           │
    ▼       ▼         ▼           ▼
 Display  Household  Activity   Studies
            │                     │
            ▼                     ▼
         Registry               Runs
                                  │
                                  ▼
                           Evidence Package
```

This materialized Context is the common semantic foundation rather than an intermediate object owned by any one downstream subsystem.

---

# Architectural Invariants

The following principles should guide future implementation.

* A Context always exists.
* A Workspace is an initialized planning investigation within a Context.
* `roost .` operates at the Context level.
* `roost workspace` operates at the Workspace level.
* Context observations use the `context.*` namespace.
* Workspace observations use the `workspace.*` namespace.
* `workspace.toml` is the authoritative dynamic Workspace configuration mechanism.
* The packaged `workspace.toml` defines recognized configuration and configuration defaults.
* Local `workspace.toml` files selectively override packaged defaults.
* Workspace configuration and Workspace semantic observations are distinct concepts.
* Configuration defaults should not be duplicated in Python registry metadata.
* The Workspace Registry should remain small and stable.
* The Workspace Registry contains canonical semantic observations, not arbitrary configuration fields.
* The effective Workspace definition is configuration input to semantic materialization.
* The materialized Context is the primary semantic representation consumed by downstream subsystems.
* A separate `WorkspacePlanningContext` semantic layer is unnecessary.
* Household Library search policy belongs to the Workspace Context.
* Household discovery belongs to the Household subsystem.
* Study methodology belongs to the Study subsystem.
* Activities consume semantic observations rather than reconstructing Workspace state.
* Evidence packages consume materialized semantic state rather than introducing another Workspace semantic model.
* Semantic values should remain explainable through their underlying configuration, filesystem state, specifications, or analytical results.
* New Workspace observations should be introduced only when they provide reusable semantic value beyond the underlying configuration.
