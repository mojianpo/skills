# Writing Log Rules

The writing log is audit-only.

Allowed fields per entry:

- chapter identifier
- drafting timestamp
- mode used
- documents updated
- brief summary of each update
- whether temporary assumptions were used
- whether benchmark check ran
- failed benchmark items
- rewrite pass number
- third-pass cause summary
- whether a retrieval slice was used
- what forgotten-element action was taken
- what authenticity pass level ran
- whether post-authenticity mini recheck ran
- whether the chapter was in marathon mode
- whether the workflow auto-advanced to the next chapter
- whether the main fix was outline, character, pace, or theme related

Forbidden uses:

- do not treat the log as the source of continuity
- do not read it instead of `08-dynamic-state.md`
- do not store unresolved story truth only in the log

Recommended entry shape:

```markdown
## Chapter 12
- drafted_at: 2026-03-18 22:10
- mode: serialized
- benchmark_check_ran: yes
- failed_benchmark_items:
  - chapter 12 first draft: hook too weak, arc movement unclear
- rewrite_pass: 1
- retrieval_slice_used: yes
- forgotten_element_action: pressure reminder for missing brother line
- authenticity_pass_level: medium
- post_authenticity_mini_recheck_ran: yes
- marathon_mode: no
- auto_advanced_to_next_chapter: no
- primary_fix_origin: pace
- updated_files:
  - 08-dynamic-state.md: recorded betrayal, new debt, next chapter carryover
  - 06-foreshadow-ledger.md: planted ring clue
  - 07-chapter-roadmap.md: moved confrontation to chapter 14
- temporary_assumptions:
  - witness timeline left provisional
- third_pass_cause_summary:
  - not needed
```
