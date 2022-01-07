import datetime
from typing import List, Optional, Union

UNDEFINED_TOPIC = "ungrouped"


class JournalEntry:
    @staticmethod
    def _parse_note(note: Optional[str]) -> str:
        if note is None:
            return ""
        stripped_note = note.removeprefix("-").lstrip()
        parsed_note = f"- {stripped_note}"
        rstripped_parsed_note = parsed_note.rstrip("\n")
        return f"{rstripped_parsed_note}\n"

    def __init__(
        self, note: Union[str, List[str]] = None, date: str = None, topic: str = None
    ) -> None:
        if isinstance(note, list):
            note = self._join_notes(note)
        self.note = self._parse_note(note)
        self.date = date or datetime.date.today().isoformat()
        self.topic = topic or UNDEFINED_TOPIC

    def _join_notes(self, notes: List[str]) -> str:
        return "".join(self._parse_note(note) for note in notes)
