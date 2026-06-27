# FUTURE-README.md

> **Temporary Note (to be removed later)**
>
> This document captures the current direction and emerging conceptual center of ROOST.
>
> It is intentionally forward-looking and may differ from the current implementation or from README.md.
>
> The purpose of this document is alignment:
>
> * Future maintainers
> * Future LLM collaborators
> * Future design discussions
>
> The concepts described here are expected to evolve through implementation and use.
>
> This document should remain focused on enduring architectural ideas rather than subsystem details.

# ROOST

**Retirement Options and Outcomes Studies Tool**

ROOST is a household-centered evidence generation system for financial life planning.

ROOST helps individuals, households, researchers, educators, and advisors explore important financial questions by generating evidence about alternative actions, timings, and outcomes.

ROOST is built upon OWL and its ability to evaluate household financial outcomes under uncertainty.

ROOST does not primarily seek a single optimal answer.

Instead, ROOST helps answer questions such as:

* Can I retire?
* When should I retire?
* How much can I spend?
* When should I claim Social Security?
* Should I perform Roth conversions?
* How flexible are my options?
* How sensitive are outcomes to my decisions?
* Can I safely wait before deciding?

ROOST generates evidence.

Humans, advisors, and LLMs interpret that evidence.

Decisions remain the responsibility of the decision-maker.

---

# Vision

Financial planning is fundamentally a process of asking questions, exploring alternatives, understanding uncertainty, and making informed decisions.

ROOST exists to support that process.

Conceptually:

```text
Household
    ↓
Question
    ↓
Evidence Generation
    ↓
Evidence Package
    ↓
Interpretation
    ↓
Decision
```

ROOST focuses on evidence generation.

Interpretation may be performed by:

* Individuals
* Advisors
* Educators
* Researchers
* LLMs
* Future guidance systems

---

# The Household is the Primary Context

Every ROOST investigation begins with a household.

A household is represented by:

* Household configuration data
* Financial information
* Assumptions
* Constraints
* Goals

Households may be:

* Real households
* Example households
* Educational households
* Research households
* Synthetic households

All analysis is performed in the context of a household.

Financial concepts become meaningful when applied to a specific household.

---

# Questions are the Primary User-Facing Object

Questions are the primary way users interact with ROOST.

Examples include:

* Can I retire?
* Should I retire?
* When should I retire?
* How much can I spend?
* Should I claim Social Security?
* When should I claim Social Security?
* Should I perform Roth conversions?
* How much should I convert?

Future questions may address other aspects of financial life planning.

Questions define information needs.

Questions do not directly produce evidence.

---

# Evidence Generation

ROOST generates evidence by exploring alternative actions, choices, timings, assumptions, and uncertainties.

Examples include:

* Retiring this year versus next year
* Claiming Social Security at different ages
* Performing Roth conversions versus skipping conversions
* Different spending levels
* Different market environments
* Different longevity assumptions

ROOST evaluates these alternatives using OWL and associated analytical machinery.

Evidence generation is systematic, reproducible, and transparent.

---

# Execution Plans

An execution plan describes how evidence will be generated for one or more questions.

An execution plan answers:

* What question is being investigated?
* What information is available?
* What information is missing?
* What alternatives will be explored?
* What evidence will be generated?
* How much execution is required?

Conceptually:

```text
Question
    ↓
Execution Plan
    ↓
Evidence Generation
```

Execution plans are intended to be understandable by both technical and non-technical users.

---

# Evidence Packages

An evidence package is the primary output of ROOST.

An evidence package contains evidence relevant to one or more questions.

Examples may include:

* Outcome summaries
* Sensitivity analysis
* Alternative comparisons
* Uncertainty analysis
* Visualizations
* Supporting metrics
* Explanatory narratives

Conceptually:

```text
Execution
    ↓
Evidence Package
```

Evidence packages are intended for:

* Human review
* Advisor review
* Educational use
* Research use
* LLM-assisted interpretation

---

# Interpretation

ROOST distinguishes between evidence generation and interpretation.

ROOST generates evidence.

Interpretation evaluates that evidence.

Interpretation may discuss:

* Tradeoffs
* Risks
* Opportunities
* Sensitivity
* Flexibility
* Optionality
* Safe deferral
* Additional information needs

Interpretation should clearly distinguish evidence from speculation.

---

# Documentation and Communication

Evidence should be easy to communicate, review, reproduce, and share.

ROOST therefore treats documentation as a first-class outcome.

Typical outputs may include:

* Reports
* Dashboards
* Websites
* Educational materials
* Research artifacts
* LLM briefing packages

Documentation should support both high-level understanding and detailed inspection.

---

# LLM Collaboration

LLMs are considered important consumers of ROOST evidence.

ROOST should provide structured information suitable for LLM interpretation.

LLM-oriented outputs may include:

* Household summaries
* Question summaries
* Evidence summaries
* Key findings
* Important uncertainties
* Guardrails
* Suggested interpretation prompts

The goal is not to outsource decisions to LLMs.

The goal is to improve interpretation of evidence.

---

# Reproducibility

ROOST values reproducibility.

Evidence generation should be:

* Repeatable
* Inspectable
* Transparent
* Documented

Users should be able to understand:

* What was investigated
* How evidence was generated
* What assumptions were used
* How conclusions were reached

---

# Architectural Invariants

The following concepts are foundational to ROOST.

These concepts should remain stable unless intentionally redesigned.

## Households are the primary analytical context

All investigations are performed in the context of a household.

## Questions are the primary user-facing entities

Users interact with ROOST through questions rather than implementation details.

## Execution plans describe intended evidence generation

Execution plans explain what evidence will be generated and why.

## Evidence packages describe generated evidence

Evidence packages are the primary analytical outputs of ROOST.

## ROOST generates evidence

ROOST is responsible for evidence generation.

## Interpretation is separate from evidence generation

Evidence generation and interpretation are distinct activities.

## OWL remains the analytical engine

ROOST builds upon OWL's ability to evaluate household financial outcomes.

## Documentation is a first-class outcome

Generated evidence should be understandable, reviewable, reproducible, and shareable.

## ROOST should use its own workflow

ROOST should document, validate, teach, and evaluate itself using the same question-driven workflow it provides to users.

---

# Long-Term Direction

ROOST is evolving toward increasingly question-centered workflows.

Conceptually:

```text
Household
    ↓
Questions
    ↓
Execution Plans
    ↓
Evidence Packages
    ↓
Documentation
    ↓
Human and LLM Interpretation
```

The goal is not to find a single optimal answer.

The goal is to help people understand their choices, explore uncertainty, evaluate alternatives, and make informed decisions with confidence.
