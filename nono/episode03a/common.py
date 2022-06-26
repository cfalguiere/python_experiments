"""Define common types types and constants."""
from typing import Any, Dict, List, Union

# import numpy.typing as npt


ClueType = Union[List[int], int]
CluesType = Dict[str, List[ClueType]]
NormClueType = List[int]
NormCluesType = Dict[str, List[NormClueType]]
# SolutionType = npt.ArrayLike
SolutionType = Any

ColorMapType = Any
