import datetime
import itertools
import re
from typing import List, Optional, Tuple, Union

import dateparser

TOKEN_SEP = "."
NOTE_SEP = ","


def parse_note(note: str) -> str:
    stripped_note = note.removeprefix("-").lstrip()
    parsed_note = f"- {stripped_note}"
    rstripped_parsed_note = parsed_note.rstrip("\n")
    return f"{rstripped_parsed_note}\n"


def parse_date(text: str) -> Union[None, str]:
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


def parse_input(text: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """Parse a textual input and return date, topic, and the note.

    Parameters
    ----------
    text : str
        Texual input.

    Returns
    -------
    Tuple[str, str, str]
        date, topic, note
    """
    m = re.search(":(?: |$)", text)
    colon_pos = m.start() if m else -1
    date = parse_date(text[:colon_pos]) if colon_pos > 0 else None
    text = text[colon_pos + 1 :].strip()
    if not text:
        return date, None, None
    tokens = text.split()
    maybe_topic_notes_tokens = split_list_on_delimiter(tokens, TOKEN_SEP)
    topic = " ".join(maybe_topic_notes_tokens[0])
    if len(maybe_topic_notes_tokens) == 1:
        return date, topic, None
    elif len(maybe_topic_notes_tokens) == 2:
        notes_tokens = maybe_topic_notes_tokens[-1]
        split_notes_tokens = split_list_on_delimiter(notes_tokens, NOTE_SEP)
        note = join_notes_tokens(split_notes_tokens)
        return date, topic, note
    else:
        raise ValueError(f"Too many {TOKEN_SEP} in input.")


def join_notes_tokens(notes_tokens: List[List[str]]) -> str:
    notes = (" ".join(tokens) for tokens in notes_tokens)
    return "".join((parse_note(note) for note in notes))


def split_list_on_delimiter(tokens: List[str], delimiter: str) -> List[List[str]]:
    return [
        list(y) for x, y in itertools.groupby(tokens, lambda z: z == delimiter) if not x
    ]
