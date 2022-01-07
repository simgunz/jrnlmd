import datetime

UNDEFINED_TOPIC = "ungrouped"


class JournalEntry:
    @staticmethod
    def _parse_note(note: str) -> str:
        stripped_note = note.removeprefix("-").lstrip()
        parsed_note = f"- {stripped_note}"
        rstripped_parsed_note = parsed_note.rstrip("\n")
        return f"{rstripped_parsed_note}\n"

    def __init__(self, note, date: str = None, topic: str = None) -> None:
        self.note = self._parse_note(note)
        self.date = date or datetime.date.today().isoformat()
        self.topic = topic or UNDEFINED_TOPIC
