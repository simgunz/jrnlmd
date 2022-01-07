import datetime
import re
from typing import Optional, Union

import dateparser

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

    @staticmethod
    def parse_date(text: str) -> Union[None, str]:
        import warnings

        # Ignore dateparser warnings regarding pytz
        warnings.filterwarnings(
            "ignore",
            message=(
                "The localize method is no longer necessary, as this time zone supports"
                " the fold attribute"
            ),
        )
        if len(text) == 1 and not re.match(r"\d", text):
            return None
        try:
            a_date = datetime.datetime.fromisoformat(text)
        except ValueError:
            a_date = dateparser.parse(
                text, settings={"DATE_ORDER": "DMY", "PREFER_DATES_FROM": "past"}
            )
        if a_date is None:
            return None
        return a_date.date().isoformat()

    def __init__(self, note: str = None, date: str = None, topic: str = None) -> None:
        self.note = self._parse_note(note)
        self.date = date or datetime.date.today().isoformat()
        self.topic = topic or UNDEFINED_TOPIC
