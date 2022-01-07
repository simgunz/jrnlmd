from argparse import ArgumentParser
from pathlib import Path
from typing import List

from jrnlmd.journal import Journal
from jrnlmd.journal_entry import JournalEntry

from .ioutils import print_with_external
from .parsers import parse_journal_entry_text


def command_add(journal: Journal, text: str) -> None:
    entry = JournalEntry.from_string(text, prompt_for_input=True)
    journal.add(entry)
    journal.save()


def command_cat(
    journal: Journal, filter_: str = "", simplified=False, compact=False
) -> None:
    date, topic, _ = parse_journal_entry_text(filter_)
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
