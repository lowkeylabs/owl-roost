# Household Library

This directory contains the built-in **Household Library** distributed with ROOST.

Each subdirectory is an independent **Household Project** that may be discovered, registered, exported, executed, documented, and reused.

Household Projects serve simultaneously as:

* executable examples
* educational tutorials
* regression fixtures
* documentation assets
* research artifacts

The Household Library provides the canonical collection of reusable planning situations shipped with ROOST.

---

# Architectural Role

Within the ROOST architecture:

```text
Household Library
        ↓
Household Discovery
        ↓
Household Registry
        ↓
Household Specification
        ↓
Workspace
        ↓
Characterization
        ↓
Experiments
```

The Household Library owns examples.

It does not own registration.

It does not own discovery.

Those responsibilities belong to the household subsystem.

---

# Household Projects

Every immediate subdirectory containing a valid `manifest.toml` is considered a Household Project.

For example:

```text
households/

    minimum/

    complete/

    tutorial_social_security/

    roth_conversion/

    alex_jamie/
```

Directory names should be short, descriptive, and stable.

The directory name does not need to match the household identifier, although doing so is generally recommended.

---

# Typical Project Layout

A minimal Household Project contains:

```text
project/

    manifest.toml

    household.py
```

A more complete project may additionally contain:

```text
project/

    README.md

    manifest.toml

    household.py

    case.toml

    HFP.xlsx

    figures/

    reports/

    notebooks/
```

Only the manifest is required for discovery.

Additional files provide documentation, generated artifacts, or alternative representations of the household.

---

# Canonical Artifacts

## manifest.toml

Provides the canonical metadata describing the Household Project.

Typical fields include:

* household identifier
* title
* description
* tags
* manifest version

The manifest supports discovery and registration.

It does not define the household itself.

---

## household.py

Provides the executable specification of the household.

The module should expose a small public interface capable of constructing and exporting the household.

Future revisions are expected to build an OWL `Plan` directly.

Whenever practical, the executable specification should remain readable enough to serve as tutorial material.

---

## case.toml

Represents one serialized configuration of the household.

Whenever practical this file should be generated rather than edited manually.

---

## HFP.xlsx

Represents one Household Financial Profile.

Like the TOML configuration, this workbook should preferably be generated from the executable specification whenever tooling permits.

---

## README.md

Describes the planning scenario represented by the project.

This documentation is intended for humans rather than discovery.

---

# Executable Specifications

The executable specification is the preferred authoritative representation of a household.

Rather than manually maintaining multiple synchronized artifacts, the long-term direction is:

```text
household.py
        ↓
OWL Plan
        ↓
case.toml
        ↓
HFP.xlsx
```

Generated artifacts should remain reproducible whenever practical.

---

# Educational Philosophy

Household Projects should be understandable.

A reader should be able to open `household.py` and learn how the household is constructed using OWL.

Whenever practical:

* prefer explicit code over abstraction
* prefer readability over cleverness
* prefer small examples over comprehensive ones

Examples should teach as well as execute.

---

# Testing

Every Household Project should be executable.

The same project should support:

* documentation
* regression testing
* integration testing
* benchmarking
* tutorials

Whenever practical, avoid creating separate testing fixtures that duplicate existing Household Projects.

---

# Future Direction

The Household Library is expected to grow over time.

Future projects may include:

* OWL tutorial households
* synthetic households
* historical planning examples
* published research cases
* imported households
* educational exercises
* benchmark problems

The preferred direction is to expand the Household Library rather than introduce one-off examples elsewhere in the repository.

Every Household Project should remain portable, executable, reproducible, and understandable.
