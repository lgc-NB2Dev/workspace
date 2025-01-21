from typing import TYPE_CHECKING

from .utils import iter_modules, ok, system, tip_entering

if TYPE_CHECKING:
    from pathlib import Path


def main():
    paths = [*iter_modules(tip=False)]
    while paths:
        failed_paths: list[Path] = []

        for p in paths:
            tip_entering(p)
            if not ok(system("git", "pull", cwd=str(p), check=False)):
                print("Pull failed, retry scheduled")
                failed_paths.append(p)

        paths = failed_paths
        if paths:
            print("Starting retry failed operations")

    system("git", "pull")
