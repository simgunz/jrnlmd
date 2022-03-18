import datetime
import re
from typing import List, Optional, Tuple, Union

import dateparser

TOKEN_SEP = "."
NOTE_SEP = ","


def parse_journal_entry_text(
    text: str,
) -> Tuple[Optional[str], Optional[str], Optional[List[str]]]:
    """Parse a journal entry text and return date, topic, and a list of notes.

    Parameters
    ----------
    text : str
        Texual input.

    Returns
    -------
    Tuple[Optional[str], Optional[str], Optional[List[str]]]
        date, topic, notes
    """
    m = re.search(":(?: |$)", text)
    colon_pos = m.start() if m else -1
    date = _parse_date(text[:colon_pos]) if colon_pos > 0 else None
    text = text[colon_pos + 1 :].strip()
    if not text:
        return date, None, None
    maybe_topic_notes = split_on_separator(text, TOKEN_SEP)
    topic = maybe_topic_notes[0]
    if len(maybe_topic_notes) == 1:
        return date, topic, None
    elif len(maybe_topic_notes) == 2:
        notes = split_on_separator(maybe_topic_notes[-1], NOTE_SEP)
        return date, topic, notes
    else:
        raise ValueError(f"Too many {TOKEN_SEP} in input.")


def _parse_date(text: str) -> Union[None, str]:
    import warnings

    # Ignore dateparser warnings regarding pytz
    warnings.filterwarnings(
        "ignore",
        message=(
            "The localize method is no longer necessary, as this time zone supports the"
            " fold attribute"
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


def split_on_separator(text: str, sep: str) -> List[str]:
    return [word.strip() for word in text.split(f" {sep} ")]
