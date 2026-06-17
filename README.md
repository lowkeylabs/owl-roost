# ROOST

**Retirement Options and Outcomes Studies Tool**

**ROOST** (Retirement Options and Outcomes Studies Tool) evaluates **retirement decision policies**—not just static plans—by comparing how **agent-controlled actions** perform under **uncertainty** when those decisions are revisited annually.

ROOST is designed to answer questions like:

> *“Given the uncertainty I face, how flexible are my retirement decisions—and which decision policies are most robust?”*

It does this by organizing retirement analysis around a small number of clear, orthogonal concepts spanning:

* Scientific experimentation
* Stochastic simulation
* Policy comparison
* Execution provenance
* Statistical evaluation under uncertainty
* Reproducible operational execution

ROOST builds on OWL while extending retirement analysis into a broader scientific experimentation framework for studying retirement policies under uncertainty.

## License

ROOST is licensed under the GNU General Public License
version 3 or later (GPL-3.0-or-later).

ROOST builds upon OWL and is distributed under a
GPL-compatible license.


## Core Concepts

ROOST introduces several key concepts in extending the work of OWL.

* Studies
* Decisions
* Choice Templates
* Cases
* Experiments
* Sessions
* Runs
* Trials
* Results

Organizationally:

```text
Study
    ├── Cases
    ├── Experiments
    │       └── Related Runs
    ├── Sessions
    │       └── Executed Runs
    ├── Results
    ├── Reports
    └── Documentation
```

ROOST builds directly on OWL cases and
execution outputs.

# Analytical Workflow

Conceptually, ROOST guides users from
questions to evidence.

```text
Decision
    ↓
Choice Template
    ↓
Experiment
    ↓
Run
    ↓
Trial
```
Decisions define questions.

Choice templates define methodologies.

Experiments organize scientific exploration.

Runs evaluate fixed policies.

Trials represent individual stochastic realizations.


## Relationship to OWL

* **OWL** computes optimal strategies for a given case
* **ROOST** evaluates, compares, and studies retirement decision policies under uncertainty

ROOST builds on OWL’s optimization engine by providing the conceptual structure, stochastic simulation framework, scientific organization model, and tooling needed to explore retirement decisions as they are actually faced:

* Sequentially
* Under uncertainty
* Across many plausible futures
* With multiple competing policy alternatives under consideration
* With reproducible scientific experimentation and statistical evaluation


## Conceptual Relationships

The following relationships define the conceptual structure of ROOST.

```text
Case × Session → Runs
Experiment → Scientifically Related Runs
Run → Statistical Summary of Trials
Trial → Primitive Stochastic Observation
```

These concepts are intentionally asymmetric.

* Trials and runs contain scientific and statistical evidence.
* Sessions preserve operational provenance and execution history.
* Experiments organize scientific interpretation and comparison.


## Statistical and Scientific Model

ROOST distinguishes between:

* **Decision variables** that define retirement policies and strategies
* **Sampling variables** that control stochastic exploration
* **Execution variables** that control runtime and infrastructure behavior

Examples include:

| Variable Type       | Examples                                                                |
| ------------------- | ----------------------------------------------------------------------- |
| Decision variables  | Roth conversion strategy, Social Security timing, spending policy       |
| Sampling variables  | random seed, trial count, bootstrap selection                           |
| Execution variables | workers per run, resolved solver, thread counts, runtime execution mode |

This distinction is central to ROOST’s architecture.

Changing a decision variable creates a scientifically different policy evaluation.

Changing a sampling or execution variable may produce:

* Different statistical estimates
* Different convergence behavior
* Different runtime characteristics
* Different operational execution profiles

while still evaluating the same underlying policy.

## Trials and Runs

A **trial** represents a single stochastic realization of uncertainty.

Examples of stochastic variation include:

* Market returns
* Historical sequence selection
* Bootstrap sampling
* Inflation trajectories
* Longevity realizations

Trials are the primitive observations of the ROOST system.

A **run** represents a statistical evaluation of a fixed policy configuration across one or more trials.

Conceptually:

```text
Policy + Uncertainty Sampling → Run
```

Runs are the primary scientific comparison unit in ROOST.

When a run contains:

* A single trial, run-level metrics are identical to trial metrics
* Multiple trials, run-level metrics become statistical summaries over uncertainty

Examples include:

* Mean spending
* Median bequest
* P90/P95 outcomes
* Success rates
* Runtime distributions
* Sampling stability measurements

This allows ROOST to evaluate policies for robustness across many plausible futures rather than optimizing against a single deterministic scenario.

## Experiments

An **experiment** defines a structured scientific exploration for a given decision or uncertainty dimension.

Conceptually:

```text
Experiment → Scientifically Related Runs
```

An experiment answers the question:

> *“What scientific question or policy dimension are we exploring?”*

Experiments may:

* Systematically vary a decision parameter (e.g., Social Security claiming age)
* Sweep across a family of choice templates
* Explore Roth conversion strategies
* Compare spending policies
* Enumerate historical market regimes
* Compare optimization or simulation approaches
* Study execution and sampling strategies
* Test whether conclusions generalize across households

Experiments are:

* Logical rather than physical
* Scientific rather than operational
* Potentially cross-case and cross-session

A single experiment may include runs from:

* Multiple sessions
* Multiple dates
* Multiple cases/households
* Multiple execution environments

Experiments are logical scientific overlays over structurally related runs.

Experiments therefore organize and interpret related runs under a common research objective.

Experiments do **not** define filesystem structure.

They define scientific meaning.

## Generalization and Cross-Case Studies

Although many retirement studies focus on a single household, ROOST is also designed to support broader comparative analysis across multiple cases.

Experiments may explore questions such as:

* Do retirement strategies generalize across different households?
* Which policies remain robust across varying balance structures?
* How sensitive are outcomes to demographic differences?
* Which optimization strategies scale consistently across cases?
* Which execution strategies scale consistently across environments?

This allows ROOST to support both:

* Detailed household-specific retirement analysis
  and
* Cross-household scientific generalization studies

within the same conceptual framework.

## Sampling and Estimation

ROOST treats uncertainty sampling as a first-class scientific concern.

Multiple runs may evaluate the same underlying policy while differing only in:

* Random seeds
* Sampling methods
* Trial counts
* Execution configuration

This supports workflows such as:

* Combining compatible runs to increase sample sizes
* Comparing sampling strategies
* Studying estimator stability
* Evaluating convergence behavior under uncertainty
* Comparing execution strategies
* Studying runtime scaling behavior

For example:

* Two independent runs of 100 trials each may be compared against
* One run containing 200 trials

to study differences in sampling behavior and estimator quality.

Scientifically compatible runs may therefore be merged or compared even when generated in different sessions.

## Core Architectural Invariants

The following concepts are foundational to ROOST and SHOULD remain stable unless intentionally redesigned.

### Runs are the primary scientific comparison unit

Runs represent statistical evaluations of fixed policy configurations under uncertainty.

Most scientific comparison, reporting, and analysis in ROOST occurs at the run level.

### Trials are primitive stochastic observations

Trials represent individual realizations of uncertainty and are aggregated into run-level statistical summaries.


### Experiments are logical scientific overlays

Experiments organize scientifically related runs and MAY span:

* Multiple sessions
* Multiple cases
* Multiple dates
* Multiple execution environments

Experiments SHOULD remain logically decoupled from filesystem hierarchy.

### Decision, sampling, and execution variables are distinct

Decision variables alter policy meaning.

Sampling variables alter statistical estimation.

Execution variables alter runtime behavior.

These variable classes SHOULD remain conceptually distinct throughout the ROOST architecture.

## Design Philosophy

ROOST treats retirement planning as a **sequential decision problem**:

* Decisions are agent-controlled
* They are revisited annually
* Outcomes unfold under uncertainty
* Policies are evaluated across many plausible futures for robustness, not just optimality
* Runs statistically evaluate policy behavior across stochastic realizations
* Experiments organize scientific comparison and interpretation
* Sessions preserve execution provenance and support incremental exploration over time

Rather than asking:

> *“What is the single optimal plan?”*

ROOST instead helps answer:

> *“Which decision policies perform well across many plausible futures—and how much flexibility do I really have?”*

## Studies

A **study** defines a structured analytical investigation organized around a particular question, methodology, or research objective.

Studies organize:

* Scientific intent
* Variable exploration strategies
* Comparison methodologies
* Aggregation semantics
* Reporting structure
* Interpretation workflows

Studies frequently organize one or more
decisions, choice templates, and
experiments into a coherent analytical
methodology.

Conceptually:

```text
Study → Structured Interpretation of Related Runs
```

A study answers questions such as:

> *“What analytical question are we exploring, and how should the resulting evidence be interpreted?”*

Examples include:

* Social Security timing analysis
* Spending flexibility analysis
* Roth conversion strategy comparison
* Historical versus bootstrap sampling analysis
* Worker-scaling analysis
* Cross-household generalization analysis
* Statistical convergence analysis

Studies are:

* Logical rather than operational
* Methodological rather than execution-oriented
* Potentially cross-session and cross-case
* Independent of any particular execution event

Studies provide the analytical context within which experiments, runs, and results are interpreted.

## Studies as Reproducible Research Packages

A study is intended to become the primary unit of sharing, reproduction, publication, and education within ROOST.

Studies may contain:

* Cases
* Household Financial Profiles (HFPs)
* Experiments
* Results
* Reports
* Documentation
* Visualizations
* Publication artifacts

Conceptually:

```text
Study
    ├── Cases
    ├── Experiments
    ├── Results
    ├── Reports
    └── Documentation
```

Studies are intentionally broader than experiments.

An experiment defines a scientific manipulation or comparison.

A study defines the broader analytical context in which one or more experiments are interpreted, documented, reproduced, and communicated.

Examples include:

* Social Security timing studies
* Roth conversion studies
* Runtime scaling studies
* Sampling convergence studies
* OWL methodology tutorials
* Publication and reproducibility packages

Studies therefore complement rather than replace experiments.

## Study Templates

A **study template** defines a reusable analytical methodology capable of generating studies and their associated analytical workflows.

Conceptually:

```text
Study Template
    ↓
Study
    ↓
Experiments
    ↓
Results
    ↓
Reports
```

Study templates may define:

* Decision-variable sweeps
* Sampling-variable sweeps
* Execution-variable sweeps
* Comparison structures
* Aggregation methodologies
* Reporting templates
* Visualization workflows

A study template may operationalize investigations such as:

```text
Explore retirement age sensitivity
    across:
        retirement ages
        market sampling methods
        uncertainty realizations
```

or:

```text
Evaluate runtime scaling behavior
    across:
        workers_per_run
        thread allocation
        solver configurations
```

Long-term, study templates are intended to support increasingly automated workflows in which ROOST can:

* Instantiate studies from reusable methodologies
* Generate experiments
* Infer comparison dimensions
* Produce reports and dashboards
* Organize scientific interpretation

This direction extends ROOST beyond simple parameter sweeps into a broader framework for retirement decision analysis, uncertainty analysis, runtime analysis, comparative research, and methodological evaluation.

## Relationship to Variable Classes

Study semantics are strongly influenced by the classes of variables being explored.

ROOST distinguishes between:

| Variable Class      | Analytical Meaning                    |
| ------------------- | ------------------------------------- |
| Decision variables  | Retirement policy exploration         |
| Sampling variables  | Uncertainty and estimator exploration |
| Execution variables | Runtime and computational exploration |

This distinction allows ROOST to support multiple categories of studies within a unified framework.

Examples include:

| Study Type             | Primary Variable Classes |
| ---------------------- | ------------------------ |
| Retirement policy      | Decision variables       |
| Sampling analysis      | Sampling variables       |
| Runtime scaling        | Execution variables      |
| Methodology comparison | Mixed variable classes   |

Over time, these distinctions may support increasingly automated inference of:

* Study categories
* Comparison methodologies
* Aggregation semantics
* Visualization strategies
* Reporting structures
* Suggested analytical workflows


## Future Direction

ROOST is evolving toward increasingly
automated study-centered workflows.

Future capabilities may include:

* Automated study generation
* Study-oriented reporting
* Publication-oriented research packages
* Automated comparison workflows
* Methodology-driven analysis

The goal is to make studies the primary
unit of reproducibility, communication,
education, and research while preserving
the core concepts described throughout
this document.
