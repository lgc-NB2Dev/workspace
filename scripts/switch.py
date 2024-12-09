import string
from typing import TYPE_CHECKING

from .utils import iter_modules, system

if TYPE_CHECKING:
    from subprocess import CompletedProcess


def main():
    for p in iter_modules():
        proc: CompletedProcess[str] = system(
            *("git", "branch"),
            capture_output=True,
            text=True,
            cwd=str(p),
        )
        branches = [x.strip(f"{string.whitespace}*") for x in proc.stdout.splitlines()]
        branches.sort(key=lambda x: 0 if x in {"master", "main"} else 1)
        branch_name = branches[0]
        system("git", "checkout", branch_name, cwd=str(p))
