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
async def up(self: BaseAsyncTask, path: Path, msg: str = "up"):
    x = await proc_exec("git", "status", "-s", cwd=path)
    if x.stdout:
        self.print("Committing...")
        await proc_exec("git", "add", ".", cwd=path)
        await proc_exec("git", "commit", "-m", msg, cwd=path)
        self.print("Pushing...")
    else:
        self.print("Nothing to commit, pushing...")
    await proc_exec("git", "push", cwd=path)
    self.print("Success")


def main(msg: str = "up"):
    with handle_interrupt():
        asyncio.run(make_workspace_task_runner(up)(msg))
