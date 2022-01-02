from typing import DefaultDict, Dict, Union

JDict = Dict[str, Dict[str, str]]
JDictDTopic = Dict[str, DefaultDict[str, str]]
JDictDDateDTopic = DefaultDict[str, DefaultDict[str, str]]
JournalDict = Union[JDict, JDictDTopic, JDictDDateDTopic]
