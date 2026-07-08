---
bundle:
  name: design-council
  version: 0.1.1
  description: The Design Intelligence Council — seven orthogonal design-evaluation lenses plus a /design-council orchestrator that runs cold fan-out, debate-to-consensus, and synthesized verdict with recorded dissent.

includes:
  - bundle: git+https://github.com/microsoft/amplifier-bundle-skills@main

# NOTE: a top-level `skills: dirs: [...]` key is NOT part of the bundle schema
# and is silently ignored by amplifier-foundation's Bundle.from_dict (it only
# reads name/version/description/includes/namespace_root/session/providers/
# tools/hooks/spawn/agents/context). Registering this bundle's ./skills
# directory with the skills system requires configuring the tool-skills
# module directly, as below — mirroring the pattern used by
# amplifier-bundle-skills' own behaviors/skills.yaml and
# amplifier-bundle-design-intelligence-enhanced's behaviors/design-skills.yaml.
tools:
  - module: tool-skills
    source: git+https://github.com/microsoft/amplifier-bundle-skills@main#subdirectory=modules/tool-skills
    config:
      skills:
        - "@design-council:skills"
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
