# Workspace Subsystem

The workspace subsystem owns the creation, materialization, organization, and lifecycle management of ROOST workspaces.

A workspace is the primary shareable unit within ROOST.

Conceptually:

```text
Workspace
    ↓
Study Definition
    ↓
Cases
    ↓
Results
    ↓
Work Products
```

The workspace subsystem is intentionally distinct from the study subsystem.

The study subsystem provides analytical guidance through:

```text
Decision
    ↓
Choice Template
    ↓
Lever
```

The workspace subsystem provides a physical environment in which analytical work is organized, executed, documented, and shared.

---

# Purpose

The workspace subsystem exists to support reproducible retirement analysis.

A workspace should be:

* Shareable
* Portable
* Self-documenting
* Rebuildable
* Suitable for publication
* Suitable for education
* Suitable for long-term archival

Workspaces may be distributed as simple directories, zip files, Git repositories, or published examples.

The same workspace abstraction should support:

* Small retirement examples
* Decision investigations
* Comparative studies
* Documentation examples
* Educational walkthroughs
* ROOST self-documentation workflows

---

# Architectural Role

ROOST distinguishes between:

```text
Analytical Guidance
```

and

```text
Analytical Organization
```

The study subsystem owns analytical guidance.

The workspace subsystem owns analytical organization.

Conceptually:

```text
Study Subsystem
    ↓
Decision Discovery
    ↓
Experiment Design

Workspace Subsystem
    ↓
Workspace Creation
    ↓
Materialization
    ↓
Documentation
    ↓
Publication
```

The two subsystems are complementary but intentionally independent.

---

# Workspace Philosophy

A workspace should remain as lightweight as possible.

A study author should not be required to understand ROOST internals in order to create or use a workspace.

The workspace should expose content.

ROOST should own machinery.

Whenever possible:

```text
Workspace
    owns:
        content

ROOST
    owns:
        implementation
```

This separation minimizes clutter and reduces maintenance burden.

---

# Minimal Workspace

The minimal workspace is intentionally small:

```text
my_study/
├── study.toml
└── Makefile
```

The workspace definition is authoritative.

Additional files and directories are optional.

---

# Study Definition

The canonical study definition is:

```text
study.toml
```

The study definition describes:

* Study identity
* Study metadata
* Study documentation
* Study configuration
* Materialization behavior

Future workspace capabilities should derive from the study definition whenever practical.

Avoid duplicating metadata across multiple files.

---

# Generated Content

The workspace subsystem may materialize generated content.

Examples include:

```text
cases/
results/
index.qmd
```

Generated content should not be considered authoritative.

Generated content should be rebuildable from the study definition and associated source materials.

Conceptually:

```text
study.toml
    ↓
materialization
    ↓
cases
results
index.qmd
```

---

# Cases

Cases are generated artifacts.

Cases represent executable retirement households.

Conceptually:

```text
study definition
    ↓
case generation
    ↓
cases/
```

Cases are intentionally treated as materialized outputs rather than workspace definitions.

---

# Results

Results are generated artifacts.

Results represent materialized execution outputs.

Conceptually:

```text
cases
    ↓
execution
    ↓
results/
```

Results should be reproducible whenever possible.

---

# Work Products

Work products are human-facing outputs produced from cases, results, or both.

Examples include:

* Papers
* Reports
* Dashboards
* Figures
* Presentations
* Spreadsheets
* Educational materials

ROOST intentionally does not impose a required organizational structure for work products.

Study authors may organize work products in whatever manner best supports the study.

---

# Makefiles

Workspaces are expected to expose a consistent build interface.

Typical targets include:

```text
make validate
make cases
make results
make all

make clean
make realclean
make pristine
```

The Makefile serves as the public workflow interface.

ROOST should own the majority of implementation logic.

Workspace-specific Makefiles should remain small whenever possible.

A typical workspace Makefile may consist primarily of:

```make
-include $(shell roost paths --makefile)
```

with optional study-specific extensions.

---

# Workspace Creation

Future versions of ROOST are expected to support:

```bash
roost workspace create <name>
```

or equivalent commands.

Workspace creation should generate a minimal workspace rather than a large project skeleton.

The default workspace should remain approachable to novice users.

---

# Architectural Invariants

The following invariants should be preserved.

## Study definitions are authoritative.

The study definition is the canonical source of workspace metadata.

Generated files should not become competing sources of truth.

## Generated content is disposable.

Cases, results, generated documentation, and similar outputs should be rebuildable.

## Workspaces remain lightweight.

Do not require every workspace to become a software project.

Avoid unnecessary directory structures.

Avoid introducing mandatory implementation scaffolding.

## ROOST owns machinery.

Workspace authors should focus on analytical content.

ROOST should own orchestration, materialization, validation, and workflow infrastructure whenever practical.

## Simplicity is preferred.

A simple study should remain simple.

Advanced capabilities should not impose complexity on small workspaces.

---

# Long-Term Direction

The workspace subsystem is expected to become the primary mechanism for:

* Study creation
* Study materialization
* Reproducible retirement analysis
* Educational examples
* Documentation generation
* Publication workflows
* ROOST self-documentation

The workspace abstraction should remain centered on retirement analysis while providing sufficient flexibility to support the broader educational and documentation needs of the ROOST ecosystem.
