# Study Subsystem

The study subsystem provides the analytical guidance layer of ROOST.

Its purpose is to help users move from:

```text
What question am I trying to answer?
```

to:

```text
What evidence should be generated?
```

without requiring users to manually construct sessions, runs, sweeps, or low-level override configurations.

The study subsystem sits between:

```text
retirement questions
```

and

```text
execution workflows
```

and is responsible for transforming analytical intent into reproducible investigation strategies.

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
What should be investigated,
and how should it be investigated?
```

The study subsystem therefore owns:

* Question discovery
* Question organization
* Question applicability
* Experiment generation
* Analytical guidance

while remaining independent of execution realization.

---

# Question-Centric Architecture

ROOST is intentionally question-driven.

Users rarely begin with:

```text
What sweep should I run?
```

Instead they begin with:

```text
Can I retire?

When should I retire?

When should I claim Social Security?

Should I perform Roth conversions?

How much can I spend?
```

The study subsystem therefore treats:

```text
Question
```

as the primary user-facing analytical abstraction.

Experiments exist to answer questions.

Questions do not exist to justify experiments.

---

# Conceptual Hierarchy

Conceptually:

```text
Study
    ↓
Question
    ↓
Decision
    ↓
Choice Template
    ↓
Lever
    ↓
Experiment
```

Experiments bridge the study subsystem and the execution subsystem:

```text
Experiment
    ↓
Session
    ↓
Run
    ↓
Trial
```

---

# Studies

A study organizes related retirement questions.

Studies provide analytical context and help users discover adjacent questions that may be relevant to their situation.

Examples:

```text
Retirement Readiness

Social Security Strategy

Tax Strategy

Market Uncertainty

Spending Sustainability
```

A study answers:

```text
What collection of related
questions should be explored?
```

Studies may contain many questions.

Questions may participate in multiple studies.

Studies are organizational entities.

Studies are not execution artifacts.

---

# Questions

Questions represent the primary analytical entities within the study subsystem.

Examples:

```text
Can I retire?

When can I retire?

How much can I spend?

When should I claim Social Security?

Should I perform Roth conversions?

How much should I convert this year?
```

Questions may:

* Participate in multiple studies
* Reference multiple decisions
* Require assumptions
* Require additional data
* Require analytical methodologies
* Require future research

Questions are intentionally independent of case applicability.

Applicability is determined through decisions, choice templates, and levers.

---

# Question Relationships

Questions form a relationship graph.

Questions may:

```text
refine other questions

suggest related questions

depend on prerequisite questions

participate in multiple studies
```

Examples:

```text
Can I retire?
    ↓

How much can I spend?

When can I retire?

What are my major risks?
```

and:

```text
When should I claim Social Security?
    ↓

How much does claiming age matter?

How does claiming affect my spouse?

How does claiming affect spending?
```

These relationships support:

* Discovery
* Recommendation
* Educational workflows
* Study navigation

---

# Decisions

A decision defines an analytical dimension that may be investigated.

Examples include:

* Social Security timing
* Roth conversion strategy
* Retirement age
* Asset allocation
* Trial count selection
* Sampling methodology
* Solver selection
* Worker scaling

A decision answers:

```text
What dimension of the problem
should be varied or explored?
```

Decisions are implementation-oriented analytical entities.

Questions may reference one or more decisions.

Decisions do not define methodologies directly.

---

# Choice Templates

A choice template defines a methodology for investigating a decision.

Examples:

```text
yearly_sweep

monthly_sweep

owl_optimizer

worker_scaling
```

A choice template answers:

```text
How should this decision
be explored?
```

Choice templates may define:

* Required levers
* Suggested override patterns
* Experimental starting points
* Recommended methodologies

Examples:

```text
roost_sweeps.ss_age_pair=
    62,63,64,65,66,67,68,69,70
```

Choice templates are reusable analytical recipes.

They are not execution artifacts.

---

# Levers

A lever represents a case-dependent capability test.

Examples:

```text
has_social_security

has_pretax_savings

has_retirement_timing
```

A lever answers:

```text
Can this investigation
be performed?
```

Levers evaluate case structure and determine whether a particular choice template may be applied.

Conceptually:

```text
Case
    ↓
Lever Evaluation
    ↓
Applicable Choice Templates
    ↓
Applicable Decisions
    ↓
Applicable Questions
```

---

# Guidance and Remediation

Levers are expected to evolve beyond simple applicability checks.

A false lever should eventually help answer:

```text
Why can't this question
be answered?

What information is missing?

What assumptions are required?

How can the user proceed?
```

Examples include:

```text
Missing Social Security information

Missing tax-deferred accounts

Missing retirement age assumptions
```

Potential guidance may include:

* HFP worksheet recommendations
* Data collection suggestions
* Assumption clarification
* Additional study recommendations

The long-term goal is to transform:

```text
Question unavailable
```

into:

```text
Question unavailable today.

Here are the steps needed
to make it answerable.
```

---

# Question Answerability

Questions exist on an answerability spectrum.

Examples include:

```text
Answerable Today

Requires Assumptions

Requires Additional Data

Requires New Methodology

Requires Research
```

Some questions may be directly materialized into experiments.

Others may require:

* Additional household information
* Clarified objectives
* New analytical methodologies
* Future research

The study subsystem is expected to help users navigate this progression.

---

# Decision Domains

ROOST currently recognizes three broad categories of decisions.

## Retirement Decisions

Questions affecting household outcomes.

Examples:

* Social Security timing
* Roth conversion strategy
* Retirement age
* Spending strategy
* Asset allocation

## Design Decisions

Questions affecting evidence generation.

Examples:

* Trial count
* Sampling methodology
* Bootstrap strategy
* Historical regime selection

## Execution Decisions

Questions affecting computational realization.

Examples:

* Solver selection
* Worker scaling
* Thread scaling
* Runtime tuning

Execution decisions should affect runtime behavior rather than retirement interpretation.

---

# Registry Architecture

The study subsystem follows the same registry-driven architecture used throughout ROOST.

Registration ownership belongs to individual modules.

Conceptually:

```text
StudySpec
    registered by studies/

QuestionSpec
    registered by questions/

DecisionSpec
    registered by decisions/

ChoiceTemplateSpec
    registered by choice_templates/

LeverSpec
    registered by levers/
```

Relationships flow downward.

Conceptually:

```text
Study
    ↓
Question
    ↓
Decision
    ↓
Choice Template
    ↓
Lever
```

Levers remain unaware of higher-level entities.

Questions remain independent of specific studies.

Studies organize questions through references.

This allows:

* Question reuse
* Multi-study participation
* Independent evolution of analytical workflows

---

# Intended Package Structure

```text
study/
    README.md

    bootstrap.py
    registry.py
    specs.py

    studies/
        __init__.py
        ...

    questions/
        __init__.py
        ...

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

# Architectural Invariants

Studies organize questions.

Questions are first-class analytical entities.

Questions may participate in multiple studies.

Experiments answer questions.

Results provide evidence for answers.

Choice templates own applicability.

Levers own capability evaluation.

Execution artifacts remain outside the study subsystem.

The study subsystem defines work that should be performed.

The execution subsystem realizes that work.

---

# Long-Term Direction

The study subsystem is expected to become the primary analytical guidance layer within ROOST.

Future capabilities may include:

* Case-aware question recommendations
* Adjacent-question discovery
* Automatic lever detection
* Experiment generation
* Session generation
* HFP guidance workflows
* Educational walkthroughs
* Research-gap discovery
* Reproducible research workflows
* Publication-oriented study templates

The long-term goal is to help users:

```text
Discover questions

Understand requirements

Generate evidence

Interpret results
```

while preserving the existing execution hierarchy and provenance model.
