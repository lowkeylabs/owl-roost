# Catalog Subsystem

The `catalog/` subsystem owns the semantic identity of information within ROOST.

The catalog defines what observations exist, what they mean, where they originate, and how they should be interpreted.

Every meaningful observation within ROOST should have exactly one semantic definition.

This document complements the project `README.md` and `ARCHITECTURE.md` by describing the architectural responsibilities owned by the catalog subsystem.

---

# Architectural Role

Within the ROOST architecture, the catalog provides the semantic foundation upon which every other subsystem depends.

Conceptually:

```text
Household

Workspace

Study

Metrics

Display

        ↓

Catalog

        ↓

Semantic Identity

        ↓

Consumers
```

The catalog defines meaning.

Other subsystems consume that meaning.

---

# Responsibilities

The catalog owns four primary responsibilities.

## Semantic Identity

The catalog defines what every observation means.

Examples include:

* Household inputs
* Derived values
* Workspace observations
* Metrics
* Aggregate values
* Synthetic observations

Every observation should have exactly one semantic definition.

---

## Ontology

The catalog classifies observations.

Ontology provides consistent semantic descriptions across the entire system.

Examples include:

* Ownership
* Semantic domain
* Value origin
* Projection kind
* Materialization level
* Analytic kind
* Node type

Ontology allows observations to be understood independently of their implementation.

---

## Explainability

The catalog owns explainability metadata.

Examples include:

* Descriptions
* Definitions
* Provenance
* Dependencies
* Lineage

Explainability should accompany every meaningful observation whenever practical.

---

## Semantic Resolution

The catalog provides semantic lookup.

Consumers request observations by meaning rather than implementation.

Consumers should not require knowledge of:

* Storage layout
* Package organization
* Filesystem location
* Internal implementation

The catalog resolves semantic identity into usable observations.

---

# Semantic Identity

Semantic identity is the primary responsibility of the catalog.

Every observation should answer questions such as:

* What is this?
* What does it represent?
* Where did it originate?
* How was it produced?
* How should it be interpreted?

Semantic identity should remain stable even if implementation changes.

---

# Canonical Definitions

Every meaningful observation should have one canonical definition.

That definition should remain authoritative throughout the system.

Other subsystems may:

* Compute observations
* Aggregate observations
* Display observations
* Compare observations

Only the catalog defines what those observations mean.

---

# Ontology

The catalog provides a shared ontology describing every registered observation.

Ontology supports consistent reasoning across all architectural subsystems.

Typical ontology dimensions include:

* Ownership
* Semantic domain
* Value origin
* Projection kind
* Analytic kind
* Materialization level
* Node type

Ontology allows analytical meaning to remain independent from execution.

---

# Explainability

Explainability is a first-class responsibility of the catalog.

Explainability should enable users to understand:

* What an observation represents
* Why it exists
* How it was computed
* Which information contributed to it
* Which assumptions were involved

Explainability should support:

* Individuals
* Advisors
* Researchers
* Educators
* LLMs

The catalog owns explainability.

Other subsystems communicate it.

---

# Semantic Resolution

Consumers should request semantic observations rather than implementation details.

Conceptually:

```text
Semantic Name
        ↓
Catalog
        ↓
Resolved Observation
```

Consumers should remain independent from:

* Files
* Tables
* Registry implementations
* Package organization

Semantic resolution promotes loose coupling throughout ROOST.

---

# Registration

The catalog follows the registration-based architecture used throughout ROOST.

Typical organization includes:

```text
bootstrap.py

registry.py

specs.py

fields/

metrics/

namespaces/
```

Registration creates the semantic model.

Registration should avoid duplication.

Every observation should be registered once.

---

# Relationship to Other Subsystems

The catalog provides semantic identity for the remainder of ROOST.

### Workspace

The workspace computes semantic observations.

The catalog defines their meaning.

---

### Study

The study subsystem references semantic observations when defining analytical methodology.

The catalog provides their identity.

---

### Metrics

Metrics generate analytical evidence.

The catalog defines what those metrics represent.

---

### Display

Display communicates semantic observations.

The catalog defines what is being communicated.

---

# Architectural Invariants

The following concepts should remain stable.

## Every observation has one semantic definition.

Meaning should be defined once.

Reuse should occur through reference rather than duplication.

---

## Semantic identity is independent of implementation.

Package organization, storage, and execution should not affect meaning.

---

## The catalog owns ontology.

Classification belongs to the catalog.

Other subsystems consume ontology.

---

## The catalog owns explainability.

Explainability metadata should remain attached to semantic definitions.

Presentation belongs elsewhere.

---

## Consumers depend upon semantic identity.

Subsystems should request meaning rather than implementation.

The catalog provides semantic resolution.

---

## Registration should remain canonical.

Every observation should be registered once.

Registration should become the authoritative source of semantic truth.

---

# Long-Term Direction

The catalog is evolving toward a complete semantic model of ROOST.

Future capabilities are expected to include:

* Richer ontology
* Enhanced provenance
* Expanded explainability
* Dependency graphs
* Semantic search
* Ontology-aware reasoning
* LLM-oriented semantic interfaces
* Automated documentation generation

Regardless of implementation, the catalog should continue to answer one architectural question:

> **What does this observation mean?**

Every other subsystem depends upon that answer.

The catalog therefore serves as the semantic backbone of ROOST, providing a single, authoritative understanding of every meaningful observation produced throughout the system.
