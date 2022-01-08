from __future__ import annotations

from .parsers import parse_journal_entry_text


class JournalEntryFilter:
    @classmethod
    def from_string(cls, text: str) -> JournalEntryFilter:
        """Parse a string into a journal entry filter.

        Parameters
        ----------
        text : str
            A textual input with the following format:
            [date:] [topic]

        Returns
        -------
        JournalEntryFilter
        """
        date, topic, _ = parse_journal_entry_text(text)
        return cls(date, topic)

    def __init__(self, date: str = None, topic: str = None) -> None:
        self.date = date
        self.topic = topic
