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
async def pull(self: BaseAsyncTask, path: Path):
    self.print("Pulling...")
    await proc_exec("git", "pull", cwd=path)
    self.print("Success")


def main():
    with handle_interrupt():
        asyncio.run(make_workspace_task_runner(pull)())
