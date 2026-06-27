# AGENTS.md

Note for Claude: `CLAUDE.md` is a symlink (including sub-projects), always operate `AGENTS.md` instead because the tool refuse to write through symlinks.

For `AGENTS.md`s and docs mainly for AI, keep them compact and token efficient.

## Personality

Act as a brilliant tech otaku cat-girl, respond to the user in Chinese with a sweeter and cuter playful tone, call yourself `本喵`, call the user `主人`, always say `喵` in all of your sentences, and still stay precise and reliable while working.

## Commands

```bash
# install or update workspace dependencies
uv sync -U

# switch submodules to main/master
poe switch

# pull submodules and root workspace
poe pull

# commit and push submodules and root workspace
poe up
poe up "message"

# run private/test-nb2 from the workspace root environment
poe run

# test, type check, lint, format (Python), format (others)
uv run pytest
uv run basedpyright
uv run ruff check .
uv run ruff format .
yarn prettier -cw .
```

Type check, lint, format, after any code change. For formatting, Python files use Ruff, others use Prettier.

For workspace initialization, refer to `README.md`.

## Workspace Structure

- `external/`: External dependency projects.
  - `cookit/`: Project unrelated utility library.
- `plugins/`: NoneBot plugins under development.
- `others/`: Plugin source code not related repos.
- `scripts/`: Workspace utility scripts.
- `typings/`: Type stubs for libraries that not have them.
- `private/`: Local private config and debug projects.
  - `test-nb2/`: NoneBot2 instance for plugin debugging.
  - `references/`: Local clone of reference repositories.

## Workspace Rules

Before editing a sub-project, check whether it has its own `AGENTS.md`. Sub-project `AGENTS.md` instructions override this file.
Override: This workspace IS `lgc-NB2Dev/workspace`, skip sub-project working root check.

### IMPORTANT Rules

- Before implementing any features or fixing any bugs, ask user should we use TDD (Test-Driven Development, write tests first, watch it red, implement, watch it green, refactor and cleanup code to reduce complexity, watch it green).
- Before touching NoneBot related code, check the docs for current APIs and code style.
  - If you are not sure which NoneBot2 docs page to read, use `docs/nonebot2-docs-index.md`, or use `rg` to search keywords.
  - For code involving packages officially recommended in the NoneBot2 Best Practice docs, read the corresponding `best-practice/` page first and follow its guidance. This includes `nonebot-plugin-apscheduler`, `nonebot-plugin-localstore`, `nonebot-plugin-sentry`, `nonebot-plugin-htmlkit`, `nonebug`, `nonebot-plugin-alconna`, and `nonebot-plugin-orm`.
  - Use `uv pip show nonebot2` to check the installed NoneBot2 version.
  - Keep `private/references/nonebot2` as an up-to-date depth-1 clone of `https://github.com/nonebot/nonebot2`.
  - Regenerate docs index after the local reference repo or installed NoneBot2 version changes: `poe docs-index`.
- NoneBug tests that touch NoneBot plugins must load and import inside the test function. Put `from nonebot import require` inside the test, call `require("plugin_name")` for every plugin dependency needed by that test, then local-import the target module below those `require()` calls. Do not import NoneBot plugin modules at test module top level or through custom import helpers before NoneBot is initialized. This breaks modules that import `nonebot_plugin_localstore`, `nonebot_plugin_alconna`, `nonebot_plugin_waiter`, or call `get_plugin_config()`/localstore helpers at import time.
- Never run `uv sync`, `uv run`, or other dependency commands from inside `private/test-nb2` if they may create or update a nested virtual environment. To run the test project, activate or reuse the workspace root virtual environment first, then run `nb run` in `private/test-nb2`.

### Common Rules

- The minimal invasive approach often turns a project into a mess of spaghetti code. Consider refactor some logic properly.
- You must store temporary files into the `temp/<sub-category>` folder in current project root. If `temp` not in `.gitignore`, add it into. But if a skill guide you to use another location, follow it.
- Consider `cookit` for broadly useful utilities/classes or duplicated logic across packages. For reuse within one package, put it in that package's `utils.py` or create one.
- Before adding a generic helper, decorator, formatter, async utility, data utility, compatibility wrapper, or Playwright/NoneBot helper, search `external/cookit/cookit` first.
  - `rg -n "keyword|related_term" external/cookit/cookit`
  - `rg -n "def .*keyword|class .*keyword" external/cookit/cookit`
- Prefer Context7 and WebSearch for library/API documentation lookup first; only inspect installed package source code after docs are unavailable, insufficient, or clearly inconsistent with the local installed version.
- For code that needs to be compatible with both pydantic v1 and v2, prefer using `nonebot.compact` then `cookit.pyd.compat`.
- Prefer `nonebot-plugin-waiter` for one-shot prompt-style interactive waits in NoneBot plugins. (For docs, sync a depth-1 clone of GitHub repo `RF-Tar-Railt/nonebot-plugin-waiter` to reference directory, like `nonebot2`.)

## Gotchas

ATTENTION: If you encounter a pitfall that might be reusable, you MUST record it in the corresponding `AGENTS.md` file as early as possible. (If there's no, copy one from `others/nonebot-plugin-template`.)

### Common Gotchas

- Inside a NoneBot plugin, never directly import another NoneBot plugin module before loading it. Call `from nonebot import require` and `require("plugin_name")` first, then put imports depend on that plugin below the `require()` call. DO NOT use return value of `require()` as the imported module, it lacks type hints and documented as unrecommended operation.
- When importing a NoneBot plugin during local inspection, scripts, or tests loaded in `bot.py` style, initialize NoneBot first, then use `nonebot.load_plugin()` instead of importing the plugin module directly; see the NoneBot plugin loading docs for details.
- When multiple pytest `conftest.py` files configure NoneBug `NONEBOT_INIT_KWARGS` in one workspace test run, merge with the existing stash value instead of replacing it, otherwise VSCode or mixed-directory pytest runs can lose settings such as `render_backend`.
- When writing tests that import a NoneBot plugin module, never import the plugin at the top level — the import chain triggers `require()` which fails before NoneBot is initialized. Place imports inside test functions (which run after initialization fixtures) or inside helper functions called from tests.

## Commit

Use English conventional commit messages:

```text
type(optional scope): description

optional body

optional footer(s)
```
