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

A decision defines a question that may be investigated.

Examples include:

* Social Security timing
* Roth conversion strategy
* Retirement age
* Asset allocation
* Trial count selection
* Solver selection
* Worker scaling

A decision answers:

    What question should be investigated?

Examples:

    Social Security Timing
        When should Social Security be claimed?

    Roth Conversion
        How should tax-deferred assets be converted?

    Worker Scaling
        How should execution concurrency be configured?

A decision does not define a specific methodology or experiment.

Instead, it defines a family of possible methodologies that may be materialized into experiments.

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

A decision may be investigated through
multiple choice templates, each of which
may materialize one or more experiments.

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
# Choice Templates

A choice template defines a methodology for investigating a decision.

A single decision may support multiple choice templates.

Examples:

    Decision
        Social Security Timing

    Choice Templates
        yearly_sweep
        monthly_sweep
        owl_optimizer

A choice template answers:

    How should this question be explored?

Choice templates may define:

* Required levers
* Suggested override patterns
* Experimental starting points
* Recommended methodologies

Examples:

    yearly_sweep

        roost_sweeps.ss_age_pair=
            62,63,64,65,66,67,68,69,70

    worker_scaling

        roost_settings.workers_per_run=
            2,4,6,8,12,16

Choice templates are reusable analytical recipes.

They are not execution artifacts.

---

# Levers

A lever represents a case-dependent applicability test.

Levers determine whether a particular choice template is applicable to a specific case.

Examples:

    has_social_security

    has_pretax_savings

    has_retirement_timing

A lever answers:

    Is this methodology applicable to this case?

Examples:

* Social Security analysis requires Social Security income.
* Roth conversion analysis requires tax-deferred assets.
* Retirement timing analysis requires retirement to remain a future event.

Conceptually:

    Case
        ↓
    Lever Evaluation
        ↓
    Applicable Choice Templates
        ↓
    Applicable Decisions

A choice template is applicable when all of its required levers evaluate true.

A decision is applicable when at least one of its choice templates is applicable.

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


Ownership

```text

DecisionSpec
    registered by decisions/

ChoiceTemplateSpec
    registered by choice_templates/

LeverSpec
    registered by levers/

```

Relationships flow downward only.

Levers are unaware of decisions.

Decisions are unaware of levers.


Conceptually:

```text
study/
    decisions/
    choice_templates/
    levers/
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

    choice_templates/
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

A decision defines a question.

A choice template defines a methodology.

A lever determines whether that methodology applies to a particular case.

The study subsystem therefore focuses on decisions and levers rather than attempting to formalize studies prematurely.

Future versions of ROOST may introduce study templates, study definitions, or study materialization workflows once the requirements become clearer through practical use.

---

# Architectural Relationships

The study subsystem intentionally maintains a one-way dependency graph:

    Decision
        ↓
    Choice Template
        ↓
    Lever

Decisions do not reference levers directly.

Levers do not reference decisions.

Choice templates connect decisions to applicability requirements.

This separation allows multiple methodologies to investigate the same decision while maintaining independent applicability constraints.

---

# Architectural Invariant

Choice templates own applicability.

Decisions do not own applicability.

A decision is applicable when at least one
choice template is applicable.


# Long-Term Direction

The study subsystem is expected to become the primary analytical guidance layer within ROOST.

Choice templates bridge the study subsystem
and the execution subsystem.

```text
Decision
    ↓
Choice Template
    ↓
Experiment
    ↓
Session
    ↓
Run
    ↓
Trial
```

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
