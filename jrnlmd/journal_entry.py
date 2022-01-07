import datetime

UNDEFINED_TOPIC = "ungrouped"


class JournalEntry:
    def __init__(self, note) -> None:
        self.note = note
        self.date = datetime.date.today().isoformat()
        self.topic = UNDEFINED_TOPIC
