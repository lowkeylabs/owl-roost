# Guide Subsystem

The `guide/` subsystem owns semantic user guidance within ROOST.

Guide helps users understand what they can do next.

Rather than embedding workflow logic throughout the codebase, Guide evaluates the current planning context and produces semantic guidance describing applicable commands, workflows, studies, and planning activities.

Guide answers one architectural question:

> **Given the current planning situation, what should the user do next?**

This document complements the project `README.md`, `ARCHITECTURE.md`, and the workspace subsystem documentation by describing the architectural responsibility owned by the guide subsystem.

---

# Architectural Role

Guide evaluates fully materialized planning contexts.

Guide produces both semantic guidance values and semantic workflow objects.

Semantic values summarize applicable workflow recommendations.

Semantic objects expose rich workflow metadata—including descriptions, commands, applicability requirements, and future extensible properties—which may be consumed directly by the Display subsystem through semantic object resolution.


Conceptually:

```text
Planning Context
        │
        ▼
Materialization
        │
        ▼
Semantic Row
        │
        ▼
Guide Evaluation
        │
        ▼
Guide Materialization
      ┌──────┴────────┐
      ▼               ▼
Semantic Namespace  Guide Trees
      └──────┬────────┘
             ▼
          Display
```

Guide does not characterize the planning context.

Guide consumes semantic observations already produced by other subsystems.

Display owns presentation.

---

# Responsibilities

Guide owns four primary responsibilities.

## Guidance

Guide recommends appropriate next activities.

Examples include:

* initialize a workspace
* review planning cases
* build execution plans
* execute pending runs
* compare results
* generate reports
* review studies

Guide never performs these activities.

Instead, it produces semantic workflow knowledge describing recommended activities.

Presentation and execution remain responsibilities of other subsystems.

---

## Evaluation

Every guide has explicit applicability requirements.

Examples include:

* one or more valid cases exist
* a workspace has been initialized
* execution plans exist
* unrealized runs remain
* multiple results exist for comparison

Guide evaluates these requirements entirely from semantic observations.

Guide never inspects the filesystem directly.

---

## Assistance

Guide supplies contextual assistance by materializing semantic guidance that supplements normal displays.

Guidance is computed from:

* the current planning context
* the current display level
* the selected display view
* the selected rows

The same planning context may therefore produce different guidance depending upon what the user is currently viewing.

---

## Explainability

Guide recommendations should always be explainable.

Guide explanations are themselves semantic.

Workflow descriptions, commands, applicability conditions, and evaluation results are exposed as semantic object properties rather than embedded presentation logic.

This allows explanations to be generated dynamically without requiring separate documentation registrations for every workflow property.

Users should be able to determine:

* why a recommendation appears
* why another recommendation does not
* which semantic observations contributed
* which applicability conditions succeeded or failed

Guide therefore follows the same explainability principles used throughout ROOST.

---

# Semantic Observations

Guide operates entirely from semantic observations.

Most observations are represented as semantic variables.

Guide itself additionally materializes semantic workflow objects that describe workflow knowledge independently of presentation.

Guide does not inspect files directly.

Guide does not parse household definitions.

Guide does not evaluate execution artifacts.

Instead, Guide consumes observations already computed by other subsystems.

Examples include:

* context.valid_case_count
* context.workspace_initialized
* study.study_count
* execution.plan_count
* results.result_count

Guide therefore remains independent of implementation details.

---

# Guide Definitions

Guide definitions contain workflow knowledge rather than presentation logic.

One guide definition may simultaneously contribute to:

* semantic namespace values
* semantic object properties
* multiple guide trees
* multiple display views

Guide definitions become semantic objects during materialization.

These objects expose workflow metadata such as:

* title
* description
* command
* category
* priority
* requirements

Display resolves these properties dynamically through the semantic object resolver.

---

# Semantic Namespace

Guide materializes a semantic namespace alongside its evaluation results.

The namespace contains both semantic values and semantic workflow objects.

Semantic values represent workflow recommendations directly.

For example:

```text
guide.workspace.initialize
```

may resolve to:

```text
roost workspace --init
```

The namespace also retains the underlying semantic workflow objects used to resolve richer workflow metadata.

For example:

```text
guide.workspace.initialize.command
guide.workspace.initialize.description
guide.workspace.initialize.priority
guide.workspace.initialize.category
```

all resolve dynamically from the same underlying `GuideSpec` object.

Conceptually:

```text
Guide Evaluation
        │
        ▼
Guide Namespace
      ┌──────┴────────┐
      ▼               ▼
Semantic Values   Semantic Objects
```

The semantic namespace is presentation-independent.

It contains no display formatting and no rendering logic.

Instead, it serves as the semantic interface between the Guide subsystem and the Display subsystem.

Display resolves workflow properties dynamically without requiring individual catalog registrations for every workflow attribute.

Future semantic object subsystems are expected to follow the same architectural pattern.

---

# Applicability Evaluation

Recommendations become applicable when all applicability requirements evaluate to true.

Conceptually:

```text
Semantic Observations
        │
        ▼
Guide Definitions
        │
        ▼
Requirement Evaluation
        │
        ▼
Guide Evaluation
        │
        ▼
Semantic Guidance
```

Requirements may compare:

* booleans
* counts
* strings
* categorical values
* future semantic observations

Guide remains independent of how those observations were produced.

---

# Guidance Views

Guide materializes multiple semantic guidance trees.

Each tree materializes one aspect of workflow knowledge for consumption by the Display subsystem.

Display determines how those trees are rendered.

Current and planned guidance views include:

| Guidance View | Purpose | Audience |
|---------------|---------|----------|
| `suggestions` | Recommended next actions. | Users |
| `details` | Expanded explanations for suggested actions. | Users |
| `workflow` | Display current workflow progress and readiness. | Users |
| `coverage` | Reveal planning situations that currently lack guidance. | Developers |
| `reasoning` | Show applicability evaluation for every guide definition. | Developers |
| `variables` | Display semantic variables consumed during guide evaluation. | Developers |
| `diagnostics` | Validate guide definitions and detect authoring problems. | Developers |

Not every interface must expose every guidance view.

---

# Semantic Object Resolution

Guide materializes semantic workflow objects alongside ordinary semantic values.

Workflow objects are stored within the Guide semantic namespace and resolved dynamically by the Display subsystem.

For example:

    guide.workspace.initialize.command

resolves to the command property of the corresponding GuideSpec object.

This mechanism allows workflow metadata to evolve naturally without requiring individual catalog registrations for every property exposed by Guide.

Display is intentionally unaware of GuideSpec.

It resolves semantic object properties generically by traversing semantic namespaces and object registries embedded within the materialized row.

Future semantic object subsystems are expected to follow the same architectural pattern.
---

# Rendering

Guide does not render output.

Guide produces semantic guidance.

Display renders that guidance using ordinary display views.

Guidance supplements the user's requested view rather than replacing it.

For example:

```text
roost cases
```

renders the requested case summary.

While:

```text
roost cases --assist
```

renders:

```text
Case Summary

Suggested Next Actions
```
Guide tree nodes reference semantic object properties directly.

For example:

    guide.workspace.initialize.command

or

    guide.workspace.initialize.description

Display resolves these properties dynamically at render time without requiring individual catalog registrations.

Future interfaces may render different guidance views without modifying guide definitions.

---

# Relationship to Other Subsystems

Guide coordinates existing architectural concepts.

It does not replace them.

### Workspace

Workspace characterizes the planning investigation.

Guide recommends planning activities based upon that characterization.

---

### Study

Study characterizes analytical methodologies.

Guide recommends appropriate studies and workflows.

---

### Execution

Execution realizes analytical plans.

Guide recommends appropriate execution activities.

---

### Display

Display renders semantic guidance.

Guide computes semantic workflow knowledge.

Display resolves semantic values and semantic object properties supplied by Guide.

---

### Catalog

Catalog provides semantic identity.

Guide consumes semantic observations produced throughout ROOST. Catalog provides the semantic vocabulary used to define many of those observations.

---

# Architectural Invariants

The following concepts should remain stable.

---

## Guide computes semantic guidance.

Guide evaluates workflow definitions.

It never performs planning activities.

---

## Guide owns workflow knowledge.

Workflow definitions are represented as semantic objects.

Descriptions, commands, applicability rules, and future workflow metadata should remain properties of those semantic objects rather than becoming embedded within presentation code.

---

## Guide consumes semantic observations.

Guide consumes semantic observations produced by other subsystems.

Guide never characterizes planning state itself.

Guide contributes new semantic workflow objects describing workflow knowledge.

---

## Guidance is contextual.

Guidance depends upon:

* planning context
* display level
* current view
* selected rows

Different views of the same planning context may produce different guidance.

---

## Guide is presentation-independent.

Guide never renders terminal output.

Display owns presentation.

Guide produces semantic guidance that may be rendered by:

* CLI
* documentation
* notebooks
* dashboards
* graphical interfaces
* future LLM assistants

Semantic workflow objects may be consumed by:

* Display
* documentation
* developer tooling
* notebooks
* dashboards
* future LLM assistants

without modification to Guide itself.

---

## Guidance is additive.

Guidance supplements the user's requested view.

It never replaces the primary display.

---

## Applicability should remain explainable.

Every recommendation should explain why it is applicable.

Recommendations that are not applicable should also be explainable.

---

## Guide definitions should remain reusable.

One semantic guide definition may contribute simultaneously to:

* semantic variables
* semantic object properties
* multiple guidance trees
* future workflow interfaces

Presentation should never be embedded within workflow definitions.

---

## Guidance should evolve naturally.

As new planning capabilities are added, Guide should recommend them automatically through new guide definitions rather than changes to existing workflow logic.

---

# Long-Term Direction

Guide is evolving toward ROOST's semantic workflow knowledge subsystem.

Guide increasingly serves as the authoritative semantic repository of workflow knowledge.

Future capabilities are expected to include:

* adaptive workflow coaching
* study recommendations
* execution planning
* comparison recommendations
* documentation guidance
* educational tutorials
* developer diagnostics
* explainable workflow reasoning

Regardless of implementation, Guide should continue to answer one architectural question:

> **Given the current planning situation, what should the user do next?**

Every recommendation should be deterministic, explainable, and derived entirely from the semantic observations already produced by the rest of the ROOST architecture.
