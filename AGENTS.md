# AGENTS.md

## First

- For docs mainly for AI (like `AGENTS.md`), you MUST keep them concise and token efficient.
- Before editing a sub-project, check whether it has its own `AGENTS.md`. Sub-project `AGENTS.md` instructions override this file. Override: This workspace IS `lgc-NB2Dev/workspace`, skip sub-project working root check.

## Commands

```bash
uv sync -U  # install and update workspace dependencies

# test, type check, lint, format
poe test       # pytest
poe check      # basedpyright
poe lint       # ruff check
poe lint-fix   # ruff check --fix --unsafe-fixes
poe format     # ruff format && pnpm prettier -cw .

poe switch      # switch submodules to main/master
poe pull        # pull submodules and root workspace
poe up "optional message"  # commit and push submodules and root workspace
poe run         # run private/test-nb2 from the workspace root environment
poe docs-index  # regenerate NoneBot2 docs index
```

Type check, lint concurrently then format after your work done with any code change.

For workspace initialization, refer to `README.md`.

## Workspace Structure

- `external/`: External dependency projects.
  - `cookit/`: Project unrelated utility library.
- `plugins/`: NoneBot plugins under development. Simply `ls` it for a complete plugin list. It's token efficient rather than `rg`.
- `others/`: Plugin source code not related repos.
- `scripts/`: Workspace utility scripts.
- `typings/`: Type stubs for libraries that not have them.
- `private/`: Local private config and debug projects.
  - `test-nb2/`: NoneBot2 instance for plugin debugging.
  - `references/`: Local clone of reference repositories.

### Structure Rules

- Store temp/intermediate files in `temp/<category>/` at the project root. Skills can override this rule.

- `plugins/` MUST contain submodules only. Never clone a repo directly into `plugins/` — use `git submodule add`.

- Private plugins or repos (that should not be submodules) MUST be cloned into `private/` and added as a member of the private project.

## Workspace Rules

### NoneBot Docs

- Before touching NoneBot related code, check the docs for current APIs and code style.
- If you are not sure which NoneBot2 docs page to read, use `docs/nonebot2-docs-index.md`, or use tools like `rg` to search keywords.
- For code involving packages officially recommended in the NoneBot2 Best Practice docs, read the corresponding `best-practice/` page first and follow its guidance. This includes `nonebot-plugin-apscheduler`, `nonebot-plugin-localstore`, `nonebot-plugin-sentry`, `nonebot-plugin-htmlkit`, `nonebug`, `nonebot-plugin-alconna`, and `nonebot-plugin-orm`.
- Use `uv pip show nonebot2` to check the installed NoneBot2 version.
- Keep `private/references/nonebot2` as an up-to-date depth-1 clone of `https://github.com/nonebot/nonebot2`.
- Regenerate docs index after the local reference repo or installed NoneBot2 version changes: `poe docs-index`.

- Prefer Context7, WebSearch, GitHub readme for library/API documentation lookup first. Inspect installed package source code after docs are unavailable, insufficient, or clearly inconsistent with the local installed version. Feel free to make a depth-1 clone of source repo into `private/references/` for local inspection.

### Architecture

- Prefer aggressive refactors, active code cleanup, and bold structure/architecture changes; do not keep legacy compatibility by default unless the user explicitly asks. Tiny patches create spaghetti code.

- Consider `cookit` for broadly useful utilities/classes or duplicated logic across packages. For reuse within one package, put it in that package's `utils.py` or create one.
- Before adding a generic helper, decorator, formatter, async utility, data utility, compatibility wrapper, or Playwright/NoneBot helper, search `external/cookit/cookit` first.
- For code that needs to be compatible with both pydantic v1 and v2, prefer using `nonebot.compact` then `cookit.pyd.compat`.

### Environment

- Never run `uv sync`, `uv run`, or other dependency commands from inside `private/test-nb2` if they may create or update a nested virtual environment. To run the test project, activate or reuse the workspace root virtual environment first, then run `nb run` in `private/test-nb2`.

### Testing Rules

- Before implementing a feature or fixing a bug, ask user if we should use TDD first if not mentioned. If yes, invoke `tdd` skill before writing code.
- DO NOT import NoneBot plugin modules at test module top level. NoneBug tests that touch NoneBot plugins must load and import inside the test function. Put `from nonebot import require` inside the test, call `require("plugin_name")` for every plugin dependency needed by that test, then local-import the target module below those `require()` calls.
- Every testcase function should have a short description as its docstring.

### Preferred Libraries

- Prefer `RF-Tar-Railt/nonebot-plugin-waiter` for one-shot prompt-style interactive waits in NoneBot plugins. For docs, check its readme.

## Gotchas

ATTENTION: If you encounter a pitfall that might be reusable, you MUST record it in the corresponding `AGENTS.md` file as early as possible. (If there's no, copy one from `others/nonebot-plugin-template`.)

### NoneBot Plugin Loading

- Inside a NoneBot plugin, never directly import another NoneBot plugin module before loading it. Call `from nonebot import require` and `require("plugin_name")` first, then put imports depend on that plugin below the `require()` call. DO NOT use return value of `require()` as the imported module, it lacks type hints and documented as unrecommended operation.

- When importing a NoneBot plugin during local inspection, scripts, or tests loaded in `bot.py` style, initialize NoneBot first, then use `nonebot.load_plugin()` instead of importing the plugin module directly; see the NoneBot plugin loading docs for details.

### Testing

- When multiple pytest `conftest.py` files configure NoneBug `NONEBOT_INIT_KWARGS` in one workspace test run, merge with the existing stash value instead of replacing it, otherwise mixed-directory pytest runs can lose nonebot configs.

- Alconna/UniMessage helpers may need `current_bot`, `current_event`, and `current_state`; exercise them inside a matcher with `app.test_matcher()` and `ctx.receive_event()` instead of mocking context.

- Playwright tests require browser binaries. Run `uv run playwright install chromium` if Chromium is missing.

## Commit

Use English conventional commit messages:

```text
type(optional scope): description

- List of change descriptions, focus one point per row

Optional footer(s)
```
