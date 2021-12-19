import datetime
import itertools
import re
from argparse import ArgumentParser
from collections import defaultdict
from pathlib import Path
from typing import Callable, DefaultDict, Dict, List, Tuple, Union

import dateparser

UNDEFINED_TOPIC_NAME = "ungrouped"

JournalDict = Union[
    Dict[str, DefaultDict[str, str]], DefaultDict[str, DefaultDict[str, str]]
]


def empty_md_dict() -> JournalDict:
    return defaultdict(lambda: defaultdict(str))


def md_to_dict(text: str) -> JournalDict:
    d = empty_md_dict()
    current_day = ""
    current_topic = ""
    for line in text.splitlines():
        if line.startswith("##"):
            current_topic = line.removeprefix("##").strip()
        elif line.startswith("#"):
            current_day = line.removeprefix("#").strip()
        elif line:
            if not (current_day and current_topic):
                raise ValueError("malformed journal")
            d[current_day][current_topic] += f"{line}\n"
    return d


def dict_to_md(d: JournalDict) -> str:
    output = []
    for day in sorted(d, reverse=True):
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
    if len(note.splitlines()) != 1:
        parsed_note = note
    else:
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
    tokens = text.split()
    date = parse_date(tokens[0])
    if date is None:
        date = datetime.date.today().isoformat()
    else:
        tokens.pop(0)
    maybe_topic_notes_tokens = split_list_on_delimiter(tokens, ".")
    notes_tokens = maybe_topic_notes_tokens[-1]
    topic = (
        " ".join(maybe_topic_notes_tokens[0])
        if len(maybe_topic_notes_tokens) == 2
        else UNDEFINED_TOPIC_NAME
    )
    split_notes_tokens = split_list_on_delimiter(notes_tokens, ",")
    note = join_notes_tokens(split_notes_tokens)
    return date, topic, parse_note(note)


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


def command_add(journal: Path, note_input: List[str]) -> None:
    date, topic, note = parse_input(" ".join(note_input))
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
    print(dict_to_md(filtered_d))


def command_cat(journal: Path, date: str = None) -> None:
    if not journal.is_file():
        return
    if date is None:
        print(journal.read_text())
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
        "note_input",
        type=str,
        nargs="+",
        help="[date] [topic . ] note1 [, note2 [, note3 [ ... ]]]",
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
    parser_since = subparsers.add_parser(
        "since", help="Output journal cat the given date."
    )
    parser_since.add_argument(
        "date",
        type=str,
        help="The start date.",
    )
    return parser


def main(argv: List[str]) -> None:
    parser = get_argparser()
    args = parser.parse_args(argv)
    if args.command == "add":
        command_add(args.journal, args.note_input)
    elif args.command == "cat":
        command_cat(args.journal, args.date)
    elif args.command == "since":
        command_since(args.journal, args.date)


def entrypoint() -> None:
    import sys

    main(sys.argv[1:])


if __name__ == "__main__":
    entrypoint()
