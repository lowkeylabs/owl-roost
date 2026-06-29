# Household Subsystem Design Notes

This document records the evolving design of the `household/` subsystem.

Unlike `README.md`, this document is intentionally exploratory.

It captures design rationale, future directions, open questions, and implementation ideas that may evolve over time.

The architectural responsibilities described by `README.md` should remain relatively stable.

This document is expected to change frequently as the subsystem matures.

---

# Design Philosophy

The household subsystem should become the canonical entry point for retirement planning within ROOST.

Its primary responsibilities are to:

* define households
* construct households
* organize household assets
* support education
* support testing
* support reproducible research

Whenever practical, a household should exist as a reusable planning asset rather than a collection of unrelated files.

---

# Household Projects

The current direction is to organize households as **Household Projects**.

Conceptually:

```text
Household Library
        ↓
Household Project
        ↓
Artifacts
```

A household project represents one canonical planning subject together with the artifacts used to understand, construct, document, validate, and export that household.

This approach replaces distinctions such as:

* synthetic household
* imported household
* tutorial household

with a single project abstraction.

The origin of a household becomes metadata rather than directory structure.

---

# Household Libraries

ROOST is expected to support multiple household libraries.

Possible search order:

```text
Current Workspace Library

↓

Additional User Libraries

↓

User Household Library

↓

Built-in Household Library
```

Each library contains multiple household projects.

The registry indexes projects from all visible libraries.

Libraries differ only by location.

They share a common project structure.

---

# Household Project Layout

The exact project layout remains under active design.

One possible direction is:

```text
jack_jill/

    metadata.toml

    README.md

    household.py

    case.toml

    HFP.xlsx

    notebooks/

    workspace/
```

Only a subset of these artifacts may be required.

The project directory rather than individual filenames provides household identity.

Generic filenames are therefore preferred whenever practical.

---

# Executable Specification

One long-term direction is for each household project to contain an executable specification.

Rather than treating `case.toml` as the authoritative household definition, the executable specification constructs an OWL `Plan` directly through the OWL Python API.

Conceptually:

```text
Executable Specification
        ↓
OWL Plan
        ↓
case.toml
        ↓
HFP.xlsx
        ↓
Workspace
```

The executable specification should remain:

* executable
* importable
* readable
* publishable
* testable

It should serve equally well for:

* ROOST
* pytest
* Quarto
* Jupyter
* documentation
* educational examples

---

# Construction versus Export

Construction and export should remain separate concepts.

Construction creates an OWL `Plan`.

Export serializes that plan into one or more operational representations.

Possible exported artifacts include:

* case.toml
* HFP.xlsx
* workspace
* notebooks
* future graphical editors

The executable specification should not depend upon a particular export format.

---

# Household Import

Imported households should become first-class household projects.

Rather than indexing arbitrary directories containing TOML files, ROOST should provide import workflows that curate imported households into the standard project structure.

Possible import sources include:

* OWL examples
* Existing ROOST workspaces
* Future Quicken exports
* Future financial planning tools

Import should preserve provenance whenever practical.

---

# Household Metadata

The registry should remain lightweight.

A household project should own rich metadata describing:

* title
* description
* tags
* provenance
* educational purpose
* supported artifacts

The registry should expose enough metadata for discovery while avoiding duplication of project contents.

---

# Testing Philosophy

Household projects should serve as executable analytical fixtures.

Whenever practical, the same household project should support:

* tutorials
* documentation
* regression testing
* integration testing
* benchmarking
* research

The preferred direction is to eliminate duplicated test fixtures.

Executable household projects become the canonical examples used throughout ROOST.

---

# Source Visibility

The executable specification should remain visible to users.

Human-readable construction code has educational value.

It also provides an audit trail explaining how an OWL `Plan` was created.

Future CLI workflows may expose the executable specification directly.

Possible examples include:

```text
roost household jack_jill --view source

roost household jack_jill --view notebook
```

The exact implementation remains undecided.

The goal is that the executed code and the displayed code remain identical.

---

# Household Evolution

One long-term direction distinguishes between:

* canonical household definition
* realized household evolution

Conceptually:

```text
Canonical Household
        ↓
Creation
        ↓
Canonical Plan
        ↓
Realized Overrides
        ↓
Current Planning State
```

The canonical household describes the enduring planning subject.

Realized overrides describe changes that have actually occurred over time.

The workspace realizes the current planning state by applying those realized changes.

This remains a long-term design direction rather than a current implementation requirement.

---

# Common Override Language

ROOST already uses overrides to describe hypothetical analytical transitions.

A promising long-term direction is to use the same override language for realized household evolution.

Conceptually:

```text
Canonical Household
        +
Realized Overrides
        ↓
Current Planning State
        +
Experimental Overrides
        ↓
Execution
```

Under this model, realized transitions and experimental transitions differ only by provenance.

Both share a common representation.

---

# Relationship to Workspace

The household subsystem owns the enduring planning subject.

The workspace owns the current realized planning state.

A household project should therefore remain reusable across many planning reviews.

Future work may allow a household project to reconstruct any historical review by replaying the realized transition history.

---

# Open Questions

Several important questions remain unresolved.

Examples include:

* Should the executable specification be `household.py`, `build.py`, or another name?
* Which artifacts are mandatory?
* Which metadata belongs in `metadata.toml`?
* How should imported projects be upgraded over time?
* Should household projects own notebooks directly?
* How should realized household history be represented?
* Should household libraries support versioning?

These questions should remain open until implementation experience suggests stable answers.

---

# Guiding Principle

Prefer simple implementations that preserve future flexibility.

Whenever possible:

* define concepts before implementations
* separate construction from representation
* separate canonical definitions from realized state
* favor executable examples over duplicated fixtures
* preserve human readability
* leverage OWL rather than reimplementing financial behavior

The household subsystem should evolve gradually toward a reusable, executable library of retirement planning assets that supports planning, education, research, testing, and reproducible analytical workflows.
