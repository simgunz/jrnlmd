from collections import defaultdict
from typing import Set

from .usertypes import JDict, JDictDDateDTopic


class Journal:
    @classmethod
    def from_dict(cls, dictionary: JDict):
        journal = cls()
        for date, v in dictionary.items():
            journal._j[date] = defaultdict(str, v)
        return journal

    def __init__(self):
        self._j: JDictDDateDTopic = self._empty_dict()

    def _empty_dict(self):
        return defaultdict(lambda: defaultdict(str))

    def to_md(
        self,
        date_descending: bool = True,
        simplified: bool = False,
        compact: bool = False,
    ) -> str:
        keys: Set[str] = set()
        for v in self._j.values():
            keys.update(v.keys())
        canSimplify = len(keys) == 1
        output = []
        for day in sorted(self._j, reverse=date_descending):
            output.append(f"# {day}")
            if not compact:
                output.append("")
            for topic in self._j[day]:
                if not (simplified and canSimplify):
                    output.append(f"## {topic}")
                    if not compact:
                        output.append("")
                note = self._j[day][topic]
                output.append(note)
        return "\n".join(output)
