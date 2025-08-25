import asyncio
from pathlib import Path

from .utils import (
    BaseAsyncTask,
    handle_interrupt,
    proc_exec,
    summon_workspace_tasks,
    task,
)


@task()
async def up(self: BaseAsyncTask, path: Path):
    x = await proc_exec("git", "status", "-s", cwd=path)
    if x.stdout:
        self.print("Committing...")
        await proc_exec("git", "add", ".", cwd=path)
        await proc_exec("git", "commit", "-m", "up", cwd=path)
        self.print("Pushing...")
    else:
        self.print("Nothing to commit, pushing...")
    await proc_exec("git", "push", cwd=path)
    self.print("Success")


def main():
    with handle_interrupt():
        asyncio.run(summon_workspace_tasks(up))
