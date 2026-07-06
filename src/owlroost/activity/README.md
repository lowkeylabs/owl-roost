# Activity Subsystem

The `activity/` subsystem owns ROOST's semantic retirement planning workflow.

Activities describe *what* retirement planning work should be performed rather than *how* it is executed.

An activity represents a durable planning milestone such as initializing a workspace, creating a household, generating planning evidence, or performing an annual retirement review.

Activity answers one architectural question:

> **Given the current planning context, which planning activities exist, what is their current state, and which should be performed next?**

---

# Responsibilities

The Activity subsystem owns:

- declarative planning activity definitions
- activity evaluation
- workflow organization
- recommendation generation
- semantic activity materialization
- activity explainability

Activity does **not** execute planning commands.

Execution remains the responsibility of the appropriate subsystem.

---

# Activity Model

Planning activities are declared using `ActivitySpec`.

Each activity describes:

- identity
- category
- frequency
- requirements
- prerequisite activities
- suggested commands
- required scenario families

Activities are declarative.

They contain no execution logic.

---

# Evaluation

The Activity engine evaluates every registered activity against the current planning context.

Evaluation produces one `ActivityResult` describing:

- readiness state
- recommendation state
- requirement evaluation

Current readiness states include:

- READY
- WAITING
- BLOCKED
- COMPLETE
- NEEDS_REVIEW
- NOT_APPLICABLE

Recommendations determine how activities are presented:

- NEXT
- UPCOMING
- DEFERRED
- HIDDEN

Recommendation is derived from evaluation and is independent of activity definition.

---

# Materialization

The subsystem materializes both semantic objects and display trees.

Semantic objects expose activity metadata such as:

- description
- requirements
- suggested commands
- category
- frequency

Display views provide multiple perspectives over the same evaluation, including:

- next
- workflow
- status
- details
- reasoning
- variables
- diagnostics

---

# Relationship to Other Subsystems

Activity consumes semantic observations produced elsewhere in ROOST.

Typical inputs include workspace, household, execution, study, and result context.

Display owns rendering.

Activity owns workflow knowledge.

---

# Architectural Invariants

The Activity subsystem should remain:

- declarative
- deterministic
- explainable
- presentation independent
- reusable
- extensible

Activities describe retirement planning practice rather than implementation details.

As ROOST evolves, new planning capabilities should be introduced by registering additional activities rather than embedding workflow logic throughout the codebase.
