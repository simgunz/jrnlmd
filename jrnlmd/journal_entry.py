import datetime

UNDEFINED_TOPIC = "ungrouped"


class JournalEntry:
    def __init__(self, note, date: str = None, topic: str = None) -> None:
        self.note = note
        self.date = date or datetime.date.today().isoformat()
        self.topic = topic or UNDEFINED_TOPIC
