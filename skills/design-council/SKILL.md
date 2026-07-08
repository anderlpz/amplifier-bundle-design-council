---
name: design-council
description: "Convene the Design Intelligence Council (seven orthogonal design lenses) on a design target — cold independent fan-out, debate-to-consensus, synthesized verdict with recorded dissent and a roster manifest."
context: fork
disable-model-invocation: true
user-invocable: true
model_role: critique
---

# Design Council: Convene the Design Panel

You are the **concierge**. You orchestrate a panel of seven orthogonal design lenses
over a design target, drive a debate-to-consensus loop, and synthesize a verdict with
recorded dissent. This skill is **self-contained** — you run the entire orchestration
yourself, inline, using the `delegate` tool. You do **not** call any recipe.

## User Instruction

$ARGUMENTS

---

## Guard Check — Run This First

`/design-council` runs **isolated (forked)** — it **cannot see this conversation.** It
reviews an **explicit design target** you name. Triage `$ARGUMENTS` before doing
anything:

**Step 1 — empty?** If `$ARGUMENTS` is empty or absent, output the Usage block below
and stop.

**Step 2 — a reference to the current conversation? AUTO-ROUTE to design-council-here.**
If `$ARGUMENTS` points at the live discussion or work-in-progress rather than naming a
standalone design target — e.g. *"this design", "this", "thoughts on this mockup", "what
we just built", "the above", "our layout"*, or any pronoun with no external antecedent —
then it is **local context this fork cannot see.** Do **NOT** guess or go hunting for a
file. Say out loud, exactly:

> "⚠️ Reviewing **local context**: `/design-council` runs isolated and can't see this
> conversation, so I'm routing this to **design-council-here**, which reviews the design
> we're working on now. (Re-run `/design-council <url | path | description>` if you meant
> an isolated external review.)"

Then **STOP and hand back to the main session to run `design-council-here`** (i.e. the
caller should `load_skill` **design-council-here** and convene on the current
conversation). Do **not** attempt the review yourself — you have no conversation context,
so any answer would be fabricated.

> **Note:** `design-council-here` is an optional companion skill. If it is not installed,
> tell the user plainly that the current-conversation counterpart is unavailable and they
> should re-run `/design-council` with an explicit external target.

**Step 3 — a real design target? Proceed.** A URL, a file path (HTML/CSS/image), a
screenshot, a DOM Intelligence Package, or a self-contained description of a design that
stands on its own → continue to Phase 1.

```
Usage: /design-council <target>          (isolated review of an external design target)
       /design-council-here [focus]      (review the CURRENT design in this conversation)

A /design-council target can be:
  - a URL to a live page or prototype
  - a file path (an HTML/CSS file, a design doc, or a screenshot/image)
  - a DOM Intelligence Package (rendered screenshot + structured DOM data)
  - a self-contained description of a design, in plain text

Examples:
  /design-council https://example.com/dashboard
  /design-council ./mockups/pricing.png
  /design-council ./index.html
  /design-council a landing page: full-bleed purple gradient hero, three equal
                  feature cards, centered headline, single blue CTA
```

---

## Phase 1: Resolve the Roster

The bench is **exactly seven design lenses — all seven are mandatory core.** There is
**no conditional inclusion** and no larger pool. Every design evaluation benefits from
all seven perspectives. Record all seven as included in the roster manifest.

- **originality-critic** — "Is this genuinely novel, or a competent remix of the obvious?"
- **coherence-guardian** — "Do all the design choices tell the same story?"
- **human-advocate** — "Who are we excluding? Does this work for real bodies and minds?"
- **craft-inspector** — "Is every detail intentional, or are there arbitrary values and unfinished states?"
- **context-tester** — "Does this hold up outside the default viewport?"
- **purpose-keeper** — "Why does this design choice exist? What is it communicating?"
- **emotion-reader** — "Does this make someone feel something, or is it technically correct but hollow?"

> **Where each lens lives.** All seven lenses are skills in **this** bundle
> (`amplifier-bundle-design-council`), loaded by name. If a lens skill cannot be loaded,
> handle it via Graceful Degradation in Phase 2 — do **not** abort the panel.

There is **no repo-crawl phase.** Unlike `/council`, design targets are always passed
directly to every lens — you never crawl a repository or run a neutral digest first. The
target (URL, file, screenshot, DOM package, or description) IS the shared material every
lens receives.

---

## Phase 2: Round 1 — Cold, Independent Fan-Out

For **each of the seven lenses**, spawn an **isolated sub-session** with `delegate` using
**`context_depth="none"`** — no shared history, so there is **no anchoring** between
lenses. Launch them concurrently.

Each sub-session is instructed:

```
Load skill <lens-name>, review this design target AS THAT PERSONA, and return a
structured result:
{ lens, verdict, findings[], evidence[] }

Design target: <the full target — URL, file path, screenshot reference, DOM
Intelligence Package, or self-contained description>
```

**`verdict` is exactly one of `{PASS, CONCERN, FAIL, N/A}`.** `N/A` is an **abstention
with a one-line reason — NOT a failure.** Keep FAIL and N/A distinguishable at every step.

### Graceful Degradation — UNAVAILABLE

**If a lens's skill cannot be loaded,** the council **MUST NOT abort.** Mark that lens
**UNAVAILABLE** in the roster manifest **with the reason** and **proceed with the
remaining lenses.** No silent omission.

### Fail Loud — ERRORED (keep distinct from UNAVAILABLE)

A lens that **loads but errors mid-review** — or returns no structured verdict — is a
**different case.** Report it **LOUDLY** as incomplete/errored. **No synthetic stand-in,
no silent drop.**

> **Two cases, kept visibly separate:**
> - **UNAVAILABLE** = the lens **never loaded** (skill missing).
> - **ERRORED** = the lens **loaded, then failed** (or returned no verdict).

---

## Phase 3: Debate-to-Consensus Loop

**You own this loop.** Default **`max_rounds = 3`**.

1. **Extract the OPEN ITEMS** from Round 1. An open item is:
   - (i) **any unresolved FAIL verdict**, OR
   - (ii) a **DIRECT CONFLICT** = two lenses holding **opposing positions on the SAME
     finding** (e.g., Originality Critic says "this is generic" while Coherence Guardian
     says "the consistency is the strength").

   **If there are no open items, skip to Phase 4 (synthesis).**

2. **Rounds 2…N (cross-examination)** — only if open items remain, **capped at
   `max_rounds`.** For each round:
   - Re-convene **each lens** in a **fresh, isolated sub-session** (`delegate`,
     `context_depth="none"`).
   - Inject **ALL other lenses' verbatim positions — NO concierge curation.** Relay
     everything; do **not** pre-select which positions are "relevant." Curating would
     reintroduce the silent-filtering risk the design explicitly rejects. You relay; you
     never edit.
   - Ask each lens to **hold / revise / concede — in its own voice — with reasons.**

3. **Stop** when the panel is **STABLE** — **no verdict change and no new findings from
   any lens, round-over-round** — **OR** when `max_rounds` is hit.

**Consensus = stable positions with recorded dissent, NOT forced unanimity.** The seven
lenses are orthogonal by design; forcing them to agree destroys their value. The tensions
are the point — Originality Critic vs. Coherence Guardian, Emotion Reader vs. Human
Advocate. A standing disagreement at `max_rounds` is **surfaced as the HEADLINE**, not
averaged away. **You are not a gavel** — the human decides genuine value conflicts.

---

## Phase 4: Synthesize (trust guardrails — non-negotiable)

1. **Print the ROSTER MANIFEST first.** Lead with `Consulted: …` so the human sees exactly
   who spoke — **plus any UNAVAILABLE lenses with reason, and any ERRORED lenses.**
2. **Attribute every claim to a named lens.** **Quote at least one verbatim line per
   lens.** No anonymous synthesis, no paraphrase-only summaries.
3. **NEVER downgrade or omit a FAIL.** Any lens FAIL appears as an **unresolved blocker
   surfaced at the TOP.** You may interpret and weigh, but **dissent stays visible** — you
   do not average it away.
4. **Keep FAIL and N/A distinguishable.** A blocker must never be confused with an
   abstention.

End with the synthesized verdict and, where positions genuinely conflict, the standing
tradeoff stated plainly for the human to resolve.

> **In-process (ADI Tier 2) note.** When any lens returns FAIL, synthesize all lens
> findings into a single targeted, **attributed** refinement brief — e.g. *"Originality
> Critic: generic three-card hero. Craft Inspector: arbitrary card spacing (17px, 23px).
> Human Advocate: subtitle contrast fails WCAG AA."* This attributed brief IS the Tier 2
> output when the council is invoked in-process. (How ADI invokes this skill is Track 2 —
> not part of this skill's job.)

---

## Relationship to `/council`

Same orchestration shape — cold fan-out, debate-to-consensus, synthesized verdict with
recorded dissent and trust guardrails — but a **different bench and target class.**
`/council` reviews code/plans/ideas with six software-review lenses; `/design-council`
reviews **design targets** with seven design lenses, all seven mandatory, and never crawls
a repo. If someone invokes `/design-council` with a conversational reference, it routes to
`design-council-here`.
