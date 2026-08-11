# Workspace Subsystem

The `workspace/` subsystem owns the **planning context** within ROOST.

A planning context describes the environment in which retirement planning is being performed. It provides filesystem context, workspace configuration when available, semantic characterization, planning intent, and the information needed by other subsystems to construct reproducible analytical investigations.

A planning context always exists.

An initialized workspace is an optional persisted planning artifact represented by:

```text
workspace.toml
```

The workspace subsystem explains **where planning is occurring, how that environment is configured, and what the planning situation means**.

It does not own canonical household projects, household discovery, analytical methodologies, execution, or presentation.

This document complements the project `README.md` and `ARCHITECTURE.md` by describing the architectural responsibilities and invariants of the workspace subsystem.

---

# Architectural Role

Within the overall ROOST architecture, the workspace subsystem provides the semantic planning context connecting filesystem state, workspace configuration, households, studies, and analytical execution.

Conceptually:

```text
Planning Directory
        │
        ▼
Planning Context
        │
        ├── Filesystem Inventory
        │
        ├── Workspace Configuration
        │
        └── Planning State
        │
        ▼
Characterization
        │
        ▼
Semantic Observations
        │
        ▼
Households / Studies / Execution
```

The workspace subsystem characterizes the environment.

Other subsystems consume that characterization.

---

# Planning Context

A **planning context** is the fundamental workspace-level abstraction.

Every filesystem directory may be treated as a planning context regardless of whether it contains an initialized workspace.

For example, ROOST may characterize:

```text
an empty directory

a directory containing planning artifacts

an initialized workspace

a directory containing child workspaces

a directory containing execution results

a mixed planning directory
```

The planning context therefore exists independently of `workspace.toml`.

At its simplest, a planning context contains identity such as:

```text
filesystem root
directory name
filesystem inventory
workspace status
```

Additional semantic observations are materialized from that context.

This separation allows commands such as workspace discovery and initialization to operate before a workspace exists.

---

# Initialized Workspaces

An **initialized workspace** is a planning context containing:

```text
workspace.toml
```

The minimal initialized workspace is intentionally small:

```text
workspace/
├── workspace.toml
└── Makefile
```

Additional organization emerges as planning requirements increase.

An initialized workspace adds persisted configuration and planning intent to the otherwise transient planning context.

The presence of `workspace.toml` therefore means:

> This planning context has an explicit persisted workspace definition.

It does not create the planning context itself.

---

# Workspace Configuration

Workspace configuration is represented by:

```text
workspace.toml
```

Configuration controls workspace-level policy such as:

```text
workspace documentation

planning context paths

household library search locations

workspace-wide execution overrides
```

The effective workspace definition is composed by the workspace loader.

Conceptually:

```text
Packaged workspace.toml
        +
Local workspace.toml
        │
        ▼
Effective Workspace Definition
```

The packaged template defines both:

```text
recognized configuration structure

default configuration values
```

The local `workspace.toml` selectively overrides those defaults.

Local configuration does not need to repeat the complete template.

---

# Configuration Ownership

The workspace subsystem owns:

```text
workspace configuration schema

workspace configuration defaults

loading local workspace configuration

validation of configuration keys

composition of defaults and overrides

workspace-level search policy
```

Configuration defaults belong in the packaged `workspace.toml` template.

They should not be duplicated as Python defaults in inventory definitions, semantic levers, or downstream subsystems.

This establishes a single authoritative source for workspace configuration defaults.

---

# Nested Configuration

Workspace configuration is hierarchical.

For example:

```toml
[context.paths]

cases = "."
results = "./results"
```

and:

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

Local configuration is recursively merged with the packaged template.

A nested override replaces the corresponding configured value without removing unrelated sibling defaults.

For example:

```toml
[context.paths]

results = "./custom-results"
```

changes the results path while preserving the configured cases path.

Unknown configuration keys are rejected from the effective definition and reported to the user.

---

# Household Library Search Policy

The workspace configuration defines the **ordered household library search policy** visible to the planning context.

The standard search order is:

```text
workspace
    ./library/households

user
    ~/.roost/library/households

builtin
    templates/library/households
```

Conceptually:

```text
workspace.toml
        │
        ▼
context.households
        │
        ▼
Household Bootstrap
        │
        ▼
HouseholdLibrarySpec
        │
        ▼
Household Discovery
```

The distinction in ownership is important.

The **workspace subsystem owns the configuration and search policy**.

The **household subsystem owns interpretation of that configuration, filesystem discovery, household manifests, HouseholdSpec construction, and household registration**.

The workspace subsystem should therefore not discover household projects or construct household registries.

---

# Filesystem Inventory

The workspace subsystem inventories the current planning context.

Inventory contains direct observations rather than interpretation.

Examples include:

```text
root path

directory name

files

directories

case files

Household Financial Profiles

workspace.toml presence

parent workspaces

child workspaces
```

Inventory answers:

> **What exists here?**

It does not answer:

> **What does it mean?**

That distinction belongs to characterization.

---

# Characterization

Characterization interprets filesystem inventory and other available planning information.

Examples include:

```text
directory kind

workspace initialization state

workspace initialization readiness

workspace creation readiness

valid planning artifacts

configured planning paths
```

Characterization answers questions such as:

```text
Is this an initialized workspace?

Is this an empty planning context?

Does this directory contain recognizable planning material?

May this directory be initialized as a workspace?

Are there parent or child workspaces?

Where are cases and results located?
```

Characterization produces semantic observations that may be registered in the workspace registry and exposed through the catalog.

---

# Semantic Levers

Workspace levers are computed semantic observations describing the planning context.

They are computed rather than persisted.

Examples include:

```text
context.workspace.directory_name

context.workspace.initialized

context.workspace.parent_count

context.workspace.child_count

context.workspace.directory_kind

context.paths.workspace

context.paths.cases

context.paths.results
```

Levers characterize the environment.

They do not represent recommendations.

They should describe stable semantic concepts rather than mirror arbitrary configuration structure.

---

# Configuration Is Not Inventory

Workspace configuration and workspace inventory are related but distinct.

For example:

```toml
[context.paths]

results = "./results"
```

is configuration.

The corresponding resolved semantic observation:

```text
context.paths.results
```

is derived state.

Likewise:

```toml
[[context.households]]
name = "workspace"
location = "./library/households"
```

is configuration.

The `HouseholdLibrarySpec` constructed from that configuration belongs to the household subsystem.

This distinction prevents configuration representation from leaking unnecessarily into semantic registries.

---

# Workspace Inventory

The workspace also materializes semantic observations describing the workspace itself.

These observations may include:

```text
workspace.name

workspace.overrides
```

Workspace inventory consumes the already composed effective workspace definition.

It does not define configuration defaults and does not perform configuration merging.

The flow is:

```text
Packaged Configuration
        +
Local Configuration
        │
        ▼
Workspace Loader
        │
        ▼
Effective Definition
        │
        ▼
Workspace Materialization
        │
        ▼
Semantic Workspace Observations
```

---

# Workspace Identity

Human-readable workspace documentation belongs in `workspace.toml`.

Examples include:

```toml
title = "2026 Retirement Planning"

description = """
Planning investigation for the
2026 planning cycle.
"""
```

Semantic workspace identity may additionally be computed from the planning context.

Filesystem identity and human-readable documentation should remain distinguishable.

A directory name is an observable filesystem fact.

A title is persisted workspace documentation.

They need not be identical.

---

# Workspace Overrides

Workspace configuration may contribute overrides that apply to analytical execution originating from that workspace.

For example:

```toml
[workspace]

overrides = [
]
```

Workspace overrides represent persisted planning intent.

They are distinct from:

```text
study overrides

experiment overrides

run-specific overrides
```

Those sources may eventually be combined when execution plans are realized.

The workspace subsystem owns the workspace contribution.

It does not own realization of the final execution configuration.

---

# Realized and Experimental Changes

ROOST distinguishes between changes that describe the current planning state and changes introduced for analytical experimentation.

**Realized changes** describe events that have already occurred.

**Experimental changes** describe hypothetical analytical alternatives.

Where practical, both should use compatible override semantics.

They differ primarily by provenance and purpose.

Conceptually:

```text
Canonical Household
        +
Realized Planning State
        │
        ▼
Current Planning State
        │
        +
Experimental Overrides
        │
        ▼
Analytical Run
```

Canonical household definitions remain unchanged.

---

# Discovery

The planning context provides semantic information that may be used to determine which analytical methodologies are applicable.

Conceptually:

```text
Planning Context
        │
        ▼
Characterization
        │
        ▼
Semantic Observations
        │
        ▼
Applicable Methodologies
```

The workspace subsystem provides characterization.

The study subsystem defines analytical methodologies.

The execution subsystem realizes analytical runs.

These responsibilities should remain separate.

---

# Generated Artifacts

A workspace may contain or reference generated artifacts such as:

```text
results

reports

figures

tables

published evidence packages
```

These artifacts are not authoritative workspace configuration.

They are generated consequences of analytical execution and presentation.

The workspace preserves enough planning context and configuration to make those artifacts reproducible whenever practical.

---

# Public Workflow

The workspace subsystem supports a workflow conceptually resembling:

```text
observe planning context

        ↓

load workspace configuration
if initialized

        ↓

compose effective definition

        ↓

inventory filesystem

        ↓

characterize planning context

        ↓

materialize semantic observations

        ↓

provide context to downstream subsystems
```

Downstream subsystems then perform household discovery, study selection, execution, display, and publishing as appropriate.

---

# Relationship to Other Subsystems

## Household

The household subsystem owns canonical Household Projects.

It owns:

```text
HouseholdLibrarySpec

HouseholdSpec

household manifest parsing

household filesystem discovery

household registry construction

household lookup
```

The workspace owns the configured household library **search policy**.

The household subsystem interprets and realizes that policy.

---

## Study

The study subsystem defines reusable analytical methodologies.

Workspace characterization may provide semantic information used to determine which methodologies are applicable.

The workspace does not define study methodologies.

---

## Execution

Workspace configuration and planning intent contribute to execution planning.

The execution subsystem realizes and executes analytical runs.

Execution artifacts do not become authoritative workspace state merely because they reside beneath a workspace.

---

## Catalog

The catalog provides semantic identity, metadata, and explainability.

Workspace inventory and semantic levers register stable observations with the catalog.

Raw dynamic configuration should not be duplicated indiscriminately as catalog observations.

---

## Display

The display subsystem presents planning contexts, workspaces, households, studies, runs, and analytical evidence.

The workspace subsystem does not own presentation.

---

## Package

The package subsystem assembles and publishes evidence derived from analytical execution.

Workspace configuration and context may contribute provenance to an evidence package.

The workspace does not own package rendering or publication.

---

# Architectural Invariants

The following invariants should remain stable.

## A planning context always exists.

A directory may be characterized without being an initialized workspace.

`workspace.toml` adds persisted workspace configuration; it does not create the underlying planning context.

---

## Workspace configuration has one source of defaults.

The packaged `workspace.toml` template defines canonical configuration defaults.

Python modules should not independently reproduce those defaults.

---

## Local workspace configuration selectively overrides canonical configuration.

The effective workspace definition is:

```text
canonical defaults
+
local overrides
```

Nested configuration is recursively composed.

Unknown configuration keys are not silently incorporated.

---

## Configuration and semantic observations are distinct.

`workspace.toml` describes configuration.

Workspace inventory and levers describe semantic observations derived from the effective planning context.

Configuration structure should not automatically become registry structure.

---

## The workspace owns household search policy, not household discovery.

`context.households` defines the ordered Household Libraries visible to the workspace.

The household subsystem resolves those libraries, discovers Household Projects, parses manifests, constructs HouseholdSpec objects, and populates the HouseholdRegistry.

---

## Household libraries are searched in configured order.

The normal search order is:

```text
workspace

user

builtin
```

Ordering is meaningful and should be preserved.

---

## Built-in resources are read-only.

Built-in Household Libraries are distributed with ROOST and should not be modified through household operations.

Workspace and user libraries may be writable according to their semantics.

---

## Characterization is independent of persistence.

Filesystem inventory and characterization operate on planning contexts whether or not `workspace.toml` exists.

Operations requiring workspace configuration must explicitly require an initialized workspace.

---

## Levers are computed.

Semantic observations are materialized from the current planning context.

They are not manually maintained as duplicated persistent state.

---

## Loaders compose configuration.

Workspace loaders own:

```text
loading canonical defaults

loading local configuration

validating configuration

recursive composition

construction of the effective definition
```

Materializers consume that definition.

They do not repeat configuration composition.

---

## Materializers produce semantic state.

Materializers transform loaded planning context into stable semantic observations.

They should not perform filesystem mutation or redefine configuration policy.

---

## Bootstrap assembles registries.

Bootstrap modules construct subsystem registries from the appropriate effective context.

For example, household bootstrap consumes configured Household Libraries and assembles the HouseholdRegistry.

Registry construction should not be hidden inside workspace configuration loading.

---

## Filesystem mutation belongs to operations.

Creation, initialization, rename, synchronization, and other filesystem mutations belong to workspace operations.

Loaders and materializers remain observational.

---

## Planning investigations are reproducible.

Analytical artifacts should be regenerable from authoritative planning inputs whenever practical.

Those inputs include:

```text
canonical households

realized planning state

workspace configuration

planning intent

study definitions

experimental configuration
```

Generated artifacts are evidence of execution rather than authoritative planning definitions.

---

# Long-Term Direction

The workspace subsystem is evolving toward the semantic entry point for retirement planning within ROOST.

Future capabilities may include:

```text
richer planning-context characterization

additional semantic levers

methodology applicability

workspace diagnostics

planning readiness assessment

multi-household investigations

longitudinal planning support

stronger provenance

improved reproducibility
```

Regardless of implementation details, the workspace subsystem should continue to answer:

> **What is the current planning context, how is it configured, and what semantic information does it provide to the rest of ROOST?**

The household subsystem can then answer:

> **Which canonical households are available in that context?**

The study subsystem can answer:

> **Which analytical methodologies are available and applicable?**

The execution subsystem can answer:

> **How are those methodologies realized and executed?**

Keeping those questions separate preserves the architectural boundaries on which ROOST depends.
