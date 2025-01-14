import typing

__all__ = [
    "ICCProfile",
    "Matrix3x3",
    "NamedGamut",
    "NamedTransferFn",
    "TransferFunction",
]

class ICCProfile:
    buffer: int
    data_color_space: int
    has_A2B: bool
    has_toXYZD50: bool
    has_trc: bool
    pcs: int
    size: int
    tag_count: int
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __init__(self) -> None: ...

class Matrix3x3:
    """

    A row-major 3x3 matrix (ie vals[row][col])

    """

    kAdobeRGB: typing.ClassVar[Matrix3x3]  # value = <skia.cms.Matrix3x3 object>
    kDisplayP3: typing.ClassVar[Matrix3x3]  # value = <skia.cms.Matrix3x3 object>
    kRec2020: typing.ClassVar[Matrix3x3]  # value = <skia.cms.Matrix3x3 object>
    kSRGB: typing.ClassVar[Matrix3x3]  # value = <skia.cms.Matrix3x3 object>
    kXYZ: typing.ClassVar[Matrix3x3]  # value = <skia.cms.Matrix3x3 object>
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __init__(self, v: list[float]) -> None: ...

class TransferFunction:
    """

    A transfer function mapping encoded values to linear values,
    represented by this 7-parameter piecewise function:

      linear = sign(encoded) *  (c*|encoded| + f)       , 0 <= |encoded| < d
             = sign(encoded) * ((a*|encoded| + b)^g + e), d <= |encoded|

    (A simple gamma transfer function sets g to gamma and a to 1.)

    """

    k2Dot2: typing.ClassVar[
        TransferFunction
    ]  # value = <skia.cms.TransferFunction object>
    kHLG: typing.ClassVar[
        TransferFunction
    ]  # value = <skia.cms.TransferFunction object>
    kLinear: typing.ClassVar[
        TransferFunction
    ]  # value = <skia.cms.TransferFunction object>
    kPQ: typing.ClassVar[TransferFunction]  # value = <skia.cms.TransferFunction object>
    kRec2020: typing.ClassVar[
        TransferFunction
    ]  # value = <skia.cms.TransferFunction object>
    kSRGB: typing.ClassVar[
        TransferFunction
    ]  # value = <skia.cms.TransferFunction object>
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __init__(self, v: list[float]) -> None: ...

NamedGamut = Matrix3x3
NamedTransferFn = TransferFunction
