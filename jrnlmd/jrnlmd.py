import argparse
import dateparser
import datetime
import itertools
import re
from argparse import ArgumentParser
from collections import defaultdict
from pathlib import Path
from typing import DefaultDict, Tuple, Union


def empty_md_dict() -> DefaultDict[str, DefaultDict[str, str]]:
    return defaultdict(lambda: defaultdict(str))


def md_to_dict(text: str) -> DefaultDict:
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


def dict_to_md(d) -> str:
    output = []
    for day in sorted(d):
        output.append(f"# {day}")
        output.append("")
        for topic in d[day]:
            output.append(f"## {topic}")
            output.append("")
            output.append(d[day][topic])
    return "\n".join(output)


def add_note_to_dict(d, note, date, topic):
    d[date][topic] += parse_note(note)
    return d


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
        message="The localize method is no longer necessary, as this time zone supports the fold attribute",
    )
    if len(text) == 1 and not re.match("\d", text):
        return None
    a_date = dateparser.parse(text, settings={"DATE_ORDER": "DMY"})
    if a_date is None:
        return None
    return a_date.strftime("%Y-%m-%d")


def parse_input(text: str) -> Tuple[str, str, str]:
    tokens = text.split()
    date = parse_date(tokens[0])
    if date is None:
        date_today = datetime.date.today()
        date = date_today.strftime("%Y-%m-%d")
    else:
        tokens.pop(0)
    maybe_topic_notes_tokens = split_list_on_delimiter(tokens, ".")
    notes_tokens = maybe_topic_notes_tokens[-1]
    topic = (
        " ".join(maybe_topic_notes_tokens[0])
        if len(maybe_topic_notes_tokens) == 2
        else "ungrouped"
    )
    split_notes_tokens = split_list_on_delimiter(notes_tokens, ",")
    note = join_notes_tokens(split_notes_tokens)
    return date, topic, parse_note(note)


def join_notes_tokens(notes_tokens):
    notes = (" ".join(tokens) for tokens in notes_tokens)
    return "".join((parse_note(note) for note in notes))


def split_list_on_delimiter(tokens, delimiter):
    return tuple(
        list(y) for x, y in itertools.groupby(tokens, lambda z: z == delimiter) if not x
    )


def get_argparser():
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
    parser_add = subparsers.add_parser(
        "since", help="Output journal cat the given date."
    )
    parser_add.add_argument(
        "since",
        type=str,
        help="The start date.",
    )
    return parser


def add_note_to_journal(journal, note_input):
    date, topic, note = parse_input(" ".join(note_input))
    if journal.is_file():
        with open(journal, "r") as f:
            d = md_to_dict(f.read())
    else:
        d = empty_md_dict()
    updated_d = add_note_to_dict(d, note, date, topic)
    with open(journal, "w") as f:
        f.write(dict_to_md(updated_d))


def main(argv):
    parser = get_argparser()
    args = parser.parse_args(argv)
    if args.command == "add":
        add_note_to_journal(args.journal, args.note_input)
    elif args.command == "since":
        if not args.journal.is_file():
            return
        with open(args.journal, "r") as f:
            d = md_to_dict(f.read())
        from_date = dateparser.parse(args.since).strftime("%Y-%m-%d")
        filtered_d = {k: v for k, v in d.items() if k >= from_date}
        print(dict_to_md(filtered_d))


def entrypoint():
    import sys

    main(sys.argv[1:])


if __name__ == "__main__":
    entrypoint()
