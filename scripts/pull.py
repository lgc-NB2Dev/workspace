import asyncio
from pathlib import Path
from typing_extensions import override

from .utils import BaseAsyncTask, proc_exec, summon_workspace_tasks


class PullTask(BaseAsyncTask):
    @override
    async def do(self, path: Path):
        self.print("Pulling...")
        await proc_exec("git", "pull", cwd=path)
        self.print("Success")


def main():
    asyncio.run(summon_workspace_tasks(PullTask))
