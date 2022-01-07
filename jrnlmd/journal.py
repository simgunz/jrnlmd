from collections import defaultdict
from pathlib import Path
from typing import Set, Union

from .journal_entry import JournalEntry
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
        self._journal_file = journal_path
        self._j: JDictDDateDTopic = self._empty_dict()
        if journal_path is not None:
            try:
                self.load()
            except FileNotFoundError:
                # The journal is a new journal
                pass

    @property
    def journal_file(self):
        return self._journal_file

    @journal_file.setter
    def journal_file(self, file_path: Union[str, Path]):
        self._journal_file = Path(file_path)

    def load(self) -> None:
        if self._journal_file is None:
            raise RuntimeError("The journal file name has not been set.")
        if not self._journal_file.is_file():
            raise FileNotFoundError()
        text = self._journal_file.read_text()
        self._from_md(text)

    def save(self) -> None:
        if self._journal_file is None:
            raise RuntimeError("The journal file name has not been set.")
        text = self.to_md()
        self._journal_file.write_text(text)

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

    def on(self, date: str) -> JournalDict:
        """Return a filtered journal on the given date."""
        return Journal.from_dict({k: v for k, v in self._j.items() if k == date})

    def about(self, topic: str) -> JournalDict:
        """Return a filtered journal about the given topic.

        The topic can be a partial match."""
        return Journal.from_dict(
            {
                k: {kk: vv for kk, vv in v.items() if topic in kk}
                for k, v in self._j.items()
                if any(topic in kkk for kkk in v.keys())
            }
        )

    def add(self, entry: JournalEntry) -> None:
        self._j[entry.date][entry.topic] += entry.note

    def _empty_dict(self):
        return defaultdict(lambda: defaultdict(str))

    def _from_md(self, text: str):
        self._j = self._empty_dict()
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
