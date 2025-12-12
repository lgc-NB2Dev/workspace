import asyncio
from pathlib import Path

from .utils import (
    BaseAsyncTask,
    handle_interrupt,
    make_workspace_task_runner,
    proc_exec,
    task,
)


@task()
async def switch(self: BaseAsyncTask, path: Path):
    res = await proc_exec(
        *("git", "branch", "--format", "%(HEAD),%(refname:short)"),
        cwd=path,
    )
    branches_raw = res.stdout.strip().splitlines()
    current_branch = None
    branches = []
    for line in branches_raw:
        head, name = line.split(",", 1)
        branches.append(name)
        if head == "*":
            current_branch = name

    target_branch = next((t for t in ("main", "master") if t in branches), None)
    if target_branch is None:
        target_branch = branches[0]
        self.print(
            f"No `main` or `master` branch found, selecting first branch `{target_branch}`",
        )

    if current_branch == target_branch:
        self.print(f"Already on branch `{target_branch}`")
        return

    await proc_exec("git", "switch", target_branch, cwd=path)
    self.print(f"Switched to branch `{target_branch}`")


def main():
    with handle_interrupt():
        asyncio.run(make_workspace_task_runner(switch, with_root=False)())
