import datetime
from typing import Optional

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

    def __init__(self, note: str = None, date: str = None, topic: str = None) -> None:
        self.note = self._parse_note(note)
        self.date = date or datetime.date.today().isoformat()
        self.topic = topic or UNDEFINED_TOPIC
