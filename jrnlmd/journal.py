from collections import defaultdict
from pathlib import Path
from typing import Set, Union

from .journal_entry import JournalEntry
from .usertypes import JDict, JDictDDateDTopic, JournalDict


class Journal:
    def __init__(self, journal_path: Path = None):
        self.file_path = journal_path
        self._j: JDictDDateDTopic = self._empty_dict()
        if journal_path is not None:
            try:
                self.load()
            except FileNotFoundError:
                # The journal is a new journal
                pass

    @classmethod
    def from_dict(cls, dictionary: JDict):
        journal = cls()
        for date, v in dictionary.items():
            journal._j[date] = defaultdict(str, v)
        return journal

    @classmethod
    def from_md(cls, text: str) -> "Journal":
        journal = cls()
        journal._from_md(text)
        return journal

    @property
    def journal_file(self):
        return self.file_path

    @journal_file.setter
    def journal_file(self, file_path: Union[str, Path]):
        self.file_path = Path(file_path)

    def load(self) -> None:
        if self.file_path is None:
            raise RuntimeError("The journal file name has not been set.")
        if not self.file_path.is_file():
            raise FileNotFoundError()
        text = self.file_path.read_text()
        self._from_md(text)

    def save(self) -> None:
        if self.file_path is None:
            raise RuntimeError("The journal file name has not been set.")
        text = self.to_md()
        self.file_path.write_text(text)

    def to_md(
        self,
        date_descending: bool = True,
        simplified: bool = False,
        compact: bool = False,
    ) -> str:
        simplify = False
        if simplified:
            keys: Set[str] = set()
            for v in self._j.values():
                keys.update(v.keys())
            simplify = len(keys) == 1
        date_marker = "##" if simplify else "#"
        maybe_blank_line = "" if compact else "\n"
        output = []
        if simplify:
            topic = f"# {keys.pop()}{maybe_blank_line}"
            output.append(topic)
        for day in sorted(self._j, reverse=date_descending):
            output.append(f"{date_marker} {day}{maybe_blank_line}")
            for topic in self._j[day]:
                if not simplify:
                    output.append(f"## {topic}{maybe_blank_line}")
                note = self._j[day][topic]
                output.append(note)
        return "\n".join(output)

    def on(self, date: str) -> JournalDict:
        """Return a filtered journal on the given date."""
        return Journal.from_dict({k: v for k, v in self._j.items() if k == date})

    def since(self, date: str) -> JournalDict:
        """Return a filtered journal on the given date."""
        return Journal.from_dict({k: v for k, v in self._j.items() if k >= date})

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

    def delete(self, date: str, topic: str = None) -> "Journal":
        if date not in self._j:
            raise KeyError(f"{date} missing from journal.")
        if topic:
            if topic not in self._j[date]:
                raise KeyError(f"{topic} missing on {date} entry.")
            topic_to_delete = [topic]
        else:
            topic_to_delete = list(self._j[date].keys())
        deleted_entries = Journal()
        for tpc in topic_to_delete:
            deleted_entries.add(JournalEntry(self._j[date][tpc], date, tpc))
            del self._j[date][tpc]
        if not self._j[date]:
            del self._j[date]
        return deleted_entries

    def topics(self):
        topics = set()
        for date in self._j:
            topics.update(set(self._j[date].keys()))
        return sorted(list(topics))

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
            elif code_fence:
                self._j[current_day][current_topic] += f"{line}\n"
