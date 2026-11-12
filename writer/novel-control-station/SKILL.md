---
name: novel-control-station
description: Use when writing, planning, continuing, repairing, revising, or running marathon/"疯狂写作"/auto continuation mode for Chinese long-form fiction with recurring characters, multiple plotlines, persistent world rules, chapter-by-chapter continuity needs, or style-specific constraints.
---

# Novel Control Station

## Overview

Run fiction projects like a controlled long-form system, not a one-shot prompt. Align the novel first, store project truth in standard files, drive each chapter from those files, and update dynamic state after every chapter. When density rises, add a lightweight secondary control view for recall, line heat, and graph-style interference checks without replacing the core files.

## When to Use

- Starting a new novel project
- Continuing a serialized story
- Repairing setting drift, character distortion, or dropped relationships
- Rebuilding plotlines, foreshadowing, or chapter plans
- Switching between serialized drafting and publication-oriented revision
- Writing fiction that needs controlled style modules such as suspense, humor, romance, literary depth, horror, fantasy, or mystery

Do not use this skill for one-off poems, short jokes, or isolated scenes that do not need persistent continuity.

## Hard Rules

- Unless the user explicitly requests another language, all planning artifacts, control documents, and fiction output must be written in Chinese. Default to simplified Chinese.
- Do not begin formal novel design until the main plot direction, core character tension, and ending direction are aligned.
- Do not let a full outline stand if benchmark outline checks still show slogan themes, flat characters, weak line interference, or hollow ending direction.
- Do not start chapter drafting before presenting the full outline and full cast dossier.
- Do not draft a chapter before reading the required project files.
- Do not treat a single flat plot as sufficient when the user wants a long-form novel. Default to multiple active lines.
- Do not let trope convenience, fake depth, or decorative structure override human truth, causal pressure, or social texture.
- Do not treat benchmark logic as doctrine. Use it as a calibrated reference system that must adapt to user intent, genre, and target readership.
- Do not copy a sample work's signature setup, role shell, twist engine, scene pattern, or language texture.
- Do not treat marathon mode as permission to skip chapter control, rewrite escalation, dynamic updates, or logging.
- Do not let a secondary graph, recall map, or scratch index override the standard project files. Derived control views are support systems only.
- Do not satisfy forgotten-element checks with token cameos, cosmetic mentions, or checklist references. Re-entry must change pressure, debt, or expectation.
- Do not run de-AI cleanup as blind flattening. Preserve genre register, era texture, narrator stance, and character voice.
- Do not let narration or interiority slide into review copy, theory-heavy explanation, or industry jargon unless the point of view, profession, era, or setting truly requires that diction.
- Do not keep specialist terms, abstract analysis words, or institutional jargon when ordinary readers would lose the thread and the same story work can be done through action, consequence, or scene context.
- Default paragraph mode to `web-serial-natural` unless `09-style-guide.md` or the current chapter control card explicitly switches to `long-paragraph`.
- Do not let chapter prose fake intensity with decorative blank space. Under `web-serial-natural`, narrative paragraphs usually hold `2-4` sentences; single-sentence narrative paragraphs are for emphasis, reveal, shock, cut, or hook and should not chain by habit.
- Do not split one speaker's continuous beat into multiple paragraphs unless interruption, stage movement, or a pressure turn truly changes the beat.
- Do not force scene ladders into rigid formula when the chapter needs looser movement. Use scene control to preserve pressure, not to fake architecture.
- Do not use chapter titles as spoiler summaries, empty riddles, or decorative labels detached from chapter pressure.
- If the project uses chapter titles, lock a naming system at project level and keep title voice consistent unless the book is intentionally entering a new phase.
- If information is missing or contradictory, explain the risk and let the user choose whether to refine details or draft directly.
- If drafting proceeds with assumptions, record them in the dynamic state file.
- After every chapter, update dynamic state before moving on.
- The writing log is audit-only. Never use it as story truth.

## Standard Files

Maintain these files for every novel project:

- `00-project-overview.md`
- `01-theme-and-proposition.md`
- `02-worldbuilding.md`
- `03-cast-bible.md`
- `04-relationship-map.md`
- `05-main-plotlines.md`
- `06-foreshadow-ledger.md`
- `07-chapter-roadmap.md`
- `08-dynamic-state.md`
- `09-style-guide.md`
- `chapters/`
- `control-cards/`
- `logs/writing-log.md`

Directory rules:

- store accepted chapter manuscripts in `chapters/`
- store one persisted chapter control card per accepted chapter in `control-cards/`
- default file naming:
  - `chapters/NN-<chapter-title>.md`
  - `control-cards/NN-<chapter-title>-control-card.md`
- if chapters are numbered-only, replace `<chapter-title>` with a short chapter slug rather than leaving filenames blank

Read [document-templates.md](references/document-templates.md) when creating or restoring these files.

## Startup Project Bootstrap

When starting a new novel project, treat the project root as an operational control surface, not just a folder that stores markdown files.

After creating the standard files, also create:

- `codex-continue-novel.ps1` in the project root

This script is the looping continuation entry point for marathon mode. It should be ready before the project leaves startup.
Use the exact template in [assets/codex-continue-novel.ps1](assets/codex-continue-novel.ps1) and replace only the project root placeholder before writing the file into the project root.
Read [bootstrap-and-marathon-handoff.md](references/bootstrap-and-marathon-handoff.md) when starting a project or handing off into marathon mode.

Bootstrap rules:

- create `codex-continue-novel.ps1` in the project root whenever a new project is initialized
- build the file from `assets/codex-continue-novel.ps1`
- replace only the project root placeholder with the actual project root
- on Windows, write the root script as `UTF-8 with BOM`; `UTF-8 without BOM` can misread Chinese literals under `powershell.exe`
- preserve the template's UTF-8 console setup and explicit UTF-8 log writing when repairing the runner
- repair stale scripts by rebuilding from the template instead of creating a second variant
- verify the root script exists and the placeholder is gone before marathon handoff
- if automatic file creation is blocked, tell the user that startup could not finish automatically and instruct them to create or copy the script manually before marathon handoff
- do not assume the user will remember the launch command later; record the exact command during handoff

## Secondary Control View

When cast density, plotline interference, or foreshadow volume makes linear rereading too blunt, load [graph-and-recall-control.md](references/graph-and-recall-control.md).

Use it to:

- translate current canon into a temporary node-and-edge control view
- prepare a short retrieval slice for the next chapter instead of rereading blindly
- detect relation jumps, cold lines, unsupported payoffs, and world-rule drift
- route return pressure for characters, plotlines, relationships, and foreshadowing

This layer is derived from the standard files and `08-dynamic-state.md`.

It may be kept as scratch notes or an optional sidecar, but:

- canonical repair always happens in the standard files first
- no new permanent truth source is required
- any conflict between the secondary view and the standard files is resolved in favor of the standard files

## Foundational Canon Loading

At project launch, major revision, and high-level review, read:

- [foundational-literary-principles.md](references/foundational-literary-principles.md)
- [critical-evaluation-standards.md](references/critical-evaluation-standards.md)
- [epoch-and-people-resonance.md](references/epoch-and-people-resonance.md)
- [reader-retention-and-ai-failure-modes.md](references/reader-retention-and-ai-failure-modes.md)

Use them to convert abstract craft into project truth inside:

- `01-theme-and-proposition.md`
- `02-worldbuilding.md`
- `03-cast-bible.md`
- `05-main-plotlines.md`
- `09-style-guide.md`

Do not leave these readings as commentary. Turn them into enforceable constraints on:

- character desire, fear, shame, debt, and contradiction
- causal line pressure
- point-of-view and form choices
- image and language discipline
- social, institutional, or era pressure
- ending residue and thematic cost

Use [research-source-notes.md](references/research-source-notes.md) only when provenance or source refresh is needed.

## Benchmark Rule Loading

At project launch, outline design, and chapter review, read:

- [popular-fiction-common-laws.md](references/popular-fiction-common-laws.md)
- [genre-benchmark-rules.md](references/genre-benchmark-rules.md)
- [benchmark-trigger-matrix.md](references/benchmark-trigger-matrix.md)

Use them to determine:

- the active benchmark rule group
- whether the project targets heat, reputation, or dual-high balance
- which pace-intensity checks stay hard and which are dynamically down-weighted
- which originality and compliance alarms must stay active

Use [benchmark-source-trace.md](references/benchmark-source-trace.md) only when source provenance matters.

## Execution Method Loading

Load these references only when their stage is active:

- [interview-and-handoff-flow.md](references/interview-and-handoff-flow.md)
- [character-construction-methods.md](references/character-construction-methods.md)
- [graph-and-recall-control.md](references/graph-and-recall-control.md)
- [dialogue-writing-rules.md](references/dialogue-writing-rules.md)
- [suspense-and-reveal-design.md](references/suspense-and-reveal-design.md)
- [chapter-architecture-rules.md](references/chapter-architecture-rules.md)
- [chapter-title-method.md](references/chapter-title-method.md)
- [scene-execution-patterns.md](references/scene-execution-patterns.md)
- [forgotten-elements-and-line-heat.md](references/forgotten-elements-and-line-heat.md)
- [authenticity-and-de-ai-pass.md](references/authenticity-and-de-ai-pass.md)
- [continuity-and-marathon-mode.md](references/continuity-and-marathon-mode.md)

Do not read every chapter-stage reference by default. Route only to the references whose pressure is actually active.

Stage routing:

- startup interview and approval handoff:
  - `interview-and-handoff-flow.md`
  - `character-construction-methods.md`
- outline and roadmap design:
  - `graph-and-recall-control.md`
  - `chapter-architecture-rules.md`
  - `chapter-title-method.md`
  - `character-construction-methods.md`
  - `scene-execution-patterns.md`
- chapter drafting and revision:
  - always load `chapter-architecture-rules.md`
  - load `chapter-title-method.md` when the project uses titled chapters or title finalization is active
  - load `graph-and-recall-control.md` when recurrence density, cast rotation, or interference pressure is high
  - load `dialogue-writing-rules.md` when dialogue is carrying pressure
  - load `suspense-and-reveal-design.md` when concealment or reveal fairness is active
  - load `scene-execution-patterns.md` when chapter mission is too broad for a single-pass draft
  - load `forgotten-elements-and-line-heat.md` when serialized recurrence risk is meaningful
  - load `authenticity-and-de-ai-pass.md` after a structurally acceptable draft exists
  - load `continuity-and-marathon-mode.md` when continuing long fiction or operating in marathon mode

## Startup Interview Flow

Run the startup flow using [interview-and-handoff-flow.md](references/interview-and-handoff-flow.md) and [character-construction-methods.md](references/character-construction-methods.md).

Ask one focused question at a time.

Core questions first:

1. Positioning
   - genre, audience, scale, release mode, primary promise, social or era pressure
2. Characters
   - protagonist setup, protagonist core personality, core cast pressure
3. Scale
   - target length, whether the project is multi-line, expected density
4. Ending Direction
   - emotional destination, cost, likely shape of the ending
5. Style And Market Mode
   - primary style, support style, style balance target, support style boundary, target mode, tolerance for slow-burn, default style intensity, paragraph mode, chapter title mode, internalized strengths to absorb, forbidden habits, pseudo-style drift, jargon ceiling, and any professional, historical, or setting terms that must remain legible

Language default:

- keep the project in Chinese unless the user explicitly requests another language
- ask only when needed whether the user wants modern vernacular, historical Chinese texture, web-serial diction, or publication-oriented prose
- unless a publication-oriented or literary long-paragraph preference is explicit, keep the default paragraph mode at `web-serial-natural`
- when diction risk is meaningful, write into `09-style-guide.md`:
  - style balance target and the strengths to absorb from mature works
  - support style boundary and the chapter-level style intensity range
  - paragraph mode, chapter-level override policy, and allowed short-paragraph triggers
  - pseudo-style drift to avoid for each active style
  - banned AI shell phrases or sentence habits
  - jargon ceiling for narration and dialogue
  - any necessary professional, historical, or setting terms that must survive authenticity cleanup

Then derive more questions from the answers:

- suspense or mystery:
  - hidden truth, clue fairness, reveal ladder
- historical:
  - era pressure, institutions, power chain
- long-form or multi-line:
  - line count, line interference, stage arcs, convergence and finish logic
- strong protagonist personality:
  - stress response, blind spots, speech signature
- romance or high-relationship pressure:
  - emotional debt, relational obstacle, intimacy risk
- style-sensitive projects:
  - narration distance, prose density, paragraph mode, how often strike paragraphs are allowed, which strengths should stay active across the whole book, how strong the style should usually run, and which pseudo-style drifts must stay off-limits

Do not ask a fixed questionnaire when the project does not need it. Derive only what the current answers make necessary.

Do not move into full design until character pressure, multi-line logic where needed, and ending direction are aligned enough to prevent blind drafting.

## Outline Benchmark Check

Before a full outline is accepted or a chapter roadmap is locked, read [chapter-architecture-rules.md](references/chapter-architecture-rules.md) and run an outline benchmark check.

Confirm all of these:

- theme is dramatized through choices, not slogans
- protagonist and core cast have desire, obstacle, price, and arc direction
- multiple lines interfere rather than float in parallel
- major characters, plotlines, and foreshadows have visible return logic rather than blind disappearance windows
- the selected genre's benchmark promise is visible
- the ending direction can produce both closure and residue

If the outline benchmark check fails:

- repair the outline first
- update the project files
- do not proceed to chapter drafting

## Outline And Cast Handoff

After interview alignment and before chapter drafting:

- present the full outline
- present the full cast dossier

The cast dossier must make visible:

- role
- core personality
- visible goal
- inner lack
- key relationships
- contradiction
- arc direction
- speech signature

The outline must make visible:

- the global promise
- main and support lines
- core conflicts
- stage progression
- key turns
- ending direction

Do not start chapters before this handoff is complete.

## Direct-Edit Branch

After outline and cast handoff, the user may choose direct-edit revision.

If the user gives changes:

- edit the current outline and cast dossier directly
- preserve already aligned material unless the new change conflicts with it
- show the repaired version

Do not restart the whole interview unless the user asks for a real reset.

## Missing Information Branch

When files or user input leave gaps:

1. List the missing, conflicting, or risky items.
2. Explain what each issue threatens.
3. Offer exactly two branches:
   - `refine details`
   - `draft directly`

If the user chooses `draft directly`:

- make the smallest safe assumption
- flag it as temporary
- record it in `08-dynamic-state.md` under pending confirmation

## Paragraph Mode Control

Record paragraph control in `09-style-guide.md` and inherit it into each chapter control card.

Modes:

- `web-serial-natural`
  - default mode for chapter prose
  - narrative paragraphs usually run `2-4` sentences
  - single-sentence narrative paragraphs are reserved for reveal, impact, pressure cut, emotional stall, or hook
  - one speaker's dialogue, attached action, and short follow-up should stay in one paragraph unless the beat truly changes
- `long-paragraph`
  - use when the project or chapter explicitly needs more continuous interiority, essay-like flow, or publication-oriented long paragraphs
  - allow longer narrative blocks, but still break on speaker change, point-of-view shift, scene/time jump, or major pressure turn
  - do not turn continuity into inert exposition walls

Override rules:

- the project default comes from `09-style-guide.md`
- the current chapter may override only when the chapter control card records the reason and the intended pace or voice effect
- after drafting and after the authenticity pass, confirm the accepted chapter still matches the selected paragraph mode

## Chapter Title Control

Read [chapter-title-method.md](references/chapter-title-method.md) when the project uses chapter titles, when the user asks for named chapters, or when a numbered-only chapter system may need to change.

Rules:

- chapter titles are optional; plain numbering is valid when speed, invisibility, or relentless forward pull serves the book better
- if the project uses chapter titles, lock one naming system in `00-project-overview.md`, `07-chapter-roadmap.md`, and `09-style-guide.md`
- each title should carry one primary job and at most one secondary job: hook, focus, orientation, motif return, or voice signal
- generate `3-5` candidate titles from the chapter control card, then choose a working title before drafting
- do not use chapter titles as blunt summaries, spoiler labels, fake-poetic fog, or generic serial filler
- after the chapter passes structure and authenticity checks, run a final title-fit recheck and replace the working title if the chapter's true center moved

## Chapter Workflow

For every chapter, use this order:

1. If the project is newly launching, structurally redirecting, or under high-level review, read the foundational canon files first.
2. Read required files:
   - `00-project-overview.md`
   - `03-cast-bible.md`
   - `05-main-plotlines.md`
   - `06-foreshadow-ledger.md`
   - `07-chapter-roadmap.md`
   - `08-dynamic-state.md`
   - `09-style-guide.md`
3. If the project has dense recurrence, large cast rotation, or multiple active interference lines, prepare a retrieval slice using [graph-and-recall-control.md](references/graph-and-recall-control.md).
   - pull only the chapter-relevant characters, relationships, plotlines, foreshadows, world rules, and debts
   - track what is hot, what is running cold, and what cannot be forgotten here
4. Read only the selected internal style module documents needed for this chapter.
   - use `09-style-guide.md` to identify style balance target, internalized strengths, support style boundary, preferred intensity range, and pseudo-style drift before loading modules
   - read the relevant internal style modules from [style-modules/index.md](references/style-modules/index.md)
   - read each selected module's `core.md` first
   - drill into deeper style documents only if the chapter needs them
5. Read only the execution-method references needed for this chapter.
   - always read `chapter-architecture-rules.md`
   - read `chapter-title-method.md` if the project uses chapter titles or if title finalization is active
   - read `graph-and-recall-control.md` if a retrieval slice was needed
   - read `dialogue-writing-rules.md` if dialogue pressure is central
   - read `suspense-and-reveal-design.md` if suspense or reveal work is active
   - read `scene-execution-patterns.md` if the chapter needs multi-unit structural control
   - read `forgotten-elements-and-line-heat.md` if recurrence management matters
   - read `continuity-and-marathon-mode.md` when continuing or auto-advancing
   - read `authenticity-and-de-ai-pass.md` only after a structurally acceptable draft exists
6. Scan for:
   - setting conflicts
   - character drift
   - broken relationship continuity
   - forgotten emotional debt
   - overdue recurring characters or relationships
   - cold plotlines that need touch, echo, or justified dormancy
   - dropped foreshadowing
   - unsupported payoff windows
   - plotline neglect
   - world-rule memory gaps
   - trope convenience overriding human truth
   - lost social or era pressure
   - generic AI shells, false-summary sentences, or over-neat contrast patterns
   - analysis-tone drift, platform-copy drift, or unexplained specialist jargon
   - paragraph-mode drift such as decorative blank lines, same-speaker over-splitting, or one-sentence paragraph chains with no pressure reason
7. Generate a chapter control card using [chapter-control-card.md](references/chapter-control-card.md).
   - record style intensity, paragraph mode, active style drivers, intended payoff, and pseudo-style drift when style pressure is meaningful
   - write the card to `control-cards/NN-<chapter-title>-control-card.md`; if the title is not final yet, use a stable working slug and rename after the final title check
8. If the project uses chapter titles, generate `3-5` candidate titles using [chapter-title-method.md](references/chapter-title-method.md).
   - choose a working title that matches the project's naming system
   - record the working title in the chapter control card and `07-chapter-roadmap.md`
9. If the risk scan is serious, use the missing information branch.
10. Draft the chapter from the control card.
   - when the chapter needs tighter control, write scene by scene or pressure unit by pressure unit using [scene-execution-patterns.md](references/scene-execution-patterns.md)
   - inherit paragraph mode from `09-style-guide.md` unless the control card records a chapter-specific override
   - under `web-serial-natural`, keep most narrative paragraphs at `2-4` sentences and avoid chaining single-sentence narrative paragraphs unless the scene is deliberately striking beats
   - keep one speaker's continuous beat, attached action, and short follow-up in the same paragraph unless the pressure or stage movement changes
   - use paragraph breaks for speaker change, scene/time or point-of-view shift, and real pressure turns rather than decorative emptiness
   - store the accepted chapter manuscript in `chapters/NN-<chapter-title>.md`
11. Run the chapter benchmark check.
12. If the benchmark check fails, apply rewrite escalation before accepting the chapter.
13. Run the authenticity pass using [authenticity-and-de-ai-pass.md](references/authenticity-and-de-ai-pass.md).
   - strip generic AI patterns, false depth, and abstract summaries first
   - cut or translate over-professionalized diction unless the project genuinely needs the term
   - then restore concrete detail, rhythm variation, and project-specific voice
14. Run a post-authenticity mini recheck.
   - confirm continuity facts still hold
   - confirm character voice and relationship pressure did not flatten or drift
   - confirm hook, closure, and residue still function
   - confirm paragraphing still matches the active paragraph mode and is not leaning on decorative blank space
   - confirm readability did not drop behind unnecessary jargon
   - confirm required professional, era, or setting terms were not accidentally removed
15. If the project uses chapter titles, run the final title check.
   - confirm the title still matches the accepted chapter's mission, turn, residue, and voice
   - replace the working title if the chapter changed its center during drafting
16. Review the chapter for continuity, style integrity, thematic pressure, critical standards, and whether return-pressure handling stayed causal rather than token.
17. Update dynamic and structural files.
   - keep `chapters/` and `control-cards/` aligned with the accepted chapter title and number
18. Record the chapter and file updates in the writing log.

## Chapter Benchmark Check
Read [quality-and-writeback-checks.md](references/quality-and-writeback-checks.md) and [reader-retention-and-ai-failure-modes.md](references/reader-retention-and-ai-failure-modes.md) before accepting a chapter.
Hard gates:
- character, logic, theme, and originality stay hard gates even in slow-burn or restrained modes
- reject flat procedural prose, benchmark cosplay, unsupported payoffs, and dialogue without pressure
- keep protagonist voice, local closure, and carryover debt legible in the accepted chapter

## Forgotten Element Control

When the project is long, dense, or heavily serialized, run [forgotten-elements-and-line-heat.md](references/forgotten-elements-and-line-heat.md) during planning and review.

Possible outcomes:

- direct advance
- pressure reminder
- justified dormancy note
- closure or archive

Never solve this check with token cameos, random reminders, or fake callbacks that do not alter pressure.

## Authenticity Pass

After structure and benchmark logic are acceptable, run [authenticity-and-de-ai-pass.md](references/authenticity-and-de-ai-pass.md).

Use a fixed three-part order:

1. remove generic AI habits, false depth, abstract summaries, empty conclusions, and textureless filler
2. cut or translate over-specialized diction, analysis-language drift, and reader-hostile jargon unless the point of view or setting genuinely needs the term
3. restore concrete detail, rhythm variation, speaker distinction, and project-specific voice

Before or during this pass, read `09-style-guide.md` for:

- banned AI shell phrases or phrasing habits
- paragraph mode and allowed short-paragraph triggers
- jargon ceiling for narration and dialogue
- professional, historical, or setting terms that must remain

If the novel intentionally uses literary density, historical register, formal narration, or stylized speech, clean genericity without flattening the chosen mode.

After medium or aggressive authenticity edits, always run a light post-pass recheck on:

- continuity facts
- character voice
- relationship pressure
- hook and closure integrity
- ordinary-reader legibility
- required terminology that should still remain

## Rewrite Escalation

If the chapter benchmark check fails:

1. first failure:
   - rewrite the full chapter by the issue list
2. second failure:
   - rewrite only the failed dimensions with tighter control
3. third failure:
   - stop blind whole-chapter rewriting
   - summarize failing items
   - summarize likely root causes
   - state whether the fix belongs in outline, character design, pacing, or theme-bearing structure
   - revise by cause instead of retrying randomly

## Marathon Mode

Marathon mode begins only after the user approves the current outline and cast dossier.

If the user asks for crazy writing, nonstop continuation, auto continuation, or marathon-style hands-off drafting:

- load [bootstrap-and-marathon-handoff.md](references/bootstrap-and-marathon-handoff.md)
- ensure `codex-continue-novel.ps1` exists in the project root before handoff
- create or repair the script from `assets/codex-continue-novel.ps1` first if it is missing or stale
- tell the user to close the current session
- then tell the user to run this command from the project root:

```powershell
powershell -ExecutionPolicy Bypass -File .\codex-continue-novel.ps1
```

- tell the user that `Ctrl+C` stops the looping runner
- if automatic startup is blocked for any reason, explicitly present the same command as the manual fallback instead of describing the process vaguely

In marathon mode:

- do not ask the user again chapter by chapter
- do keep every internal control step active

For each chapter, still do:

- required file reads
- retrieval slice preparation when density requires it
- chapter control card
- working title generation and final title recheck when titled chapters are active
- selected style module loading
- forgotten-element and line-heat scan
- benchmark and continuity checks
- rewrite escalation when needed
- authenticity pass
- post-authenticity mini recheck
- dynamic-state update
- structural file repair
- writing-log entry

Continue automatically to the next chapter only after the current chapter is accepted and written back into project files.

Stop marathon mode only when the approved outline has naturally concluded:

- main lines are resolved
- support lines are closed or intentionally left with justified residue
- major debts are paid or transformed
- ending direction is fulfilled

Do not stop because a fixed chapter count or word target was reached.

## Dynamic Update Rules
Read [quality-and-writeback-checks.md](references/quality-and-writeback-checks.md) for the full writeback checklist.
After every accepted chapter:
- update `08-dynamic-state.md` using [dynamic-state-template.md](references/dynamic-state-template.md)
- update changed canonical files in `03/04/05/06/07/02` as needed
- if chapter titles are active, make sure the locked chapter title in `07-chapter-roadmap.md` still matches the accepted chapter
- sync optional secondary control notes only after canonical files are current
- apply the logging rules in [logging-rules.md](references/logging-rules.md)

## Style Module Loading

The control station contains internal style modules and loads them on demand.

At project start:

- ask for 1 or 2 primary styles
- ask for at most 1 support style
- record style balance target and the strengths to absorb from mature works
- define support style boundary, preferred style intensity range, and pseudo-style drift to avoid
- record forbidden style modes

At chapter time:

- route style loading through [style-modules/index.md](references/style-modules/index.md)
- use `09-style-guide.md` to decide which strengths are active in this chapter and how hard the style should run
- load only the selected internal module `core.md` files first
- load deeper module documents only if the chapter needs them
- write the chosen style pressures, active style drivers, payoff focus, and pseudo-style drift into the chapter control card

Available internal modules:

- humor
- suspense
- mystery
- romance
- horror
- fantasy
- literary

## Review And Writeback Detail

Read [quality-and-writeback-checks.md](references/quality-and-writeback-checks.md) when applying adaptive weighting, originality discipline, chapter quality gates, final writeback, or common-failure review.
