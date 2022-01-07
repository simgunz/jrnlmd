import datetime
import itertools
import os
import re
import subprocess
import tempfile
from argparse import ArgumentParser
from pathlib import Path
from typing import List, Optional, Tuple, Union

import dateparser

from jrnlmd.journal import Journal
from jrnlmd.journal_entry import JournalEntry

TOKEN_SEP = "."
NOTE_SEP = ","
EDITOR_INPUT_SYMBOL = "@"
UNDEFINED_TOPIC = "ungrouped"
EXTERNAL_COMMAND = "bat -l markdown --pager=never --style=plain"


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


def print_with_external(text: str) -> None:
    try:
        subprocess.run(EXTERNAL_COMMAND.split(), input=text, encoding="utf-8")
    except Exception:
        print(text)


def input_from_editor():

    editor = os.environ.get("EDITOR", "vim")
    with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:
        subprocess.call([editor, tf.name])
        tf.seek(0)
        return tf.read().decode("utf-8")


def command_add(journal: Journal, text: str) -> None:
    date, topic, note = parse_input(text)
    if note is None:
        note = input_from_editor()
    entry = JournalEntry(note, date, topic)
    journal.add(entry)
    journal.save()


def command_cat(
    journal: Journal, filter_: str = "", simplified=False, compact=False
) -> None:
    date, topic, _ = parse_input(filter_)
    simplify = False
    journal_filtered = journal
    if date:
        journal_filtered = journal_filtered.on(date)
    if topic:
        simplify = True
        journal_filtered = journal_filtered.about(topic)
    print_with_external(
        journal_filtered.to_md(
            date_descending=False,
            simplified=(simplified and simplify),
            compact=compact,
        )
    )


def command_since(journal: Journal, since: str) -> None:
    # TODO: add filter here
    print_with_external(journal.to_md(date_descending=False))


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
        type=str,
        nargs="*",
        help="[date:] [topic [ . note1 [, note2 [, note3 [ ... ]]]]]",
    )
    parser_cat = subparsers.add_parser(
        "cat", help="Print the journal on the standard output."
    )
    parser_cat.add_argument("filter", type=str, nargs="*", help="[date:] [topic]")
    parser_cat.add_argument(
        "--simplified", action="store_true", help="Hide topic if unique."
    )
    parser_cat.add_argument(
        "--compact", action="store_true", help="Remove empty lines in output."
    )
    return parser


def main(argv: List[str]) -> None:
    parser = get_argparser()
    args = parser.parse_args(argv)
    journal = Journal(args.journal)
    if args.command == "add":
        text = " ".join(args.text)
        command_add(journal, text)
    elif args.command == "cat":
        filter_ = " ".join(args.filter)
        command_cat(journal, filter_, args.simplified, args.compact)


def entrypoint() -> None:
    import sys

    main(sys.argv[1:])


if __name__ == "__main__":
    entrypoint()
