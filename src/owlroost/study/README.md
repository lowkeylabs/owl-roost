# Study Subsystem

The study subsystem provides a higher-level analytical layer above the core ROOST execution architecture.

Its purpose is to help users move from:

```text
What decision should I investigate?
```

to:

```text
What experiments should I run?
```

rather than requiring users to manually construct sessions and sweeps from low-level override variables.

---

# Conceptual Role

The core ROOST execution hierarchy is:

```text
Case
    ↓
Session
    ↓
Run
    ↓
Trial
```

This hierarchy answers:

```text
How was a result produced?
```

The study subsystem addresses a different question:

```text
What decisions are available,
and how should they be investigated?
```

The study subsystem therefore sits above the execution layer and helps bridge retirement questions, experimental design questions, and execution-tuning questions into reproducible analytical workflows.

---

# Decisions

A decision defines a choice space.

Examples include:

* Social Security timing
* Roth conversion strategy
* Retirement age
* Asset allocation
* Trial count selection
* Solver selection
* Worker scaling

A decision answers:

```text
What alternatives could be explored?
```

Conceptually:

```text
Decision
    ↓
Choice Templates
    ↓
Experiments
    ↓
Sessions
```

A decision does not define a specific experiment.

Instead, it defines a family of possible experiments.

For example:

```text
Decision:
    Social Security Timing

Possible Experiments:
    Annual sweep
    Monthly sweep
    Couple sweep
    Single-person sweep
```

---

# Levers

A decision may or may not be meaningful for a particular case.

ROOST therefore introduces the concept of a lever.

A lever represents a structural decision opportunity that exists within a case.

Examples:

```python
has_ss_lever
has_conversion_lever
has_retirement_lever
has_allocation_lever
```

A lever answers:

```text
Is this decision applicable
to this case?
```

Examples:

* Social Security timing is meaningful only when Social Security income exists.
* Roth conversion analysis is meaningful only when tax-deferred assets exist.
* Retirement timing is meaningful only when retirement has not already occurred.

Conceptually:

```text
Case
    ↓
Lever Detection
    ↓
Applicable Decisions
```

Levers therefore determine which decisions should be presented to a user.

---

# Decision Domains

ROOST recognizes three broad categories of decisions.

## Retirement Decisions

Questions affecting household outcomes.

Examples:

* Social Security timing
* Roth conversion
* Retirement age
* Spending strategies
* Asset allocation

---

## Design Decisions

Questions affecting analytical validity.

Examples:

* Trial count
* Sampling methodology
* Bootstrap strategy
* Historical regime selection

---

## Execution Decisions

Questions affecting computational efficiency.

Examples:

* Solver selection
* Worker scaling
* Thread scaling
* Runtime tuning
* Hardware utilization

---

# Registry Architecture

The study subsystem follows the same registry-driven architecture used throughout ROOST.

No hard-coded decision lists should exist.

No hard-coded lever lists should exist.

Registration ownership belongs to individual modules.

Conceptually:

```text
study/
    decisions/
        social_security.py
        roth_conversion.py
        retirement_age.py
        worker_scaling.py

    levers/
        social_security.py
        conversion.py
        retirement.py
```

Each module registers itself through the appropriate registry.

Bootstrap code discovers and registers all modules automatically.

---

# Intended Package Structure

```text
study/
    README.md

    bootstrap.py
    registry.py
    specs.py

    decisions/
        __init__.py
        ...

    levers/
        __init__.py
        ...
```

---

# Relationship to Studies

ROOST documentation frequently refers to studies.

A study is intentionally treated as a higher-level organizational concept rather than a first-class registry object.

Conceptually:

```text
Study
    ├── Cases
    ├── Decisions
    ├── Experiments
    ├── Sessions
    ├── Results
    ├── Reports
    └── Documentation
```

A study organizes analytical work.

A decision defines a choice space.

A lever determines whether the decision applies to a particular case.

The study subsystem therefore focuses on decisions and levers rather than attempting to formalize studies prematurely.

Future versions of ROOST may introduce study templates, study definitions, or study materialization workflows once the requirements become clearer through practical use.

---

# Long-Term Direction

The study subsystem is expected to become the primary analytical guidance layer within ROOST.

Future capabilities may include:

* Case-aware decision recommendations
* Automatic lever detection
* Experiment generation
* Session generation
* Educational walkthroughs
* Reproducible research workflows
* Publication-oriented study templates

while preserving the existing execution hierarchy and provenance model.

The goal is to help users discover meaningful decisions, construct appropriate experiments, and organize analytical work into reproducible studies.
