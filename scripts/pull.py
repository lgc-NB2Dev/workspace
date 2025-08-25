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
async def pull(self: BaseAsyncTask, path: Path):
    self.print("Pulling...")
    await proc_exec("git", "pull", cwd=path)
    self.print("Success")


def main():
    with handle_interrupt():
        asyncio.run(summon_workspace_tasks(pull))
