from pathlib import Path
from subprocess import run
from typing import Any

ROOT_PATH = Path(__file__).parent.parent
PACKAGES_PATH = ROOT_PATH / "packages"
OTHERS_PATH = ROOT_PATH / "others"


def system(*args: str, **kwargs: Any):
    kwargs.setdefault("cwd", str(ROOT_PATH))
    r = run(args, **kwargs)  # noqa: S603
    return r.returncode


def system_no_fail(*args: str, **kwargs: Any):
    c = system(*args, **kwargs)
    if c:
        raise RuntimeError(f"command {args} failed with code {c}")


def iter_packages():
    for p in (*PACKAGES_PATH.iterdir(), *OTHERS_PATH.iterdir()):
        if p.is_dir() and (p / "pyproject.toml").exists():
            yield p
