# Bootstrap And Marathon Handoff

Use this reference only when:

- starting a new novel project
- preparing crazy-writing or auto-continuation handoff

## Startup checklist

1. Create the standard project files first.
2. Read `assets/codex-continue-novel.ps1`.
3. Replace `__PROJECT_ROOT__` with the actual absolute project root.
4. On Windows, write the result to `codex-continue-novel.ps1` in the project root as `UTF-8 with BOM`, not `UTF-8 without BOM`.
5. Preserve the template's UTF-8 console setup and explicit UTF-8 log writing.
6. Verify that `codex-continue-novel.ps1` exists in the project root.
7. Verify that the written script no longer contains `__PROJECT_ROOT__`.
8. Record the launch command in the handoff wording:

```powershell
powershell -ExecutionPolicy Bypass -File .\codex-continue-novel.ps1
```

## Handoff checklist

1. Confirm the outline and cast dossier are already approved.
2. Confirm the root runner script exists and is current.
3. Tell the user to close the current session.
4. Tell the user to run:

```powershell
powershell -ExecutionPolicy Bypass -File .\codex-continue-novel.ps1
```

5. Tell the user that `Ctrl+C` stops the looping runner.
6. If automatic bootstrap or automatic startup was blocked, say so plainly and present the same command as the manual fallback.

## Example

Example startup handoff:

- project root: `D:\novels\qing-ye-ji`
- action: write `D:\novels\qing-ye-ji\codex-continue-novel.ps1` from the template, replacing only `__PROJECT_ROOT__`, and keep the file as `UTF-8 with BOM`
- user-facing handoff: `关闭当前会话后，在项目根目录运行 powershell -ExecutionPolicy Bypass -File .\codex-continue-novel.ps1`

Example marathon handoff:

- user request: `开启疯狂写作`
- required response: confirm the runner script exists, tell the user to close the current session, then present the exact command block without paraphrasing it away
