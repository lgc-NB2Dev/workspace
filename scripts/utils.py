import asyncio
import re
import sys
import textwrap
from abc import ABC, abstractmethod
from asyncio import CancelledError, Event, Semaphore, Task
from asyncio.taskgroups import TaskGroup
from collections.abc import Callable, Coroutine, Iterable
from contextlib import contextmanager, suppress
from dataclasses import dataclass
from functools import cached_property, partial
from pathlib import Path
from signal import SIGTERM
from subprocess import PIPE
from typing import (
    TYPE_CHECKING,
    Any,
    Concatenate,
    Generic,
    NamedTuple,
    ParamSpec,
    TypeAlias,
    TypeVar,
)

from tenacity import RetryCallState, RetryError, retry, wait_fixed

if TYPE_CHECKING:
    from asyncio.subprocess import Process

if sys.version_info < (3, 11):
    from asyncio.taskgroups import TaskGroup
else:
    from taskgroup import TaskGroup


SCRIPTS_DIR = Path(__file__).parent
ROOT_DIR = SCRIPTS_DIR.parent

P = ParamSpec("P")
R = TypeVar("R")

Co: TypeAlias = Coroutine[Any, Any, R]


def discover_submodules() -> list[Path]:
    f = (ROOT_DIR / ".gitmodules").read_text("u8")
    return [
        (ROOT_DIR / match.group(1))
        for match in re.finditer(r"^\s+path = (.+)$", f, re.MULTILINE)
    ]


def pad_num(num: int, num_max: int) -> str:
    return str(num).rjust(len(str(num_max)), "0")


async def dynamic_tasks(
    semaphore: Semaphore,
    constructors: Iterable[Callable[[], Coroutine]],
):
    _ev = Event()

    async def _w(co: Coroutine):
        async with semaphore:
            await co

    def _cb(_t: Task):
        _ev.set()
        _ev.clear()

    async with TaskGroup() as group:
        for con in constructors:
            while semaphore.locked():
                await _ev.wait()
            task = group.create_task(_w(con()))
            task.add_done_callback(_cb)
            await asyncio.sleep(0)  # yield to let semaphore acquire


@dataclass
class BaseAsyncTask(ABC, Generic[P, R]):
    current: int
    total: int
    name: str
    max_attempts: int = 3
    retry_wait: int = 2
    reraise: bool = False

    stop_retry_now: bool = False
    failed_with_exception: bool = False

    @cached_property
    def current_s(self):
        return pad_num(self.current, self.total)

    @cached_property
    def attempts_s(self):
        return pad_num(self.attempts, self.max_attempts)

    def __post_init__(self):
        self.attempts = 0
        self.retrying_f = retry(
            stop=self.should_stop,
            wait=wait_fixed(self.retry_wait),
            before=self.before_retry,
            after=self.after_retry,
            reraise=False,
        )(self.do)

    def print(self, *msg: str):
        print(
            f"({self.current_s}/{self.total}"
            f"|{self.attempts_s}/{self.max_attempts})"
            f" {self.name} |",
            *msg,
        )

    def should_stop(self, _s: RetryCallState, /):
        return (self.attempts >= self.max_attempts) or self.stop_retry_now

    def before_retry(self, _s: RetryCallState, /):
        self.attempts += 1
        with suppress(AttributeError):
            del self.attempts_s

    def print_retry_msg(self, s: RetryCallState, /):
        if self.should_stop(s):
            self.print(f"Operation still failed after {self.attempts} attempts")
        else:
            self.print(
                f"Attempt {self.attempts} failed"
                f", will retry after {self.retry_wait} seconds",
            )
        if s.outcome and (e := s.outcome.exception()):
            self.print(f"  {type(e).__name__}: {e}")

    def after_retry(self, s: RetryCallState, /):
        self.print_retry_msg(s)

    @abstractmethod
    async def do(self, *args: P.args, **kwargs: P.kwargs) -> R: ...

    async def __call__(self, *args: P.args, **kwds: P.kwargs) -> R | None:
        try:
            return await self.retrying_f(*args, **kwds)
        except RetryError as e:
            self.failed_with_exception = True
            if self.reraise:
                e.reraise()


def pascal_case(snake_str: str) -> str:
    return "".join(word.capitalize() for word in snake_str.split("_"))


def task(cls_name: str | None = None):
    def deco(
        func: Callable[Concatenate[BaseAsyncTask[P, R], P], R],
    ) -> type[BaseAsyncTask[P, R]]:
        return type(  # pyright: ignore[reportReturnType]
            cls_name or f"{pascal_case(func.__name__)}Task",
            (BaseAsyncTask,),
            {"do": func},
        )

    return deco


NAME_REPLACE_LIST = [
    ("nonebot-plugin-", "nb-p-"),
    ("nb-cli-plugin-", "nb-cli-p-"),
    ("picstatus-template-", "ps-t-"),
]


def replace_name(name: str) -> str:
    for old, new in NAME_REPLACE_LIST:
        name = name.replace(old, new)
    return name


def make_workspace_task_runner(
    task_cls: type[BaseAsyncTask[Concatenate[Path, P], Any]],
    with_root: bool = True,
) -> Callable[P, Co[None]]:
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> None:
        paths = discover_submodules()
        total = len(paths)
        print(f"* Discovered {total} submodules in workspace")

        names = [replace_name(p.name) for p in paths]
        max_path_len = max(len(x) for x in names)

        tasks = [
            (task_cls(i, total, n.ljust(max_path_len)), p)
            for i, (n, p) in enumerate(zip(names, paths), 1)
        ]
        await dynamic_tasks(
            Semaphore(8),
            (partial(t, p) for t, p in tasks),
        )

        if not with_root:
            return
        if any(x.failed_with_exception for x, _ in tasks):
            print("* Error occurred, will not continue committing root workspace")
            return
        await task_cls(1, 1, "<root>")(ROOT_DIR, *args, **kwargs)

    return wrapper


class ExecResult(NamedTuple):
    process: "Process"
    code: int
    stdout: str
    stderr: str


class CommandFailedError(RuntimeError):
    def __init__(self, r: ExecResult) -> None:
        super().__init__(
            f"Command failed with code {r.code}\n{textwrap.indent(r.stderr, '    ')}",
        )


async def proc_exec(*args: str, check: bool = True, **kwargs):
    p = await asyncio.create_subprocess_exec(
        *args,
        stdin=kwargs.pop("stdin", PIPE),
        stdout=kwargs.pop("stdout", PIPE),
        stderr=kwargs.pop("stderr", PIPE),
        **kwargs,
    )
    try:
        stdout, stderr = await p.communicate()
    except CancelledError:
        p.send_signal(SIGTERM)
        await p.wait()
        raise
    assert p.returncode is not None
    r = ExecResult(
        process=p,
        code=p.returncode,
        stdout=stdout.decode().strip(),
        stderr=stderr.decode().strip(),
    )
    if check and r.code != 0:
        raise CommandFailedError(r)
    return r


@contextmanager
def handle_interrupt():
    try:
        yield
    except (KeyboardInterrupt, asyncio.CancelledError):
        print("* Cancelled")
