---
bundle:
  name: design-council
  version: 0.1.0
  description: The Design Intelligence Council — seven orthogonal design-evaluation lenses plus a /design-council orchestrator that runs cold fan-out, debate-to-consensus, and synthesized verdict with recorded dissent.

includes:
  - bundle: git+https://github.com/microsoft/amplifier-bundle-skills@main

skills:
  dirs:
    - ./skills
---

# Design Intelligence Council

A multi-perspective design evaluation system. Seven orthogonal persona lenses fan
out independently over a design target, debate to consensus, and produce a
synthesized verdict with recorded dissent — the proven `/council` pattern applied
to design.

## The Seven Lenses

| Lens | Load-Bearing Question |
|------|-----------------------|
| **originality-critic** | Is this genuinely novel, or a competent remix of the obvious? |
| **coherence-guardian** | Do all the design choices tell the same story? |
| **human-advocate** | Who are we excluding? Does this work for real bodies and minds? |
| **craft-inspector** | Is every detail intentional, or are there arbitrary values and unfinished states? |
| **context-tester** | Does this hold up outside the default viewport — on a phone, in sunlight, in motion? |
| **purpose-keeper** | Why does this design choice exist? What is it communicating? |
| **emotion-reader** | Does this make someone feel something, or is it technically correct but hollow? |

## Orchestrator

**`/design-council <target>`** — convene the full panel on a design target (a URL,
a file path, a screenshot, a DOM Intelligence Package, or a self-contained
description). Runs cold independent fan-out, up to three debate rounds, and a
synthesized verdict.

## Grounding

The lenses are grounded in Design Intelligence Enhanced's philosophy (Five Pillars,
Nine Dimensions, Three-Layer Sensibility Model) cross-referenced with established
design evaluation research (Norman, Rams, Nielsen, WCAG). This grounding is
attribution, not a runtime dependency — the bundle is self-contained and usable
without the ADI pipeline.

@design-council:context/design-council-awareness.md
