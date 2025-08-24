import asyncio
from pathlib import Path
from typing_extensions import override

from .utils import BaseAsyncTask, proc_exec, summon_workspace_tasks


class UpTask(BaseAsyncTask):
    @override
    async def do(self, path: Path):
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


asyncio.run(summon_workspace_tasks(UpTask))
