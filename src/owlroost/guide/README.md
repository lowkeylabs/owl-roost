# Guide Subsystem

The `guide/` subsystem owns user guidance within ROOST.

Guide helps users understand what they can do next.

Rather than embedding workflow logic throughout the codebase, Guide evaluates the current planning context and produces explainable recommendations describing applicable commands, workflows, studies, and planning activities.

Guide answers:

> **Given the current planning situation, what should happen next?**

This document complements the project `README.md`, `ARCHITECTURE.md`, and the workspace subsystem documentation by describing the architectural responsibility owned by the guide subsystem.

---

# Architectural Role

Guide sits above the planning subsystems.

Conceptually:

```text
Planning Context
        │
        ▼
Characterization
        │
        ▼
Semantic Variables
        │
        ▼
Guide
        │
        ▼
Suggested Activities
```

Guide does not characterize the planning context.

Guide consumes semantic observations produced by other subsystems.

---

# Responsibilities

Guide owns four primary responsibilities.

## Guidance

Guide recommends appropriate next activities.

Examples include:

* initialize a workspace
* import a household
* create a study
* execute an experiment
* review results
* compare runs
* generate documentation

Guide never performs these activities.

It merely recommends them.

---

## Applicability

Every recommendation has explicit applicability requirements.

Examples include:

* one or more valid cases exist
* a workspace has been initialized
* execution results are available
* multiple runs exist for comparison

Guide evaluates these requirements using semantic variables rather than inspecting files directly.

---

## Explainability

Guide recommendations should always be explainable.

Users should be able to determine:

* why a recommendation appears
* why another recommendation does not
* which semantic observations contributed
* which applicability conditions succeeded or failed

Guide therefore supports the same explainability principles used throughout ROOST.

---

## Workflow Discovery

Guide introduces users to ROOST.

Rather than requiring users to memorize command sequences, Guide discovers appropriate workflows from the current planning situation.

For example:

```text
Empty directory

↓

Initialize Workspace
Import Case
Open Example
```

Later:

```text
Initialized workspace

↓

Build Cases
Create Study
Generate Reports
```

Still later:

```text
Completed execution

↓

Review Results
Compare Runs
Generate Documentation
```

The current planning situation determines the available guidance.

---

# Semantic Variables

Guide operates entirely from semantic variables.

Guide does not inspect the filesystem directly.

Guide does not parse household files.

Guide does not evaluate execution artifacts.

Instead, Guide consumes observations already computed by other subsystems.

Examples include:

* context.valid_case_count
* context.workspace_initialized
* study.experiment_count
* results.run_count

The guide subsystem therefore remains independent of implementation details.

---

# Guide Definitions

Guide recommendations are registered.

A guide definition typically describes:

* title
* description
* suggested command
* applicability expression
* optional documentation
* optional priority

Guide definitions are reusable.

Different interfaces may present them differently while sharing identical applicability logic.

---

# Applicability Expressions

Recommendations become applicable when their applicability expression evaluates to true.

Conceptually:

```text
Semantic Variables
        │
        ▼
Applicability Expression
        │
        ▼
Applicable Recommendation
```

Expressions may compare:

* booleans
* counts
* strings
* categorical values
* future semantic observations

Guide remains independent of how those observations were computed.

---

# User Interfaces

Guide does not own presentation.

Different interfaces may consume Guide differently.

Examples include:

* CLI welcome screens
* Context summaries
* Interactive tutorials
* Documentation
* Future graphical interfaces
* Future LLM assistants

Every interface should consume the same underlying guide definitions.

---

# Relationship to Other Subsystems

Guide coordinates existing architectural concepts.

It does not replace them.

### Workspace

Workspace characterizes the planning investigation.

Guide recommends planning activities based upon that characterization.

---

### Study

Study defines analytical methodologies.

Guide recommends applicable studies.

---

### Execution

Execution realizes analytical plans.

Guide recommends appropriate execution workflows.

---

### Display

Display renders guidance.

Guide supplies recommendations.

---

### Catalog

Catalog provides semantic identity.

Guide consumes semantic variables registered within the catalog.

---

# Architectural Invariants

The following concepts should remain stable.

## Guide owns recommendations.

Guide recommends activities.

It does not perform them.

---

## Guide consumes semantic observations.

Guide never computes planning state directly.

Other subsystems own characterization.

Guide consumes those observations.

---

## Applicability should be explainable.

Every recommendation should explain why it is applicable.

Recommendations that are not applicable should also be explainable.

---

## Guide should remain interface-independent.

CLI, documentation, graphical interfaces, and future LLM assistants should consume identical guide definitions.

Presentation belongs elsewhere.

---

## Guidance should evolve naturally.

As new planning capabilities are added, Guide should recommend them automatically through new guide definitions rather than changes to existing workflow logic.

---

# Long-Term Direction

Guide is evolving toward the semantic workflow engine for ROOST.

Future capabilities are expected to include:

* adaptive planning workflows
* study recommendations
* context-sensitive help
* execution guidance
* comparison guidance
* documentation guidance
* educational tutorials
* explainable applicability trees

Regardless of implementation, the guide subsystem should continue to answer one architectural question:

> **Given the current planning situation, what should the user do next?**

Every recommendation should be explainable, deterministic, and derived from the semantic observations already produced by the rest of the ROOST architecture.
