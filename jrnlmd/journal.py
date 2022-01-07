from collections import defaultdict
from pathlib import Path
from typing import Set

from .usertypes import JDict, JDictDDateDTopic, JournalDict


class Journal:
    @classmethod
    def from_dict(cls, dictionary: JDict):
        journal = cls()
        for date, v in dictionary.items():
            journal._j[date] = defaultdict(str, v)
        return journal

    @classmethod
    def from_md(cls, text: str) -> JournalDict:
        journal = cls()
        journal._from_md(text)
        return journal

    def __init__(self, journal_path: Path = None):
        self._journal_path = journal_path
        self._j: JDictDDateDTopic = self._empty_dict()

    def load(self) -> None:
        if self._journal_path is None:
            raise RuntimeError("The journal file name has not been set.")
        if not self._journal_path.is_file():
            raise FileNotFoundError()
        text = self._journal_path.read_text()
        self._from_md(text)

    def save(self) -> None:
        if self._journal_path is None:
            raise RuntimeError("The journal file name has not been set.")
        self._journal_path.write_text("")

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

    def _empty_dict(self):
        return defaultdict(lambda: defaultdict(str))

    def _from_md(self, text: str):
        current_day = ""
        current_topic = ""
        code_fence = False
        for line in text.splitlines():
            if line.startswith("```") or line.startswith("~~~"):
                code_fence = not code_fence
            if line.startswith("##") and not code_fence:
                current_topic = line.removeprefix("##").strip()
            elif line.startswith("#") and not code_fence:
                current_day = line.removeprefix("#").strip()
            elif line:
                if not (current_day and current_topic):
                    raise ValueError("malformed journal")
                self._j[current_day][current_topic] += f"{line}\n"
