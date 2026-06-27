# Display Subsystem

The `display/` subsystem owns the presentation of information within ROOST.

Display transforms semantic observations and analytical evidence into representations suitable for people.

The display subsystem determines **how** information is communicated.

It does not determine **what** information exists or **how** it is generated.

This document complements the project `README.md` and `ARCHITECTURE.md` by describing the architectural responsibilities owned by the display subsystem.

---

# Architectural Role

Within the ROOST architecture, the display subsystem occupies the final stage of the evidence-generation workflow.

Conceptually:

```text
Evidence
    ↓
Display
    ↓
Reports

Tables

Dashboards

Documentation

Visualizations
```

Display communicates evidence.

It does not generate evidence.

---

# Responsibilities

The display subsystem owns four primary responsibilities.

## Presentation

Display determines how information should be presented.

Examples include:

* Tables
* Reports
* Dashboards
* Web pages
* Documentation
* Interactive displays

Presentation should remain independent from evidence generation.

---

## Organization

Display organizes related information into meaningful views.

Examples include:

* Household summaries
* Balance sheets
* Spending summaries
* Transition comparisons
* Evidence summaries

Views organize information without changing its meaning.

---

## Formatting

Display owns presentation formatting.

Examples include:

* Labels
* Units
* Numeric formatting
* Ordering
* Grouping
* Visibility
* Layout

Formatting should improve readability without altering analytical content.

---

## Communication

Display communicates analytical evidence to people.

Typical consumers include:

* Individuals
* Advisors
* Researchers
* Educators
* LLMs
* Documentation systems

Communication should preserve analytical meaning while improving accessibility.

---

# Display Philosophy

Display separates presentation from analytical meaning.

The display subsystem should never redefine analytical concepts.

Instead it presents information owned by other architectural subsystems.

Conceptually:

```text
Catalog
        ↓
Semantic Meaning

Metrics
        ↓
Evidence

Display
        ↓
Presentation
```

Meaning remains unchanged.

Presentation may vary.

---

# Display Fields

Display fields describe how individual observations should appear.

Examples include:

* Human-readable labels
* Units
* Formatting rules
* Visibility
* Ordering
* Presentation profiles

Display fields describe presentation.

They do not own analytical meaning.

---

# Display Views

Views organize multiple display fields into reusable presentations.

Examples include:

* Household Summary
* Balance Sheet
* Spending
* Retirement Timing
* Social Security
* Transition Comparison
* Workspace Summary

Views define communication.

They do not generate evidence.

---

# Presentation Profiles

A single observation may appear differently in different contexts.

For example:

* Detailed reports
* Summary tables
* Pivot tables
* Dashboards
* Documentation
* Educational material

Presentation profiles allow the same analytical observation to be reused across many forms of communication without changing its underlying meaning.

---

# Explainability

Display supports explainability.

Explainability itself belongs to the semantic model.

The display subsystem communicates available explainability information.

Examples include:

* Descriptions
* Provenance
* Definitions
* Lineage
* Supporting rationale

Display should expose explainability rather than recreate it.

---

# Relationship to Other Subsystems

The display subsystem depends upon other architectural subsystems.

### Catalog

The catalog defines semantic identity.

Display presents that identity.

---

### Metrics

Metrics define analytical evidence.

Display communicates that evidence.

---

### Workspace

The workspace characterizes the current analytical context.

Display presents workspace observations.

---

### Study

The study subsystem defines analytical methodology.

Display communicates analytical intent and resulting evidence.

---

# Registration

The display subsystem follows the registration-based architecture used throughout ROOST.

Typical organization includes:

```text
bootstrap.py

registry.py

specs.py

fields/

views/

formatters/
```

Fields define presentation.

Views organize presentation.

Formatters render presentation.

Registration enables new presentation capabilities without modifying existing behavior.

---

# Architectural Invariants

The following concepts should remain stable.

## Display owns presentation.

Display determines how information is communicated.

It does not generate evidence.

---

## Display does not own semantics.

Analytical meaning belongs to the catalog.

Evidence belongs to metrics.

Display communicates both.

---

## Display does not alter evidence.

Formatting should never change analytical meaning.

Presentation should remain faithful to the underlying evidence.

---

## Presentation is reusable.

The same analytical observation should be usable in multiple presentation contexts without duplication.

---

## Explainability should remain visible.

Display should expose available explainability whenever practical.

Understanding evidence is as important as viewing it.

---

## Presentation remains independent.

Changes to presentation should not require changes to analytical methodology.

Analytical methodology should not depend upon presentation.

---

# Long-Term Direction

The display subsystem is evolving toward a flexible presentation layer capable of communicating evidence across many forms of media.

Future capabilities are expected to include:

* Richer dashboards
* Interactive exploration
* Adaptive layouts
* Personalized views
* Educational presentations
* LLM-oriented evidence summaries
* Publication-quality reporting

Regardless of presentation technology, the architectural responsibility remains unchanged.

The display subsystem should answer one question:

> **How should trustworthy analytical evidence be communicated clearly, consistently, and without altering its meaning?**
