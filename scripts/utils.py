from pathlib import Path
from subprocess import CompletedProcess, run
from typing import Any

ROOT_PATH = Path(__file__).parent.parent
EXTERNAL_PATH = ROOT_PATH / "external"
PLUGINS_PATH = ROOT_PATH / "plugins"
OTHERS_PATH = ROOT_PATH / "others"


def system(*args: str, check: bool = True, **kwargs: Any):
    kwargs.setdefault("cwd", str(ROOT_PATH))
    r: CompletedProcess = run(args, check=check, **kwargs)  # noqa: S603
    return r.returncode


def iter_modules(tip: bool = True):
    for p in (
        *EXTERNAL_PATH.iterdir(),
        *PLUGINS_PATH.iterdir(),
        *OTHERS_PATH.iterdir(),
    ):
        if p.is_dir() and (p / ".git").exists():
            if tip:
                print(f"Entering {p.relative_to(ROOT_PATH)}")
            yield p


def iter_packages(tip: bool = True):
    for p in iter_modules(tip=False):
        if (p / "pyproject.toml").exists():
            if tip:
                print(f"Entering {p.relative_to(ROOT_PATH)}")
            yield p
