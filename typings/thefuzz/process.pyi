from collections.abc import Generator, Mapping, Sequence
from typing import Callable, TypeVar, overload

from . import fuzz as fuzz, utils as utils

_Q = TypeVar("_Q")
_K = TypeVar("_K")
_V = TypeVar("_V")

_SQ = TypeVar("_SQ", bound=str)
_SK = TypeVar("_SK", bound=str)
_SV = TypeVar("_SV", bound=str)

default_scorer = fuzz.WRatio
default_processor = utils.full_process

# extractWithoutOrder
@overload
def extractWithoutOrder(
    query: _SQ,
    choices: Mapping[_SK, _SV],
    processor: Callable[[_SQ | _SV], str] = ...,
    scorer: Callable[[str, str], int] = ...,
    score_cutoff: int = 0,
) -> Generator[tuple[_SV, int, _SK], None, None]: ...
@overload
def extractWithoutOrder(
    query: _SQ,
    choices: Sequence[_SV],
    processor: Callable[[_SQ | _SV], str] = ...,
    scorer: Callable[[str, str], int] = ...,
    score_cutoff: int = 0,
) -> Generator[tuple[_SV, int], None, None]: ...
@overload
def extractWithoutOrder(
    query: _Q,
    choices: Mapping[_K, _V],
    processor: Callable[[_Q | _V], str],
    scorer: Callable[[str, str], int] = ...,
    score_cutoff: int = 0,
) -> Generator[tuple[_V, int, _K], None, None]: ...
@overload
def extractWithoutOrder(
    query: _Q,
    choices: Sequence[_V],
    processor: Callable[[_Q | _V], str],
    scorer: Callable[[str, str], int] = ...,
    score_cutoff: int = 0,
) -> Generator[tuple[_V, int], None, None]: ...

# extract
@overload
def extract(
    query: _SQ,
    choices: Mapping[_SK, _SV],
    processor: Callable[[_SQ | _SV], str] = ...,
    scorer: Callable[[str, str], int] = ...,
    limit: int = 5,
) -> list[tuple[_SV, int, _SK]]: ...
@overload
def extract(
    query: _SQ,
    choices: Sequence[_SV],
    processor: Callable[[_SQ | _SV], str] = ...,
    scorer: Callable[[str, str], int] = ...,
    limit: int = 5,
) -> list[tuple[_SV, int]]: ...
@overload
def extract(
    query: _Q,
    choices: Mapping[_K, _V],
    processor: Callable[[_Q | _V], str],
    scorer: Callable[[str, str], int] = ...,
    limit: int = 5,
) -> list[tuple[_V, int, _K]]: ...
@overload
def extract(
    query: _Q,
    choices: Sequence[_V],
    processor: Callable[[_Q | _V], str],
    scorer: Callable[[str, str], int] = ...,
    limit: int = 5,
) -> list[tuple[_V, int]]: ...

# extractBests
@overload
def extractBests(
    query: _SQ,
    choices: Mapping[_SK, _SV],
    processor: Callable[[_SQ | _SV], str] = ...,
    scorer: Callable[[str, str], int] = ...,
    score_cutoff: int = 0,
    limit: int = 5,
) -> list[tuple[_SV, int, _SK]]: ...
@overload
def extractBests(
    query: _SQ,
    choices: Sequence[_SV],
    processor: Callable[[_SQ | _SV], str] = ...,
    scorer: Callable[[str, str], int] = ...,
    score_cutoff: int = 0,
    limit: int = 5,
) -> list[tuple[_SV, int]]: ...
@overload
def extractBests(
    query: _Q,
    choices: Mapping[_K, _V],
    processor: Callable[[_Q | _V], str],
    scorer: Callable[[str, str], int] = ...,
    score_cutoff: int = 0,
    limit: int = 5,
) -> list[tuple[_V, int, _K]]: ...
@overload
def extractBests(
    query: _Q,
    choices: Sequence[_V],
    processor: Callable[[_Q | _V], str],
    scorer: Callable[[str, str], int] = ...,
    score_cutoff: int = 0,
    limit: int = 5,
) -> list[tuple[_V, int]]: ...

# extractOne
@overload
def extractOne(
    query: _SQ,
    choices: Mapping[_SK, _SV],
    processor: Callable[[_SQ | _SV], str] = ...,
    scorer: Callable[[str, str], int] = ...,
    score_cutoff: int = 0,
) -> tuple[_SV, int, _SK]: ...
@overload
def extractOne(
    query: _SQ,
    choices: Sequence[_SV],
    processor: Callable[[_SQ | _SV], str] = ...,
    scorer: Callable[[str, str], int] = ...,
    score_cutoff: int = 0,
) -> tuple[_SV, int]: ...
@overload
def extractOne(
    query: _Q,
    choices: Mapping[_K, _V],
    processor: Callable[[_Q | _V], str],
    scorer: Callable[[str, str], int] = ...,
    score_cutoff: int = 0,
) -> tuple[_V, int, _K]: ...
@overload
def extractOne(
    query: _Q,
    choices: Sequence[_V],
    processor: Callable[[_Q | _V], str],
    scorer: Callable[[str, str], int] = ...,
    score_cutoff: int = 0,
) -> tuple[_V, int]: ...

# dedupe
def dedupe(
    contains_dupes: Sequence[_SV],
    threshold: int = 70,
    scorer: Callable[[str, str], int] = ...,
) -> Sequence[_SV]: ...
