from . import utils as utils

def ratio(s1: str, s2: str) -> int: ...
def partial_ratio(s1: str, s2: str) -> int: ...
def token_sort_ratio(
    s1: str,
    s2: str,
    force_ascii: bool = True,
    full_process: bool = True,
) -> int: ...
def partial_token_sort_ratio(
    s1: str,
    s2: str,
    force_ascii: bool = True,
    full_process: bool = True,
) -> int: ...
def token_set_ratio(
    s1: str,
    s2: str,
    force_ascii: bool = True,
    full_process: bool = True,
) -> int: ...
def partial_token_set_ratio(
    s1: str,
    s2: str,
    force_ascii: bool = True,
    full_process: bool = True,
) -> int: ...
def QRatio(
    s1: str,
    s2: str,
    force_ascii: bool = True,
    full_process: bool = True,
) -> int: ...
def UQRatio(
    s1: str,
    s2: str,
    full_process: bool = True,
) -> int: ...
def WRatio(
    s1: str,
    s2: str,
    force_ascii: bool = True,
    full_process: bool = True,
) -> int: ...
def UWRatio(
    s1: str,
    s2: str,
    full_process: bool = True,
) -> int: ...
