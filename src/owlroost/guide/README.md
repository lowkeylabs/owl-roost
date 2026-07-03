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
Guide Views
        │
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

It merely recommends them.

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

Guide supplies contextual assistance that supplements normal displays.

Guidance is computed from:

* the current planning context
* the current display level
* the selected display view
* the selected rows

The same planning context may therefore produce different guidance depending upon what the user is currently viewing.

---

## Explainability

Guide recommendations should always be explainable.

Users should be able to determine:

* why a recommendation appears
* why another recommendation does not
* which semantic observations contributed
* which applicability conditions succeeded or failed

Guide therefore follows the same explainability principles used throughout ROOST.

---

# Semantic Variables

Guide operates entirely from semantic variables.

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

Workflow guidance is registered declaratively.

Each guide definition typically describes:

* title
* description
* suggested command
* applicability requirements
* priority

Guide definitions contain workflow knowledge rather than presentation logic.

One guide definition may contribute to multiple guidance views.

---

# Applicability Evaluation

Recommendations become applicable when all applicability requirements evaluate to true.

Conceptually:

```text
Semantic Variables
        │
        ▼
Guide Definition
        │
        ▼
Requirement Evaluation
        │
        ▼
Applicable Guide
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

Guide produces semantic guidance.

Display determines how that guidance is rendered.

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

Display renders guidance.

Guide computes semantic guidance.

---

### Catalog

Catalog provides semantic identity.

Guide consumes semantic variables registered within the catalog.

---

# Architectural Invariants

The following concepts should remain stable.

## Guide computes semantic guidance.

Guide evaluates workflow definitions.

It never performs planning activities.

---

## Guide consumes semantic observations.

Guide never computes planning state directly.

Other subsystems own characterization.

Guide consumes those observations.

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

One guide definition may contribute to multiple guidance views.

Presentation should never be embedded within workflow definitions.

---

## Guidance should evolve naturally.

As new planning capabilities are added, Guide should recommend them automatically through new guide definitions rather than changes to existing workflow logic.

---

# Long-Term Direction

Guide is evolving toward ROOST's semantic workflow engine.

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
