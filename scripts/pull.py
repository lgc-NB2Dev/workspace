from typing import TYPE_CHECKING

from .utils import iter_modules, ok, system, tip_entering

if TYPE_CHECKING:
    from pathlib import Path


def main():
    max_retry = 3

    paths = [*iter_modules(tip=False)]
    for i in range(1, max_retry + 1):
        if not paths:
            break
        if i > 1:
            print(f"Starting retry failed operations ({i} / {max_retry})")

        failed_paths: list[ Path] = []
        for p in paths:
            tip_entering(p)
            if not ok(system("git", "pull", cwd=str(p), check=False)):
                print("Pull failed, retry scheduled")
                failed_paths.append(p)

        paths = failed_paths

    else:
        print(f"Still have failed operations after {max_retry} tries, stopping")
        return

    system("git", "pull")
