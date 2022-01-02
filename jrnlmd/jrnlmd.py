import datetime
import itertools
import os
import re
import subprocess
import tempfile
from argparse import ArgumentParser
from collections import defaultdict
from pathlib import Path
from typing import Callable, DefaultDict, Dict, List, Optional, Set, Tuple, Union

import dateparser

TOKEN_SEP = "."
NOTE_SEP = ","
EDITOR_INPUT_SYMBOL = "@"
UNDEFINED_TOPIC = "ungrouped"
EXTERNAL_COMMAND = "bat -l markdown --pager=never --style=plain"

JournalDict = Union[
    Dict[str, Dict[str, str]],
    Dict[str, DefaultDict[str, str]],
    DefaultDict[str, DefaultDict[str, str]],
]


def empty_md_dict() -> DefaultDict[str, DefaultDict[str, str]]:
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


def dict_to_md(
    d: JournalDict, date_descending=True, simplified=False, compact=False
) -> str:
    keys: Set[str] = set()
    for v in d.values():
        keys.update(v.keys())
    canSimplify = len(keys) == 1
    output = []
    for day in sorted(d, reverse=date_descending):
        output.append(f"# {day}")
        if not compact:
            output.append("")
        for topic in d[day]:
            if not (simplified and canSimplify):
                output.append(f"## {topic}")
                if not compact:
                    output.append("")
            note = d[day][topic]
            output.append(note)
    return "\n".join(output)


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


def filter_dict_date(
    d: JournalDict, date: str, filt_func: Callable = str.__eq__
) -> JournalDict:
    return {k: v for k, v in d.items() if filt_func(k, date)}


def filter_dict_topic(d: JournalDict, topic: str) -> JournalDict:
    return {
        k: {kk: vv for kk, vv in v.items() if topic in kk}
        for k, v in d.items()
        if any(topic in kkk for kkk in v.keys())
    }


def input_from_editor():

    editor = os.environ.get("EDITOR", "vim")
    with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:
        subprocess.call([editor, tf.name])
        tf.seek(0)
        return tf.read().decode("utf-8")


def command_add(journal: Path, text: str) -> None:
    date, topic, note = parse_input(text)
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
    d[date][topic] += parse_note(note)
    with open(journal, "w") as f:
        f.write(dict_to_md(d))


def command_cat(
    journal: Path, filter_: str = "", simplified=False, compact=False
) -> None:
    if not journal.is_file():
        return
    filtered_d = md_to_dict(journal.read_text())
    if not filter_:
        print_with_external(
            dict_to_md(filtered_d, date_descending=False, compact=compact)
        )
        return
    date, topic, _ = parse_input(filter_)
    simplify = False
    if date:
        filtered_d = filter_dict_date(filtered_d, date, filt_func=str.__eq__)
    if topic:
        simplify = True
        filtered_d = filter_dict_topic(filtered_d, topic)
    print_with_external(
        dict_to_md(
            filtered_d,
            date_descending=False,
            simplified=(simplified and simplify),
            compact=compact,
        )
    )


def command_since(journal: Path, since: str) -> None:
    if not journal.is_file():
        return
    d = md_to_dict(journal.read_text())
    filtered_d = filter_dict_date(d, since, filt_func=str.__ge__)
    print_with_external(dict_to_md(filtered_d, date_descending=False))


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
    if args.command == "add":
        text = " ".join(args.text)
        command_add(args.journal, text)
    elif args.command == "cat":
        filter_ = " ".join(args.filter)
        command_cat(args.journal, filter_, args.simplified, args.compact)


def entrypoint() -> None:
    import sys

    main(sys.argv[1:])


if __name__ == "__main__":
    entrypoint()
