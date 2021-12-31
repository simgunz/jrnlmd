import datetime
import itertools
import os
import re
import subprocess
import tempfile
from argparse import ArgumentParser
from collections import defaultdict
from pathlib import Path
from typing import Callable, DefaultDict, Dict, List, Tuple, Union

import dateparser

TOKEN_SEP = "."
NOTE_SEP = ","
EDITOR_INPUT_SYMBOL = "@"
UNDEFINED_TOPIC = "ungrouped"

JournalDict = Union[
    Dict[str, DefaultDict[str, str]], DefaultDict[str, DefaultDict[str, str]]
]


def empty_md_dict() -> JournalDict:
    return defaultdict(lambda: defaultdict(str))


def md_to_dict(text: str) -> JournalDict:
    d = empty_md_dict()
    current_day = ""
    current_topic = ""
    code_fence = False
    for line in text.splitlines():
        if line.startswith("```") or line.startswith("~~~"):
            code_fence = not code_fence
        if line.startswith("##") and not code_fence:
            current_topic = line.removeprefix("##").strip()
        elif line.startswith("#") and not code_fence:
            current_day = line.removeprefix("#").strip()
        elif line:
            if not (current_day and current_topic):
                raise ValueError("malformed journal")
            d[current_day][current_topic] += f"{line}\n"
    return d


def dict_to_md(d: JournalDict, date_descending=True) -> str:
    output = []
    for day in sorted(d, reverse=date_descending):
        output.append(f"# {day}")
        output.append("")
        for topic in d[day]:
            output.append(f"## {topic}")
            output.append("")
            output.append(d[day][topic])
    return "\n".join(output)


def add_note_to_dict(d: JournalDict, note: str, date: str, topic: str):
    d[date][topic] += parse_note(note)


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
        a_date = dateparser.parse(text, settings={"DATE_ORDER": "DMY"})
    if a_date is None:
        return None
    return a_date.date().isoformat()


def parse_input(text: str) -> Tuple[str, str, str]:
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
        for index, note_token in enumerate(split_notes_tokens):
            if len(note_token) == 1 and note_token[0] == EDITOR_INPUT_SYMBOL:
                split_notes_tokens[index] = [input_from_editor()]
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


def filter_dict_date(
    d: JournalDict, date: str, filt_func: Callable = str.__eq__
) -> JournalDict:
    return {k: v for k, v in d.items() if filt_func(k, date)}


def input_from_editor():

    editor = os.environ.get("EDITOR", "vim")
    with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:
        subprocess.call([editor, tf.name])
        tf.seek(0)
        return tf.read().decode("utf-8")


def command_add(journal: Path, text: List[str]) -> None:
    date, topic, note = parse_input(" ".join(text))
    if date is None:
        date = datetime.date.today().isoformat()
    if topic is None:
        topic = UNDEFINED_TOPIC
    if note is None:
        raw_note = input_from_editor()
        note = parse_note(raw_note)
    if journal.is_file():
        d = md_to_dict(journal.read_text())
    else:
        d = empty_md_dict()
    add_note_to_dict(d, note, date, topic)
    with open(journal, "w") as f:
        f.write(dict_to_md(d))


def cat_filtered_journal(journal: Path, date: str, filt_func: Callable) -> None:
    iso_date = parse_date(date)
    if iso_date is None:
        return
    d = md_to_dict(journal.read_text())
    filtered_d = filter_dict_date(d, iso_date, filt_func)
    print(dict_to_md(filtered_d, date_descending=False))


def command_cat(journal: Path, date: str = None) -> None:
    if not journal.is_file():
        return
    if date is None:
        cat_filtered_journal(journal, "0001-01-01", filt_func=str.__ge__)
    else:
        cat_filtered_journal(journal, date, filt_func=str.__eq__)


def command_since(journal: Path, since: str) -> None:
    if not journal.is_file():
        return
    cat_filtered_journal(journal, since, filt_func=str.__ge__)


def get_argparser() -> ArgumentParser:
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", help="journal actions")
    parser.add_argument(
        "-j",
        "--journal",
        type=Path,
        required=True,
        help="The journal file",
    )
    parser_add = subparsers.add_parser("add", help="Add a new note to the journal.")
    parser_add.add_argument(
        "text",
        metavar="",
        type=str,
        nargs="*",
        help="[date .] [topic . ] note1 [, note2 [, note3 [ ... ]]]",
    )
    parser_cat = subparsers.add_parser(
        "cat", help="Print the journal on the standard output."
    )
    parser_cat.add_argument(
        "date",
        type=str,
        nargs="?",
        help="The date to display.",
    )
    return parser


def main(argv: List[str]) -> None:
    parser = get_argparser()
    args = parser.parse_args(argv)
    if args.command == "add":
        command_add(args.journal, args.text)
    elif args.command == "cat":
        command_cat(args.journal, args.date)


def entrypoint() -> None:
    import sys

    main(sys.argv[1:])


if __name__ == "__main__":
    entrypoint()
