import datetime


class JournalEntry:
    def __init__(self, note) -> None:
        self.note = note
        self.date = datetime.date.today().isoformat()
