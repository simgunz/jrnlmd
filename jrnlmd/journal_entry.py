from __future__ import annotations

import datetime
from typing import List, Optional, Union

from .parsers import parse_journal_entry_text

UNDEFINED_TOPIC = "ungrouped"


class JournalEntry:
    @staticmethod
    def from_string(text: str, prompt_for_input=False) -> JournalEntry:
        """Parse a string into a journal entry.

        Parameters
        ----------
        text : str
            A textual input with the following format:
            [date:] [topic [ . note1 [, note2 [, note3 [ ... ]]]]]
        prompt_for_input : bool, optional
            Flag to enable prompt from EDITOR if no note is present in the text,
            by default False

        Returns
        -------
        JournalEntry
        """
        from jrnlmd.ioutils import input_from_editor

        date, topic, notes = parse_journal_entry_text(text)
        if notes is None and prompt_for_input:
            notes = input_from_editor()
        return JournalEntry(notes, date, topic)

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
