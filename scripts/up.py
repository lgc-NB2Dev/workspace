from typing import TYPE_CHECKING, Union

from .utils import iter_modules, ok, system

if TYPE_CHECKING:
    from pathlib import Path
    from subprocess import CompletedProcess


def commit(cwd: Union[str, "Path", None] = None, **kwargs):
    return system("git", "commit", "-m", "up", cwd=cwd, **kwargs)


def up(cwd: Union[str, "Path", None] = None):
    status_p: CompletedProcess[bytes] = system(
        *("git", "status", "-s"),
        capture_output=True,
        cwd=cwd,
    )
    if status_p.stdout.strip():
        system("git", "add", ".", cwd=cwd)
        commit(cwd)

    branch_p: CompletedProcess[str] = system(
        *("git", "branch", "--show-current"),
        capture_output=True,
        text=True,
        cwd=cwd,
    )
    branch = branch_p.stdout.strip()
    log_p: CompletedProcess[str] = system(
        *("git", "log", f"origin/{branch}..{branch}"),
        capture_output=True,
        text=True,
        cwd=cwd,
    )
    if log_p.stdout.strip() and (not ok(system("git", "push", cwd=cwd, check=False))):
        system("git", "pull", cwd=cwd)
        system("git", "push", cwd=cwd)


def main():
    for p in iter_modules():
        up(p)
    up()
