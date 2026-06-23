Yes, and I think that's actually better than introducing a separate `docs/` tree.

What you're describing is that the documentation itself becomes a first-class ROOST publication artifact.

Something like:

```text
site-src/

├── index.qmd
│
├── vision/
│   ├── future-readme.qmd
│   ├── workflow.qmd
│   └── concepts.qmd
│
├── architecture/
│   ├── architecture.qmd
│   ├── registries.qmd
│   ├── ontology.qmd
│   ├── workspace.qmd
│   ├── study.qmd
│   ├── catalog.qmd
│   ├── display.qmd
│   └── execution.qmd
│
├── developer/
│   ├── contributing.qmd
│   ├── design-principles.qmd
│   └── self-documentation.qmd
│
└── studies/
    └── ...
```

Then:

```bash
quarto render
```

produces:

```text
docs/
    index.html
```

for:

* GitHub Pages
* PyPI project links
* JOSS references
* Contributor onboarding
* Future LLM context

all from the same source.

---

The thing I particularly like is that this aligns with your dogfooding principle.

ROOST already wants to produce:

```text
Question
    ↓
Evidence Package
    ↓
Documentation
```

for retirement investigations.

Why shouldn't ROOST itself be documented the same way?

For example:

```text
site-src/architecture/workspace.qmd
```

might literally be generated from:

```text
Question:
    How does the workspace subsystem work?

Evidence:
    Registry inventory
    Class inventory
    Workflow diagrams
    Example workspaces
```

The architecture documentation becomes another evidence package.

---

I would probably think of the documentation hierarchy as having three layers.

## Layer 1 — Vision

Audience:

```text
Retirees
Advisors
Researchers
Educators
New Users
```

Examples:

```text
What is ROOST?

Why does ROOST exist?

How does the workflow work?

What is an evidence package?
```

This is where the future README belongs.

---

## Layer 2 — Architecture

Audience:

```text
Contributors
Reviewers
Future Maintainers
Future LLMs
JOSS Readers
```

Examples:

```text
How are questions represented?

How do registries work?

Why is metadata registry-driven?

How are execution plans materialized?

How does the catalog ontology work?
```

---

## Layer 3 — Reference

Audience:

```text
Developers
Advanced Users
```

Examples:

```text
CLI Reference

Variable Catalog

Metric Catalog

Filesystem Layout

Configuration Reference
```

These can be increasingly auto-generated.

---

What I find interesting is that your existing self-documentation work is already pushing in this direction.

You have:

```text
Catalog
    ↓
Metadata

Display
    ↓
Explanation

Registry
    ↓
Discovery
```

which means much of the architecture documentation could eventually be generated rather than hand-written.

For example:

```text
Catalog Variables

Metrics

Studies

Questions

Choice Templates

Levers

Views
```

can all become living documentation.

---

For a JOSS paper, I'd actually expect citations to point into sections like:

```text
Architecture

Ontology

Workflow

Reproducibility

Evidence Packages
```

rather than a giant README.

A Quarto site is a much stronger long-term artifact.

---

So if I were naming things today, I'd probably do:

```text
site-src/

    vision/
        future-readme.qmd

    architecture/
        architecture.qmd

    reference/
        ...
```

and think of:

```text
future-readme.qmd
```

as the conceptual north star.

Not the repository README.

Not a design note.

But the canonical statement of:

```text
What ROOST is trying to become.
```

Everything else—architecture pages, subsystem pages, generated reference pages, studies, and even self-documentation—exists to support and realize that vision.
