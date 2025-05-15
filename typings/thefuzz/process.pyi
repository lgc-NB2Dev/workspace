from collections.abc import Generator
from typing import Callable, Iterable, Mapping, TypeVar, overload

from . import fuzz as fuzz, utils as utils

_Q = TypeVar("_Q")
_K = TypeVar("_K")
_V = TypeVar("_V")

class _SupportsItems(Mapping[_K, _V]):
    def items(self) -> Iterable[tuple[_K, _V]]: ...

default_scorer = fuzz.WRatio
default_processor = utils.full_process

@overload
def extractWithoutOrder(
    query: _Q,
    choices: _SupportsItems[_K, _V],
    processor: Callable[[_Q | _V], str] = ...,
    scorer: Callable[[_Q, _V], int] = ...,
    score_cutoff: int = 0,
) -> Generator[None, None, tuple[_V, int, _K]]: ...
@overload
def extractWithoutOrder(
    query: _Q,
    choices: Iterable[_V],
    processor: Callable[[_Q | _V], str] = ...,
    scorer: Callable[[_Q, _V], int] = ...,
    score_cutoff: int = 0,
) -> Generator[None, None, tuple[_V, int]]: ...
def extract(
    query,
    choices,
    processor=...,
    scorer=...,
    limit: int = 5,
): ...
def extractBests(
    query,
    choices,
    processor=...,
    scorer=...,
    score_cutoff: int = 0,
    limit: int = 5,
): ...
def extractOne(
    query,
    choices,
    processor=...,
    scorer=...,
    score_cutoff: int = 0,
): ...
def dedupe(
    contains_dupes,
    threshold: int = 70,
    scorer=...,
): ...
