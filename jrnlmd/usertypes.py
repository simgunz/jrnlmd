from typing import DefaultDict, Dict, Union

JournalDict = Union[
    Dict[str, Dict[str, str]],
    Dict[str, DefaultDict[str, str]],
    DefaultDict[str, DefaultDict[str, str]],
]
