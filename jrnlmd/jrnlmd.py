from argparse import ArgumentParser
from pathlib import Path
from typing import List, Tuple

from .ioutils import print_with_external
from .journal import Journal
from .journal_entry import JournalEntry
from .journal_entry_filter import JournalEntryFilter


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
    elif args.command == "del":
        filter_ = " ".join(args.filter)
        command_del(journal, filter_)


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
    parser_cat.add_argument(
        "filter", type=str, nargs="*", help="[[{from, since}] date:] [topic]"
    )
    parser_cat.add_argument(
        "--simplified",
        action="store_true",
        help="Do not print the topic when the filter match a single topic.",
    )
    parser_cat.add_argument(
        "--compact",
        action="store_true",
        help="Reduce the number of blank lines in the output.",
    )
    parser_delete = subparsers.add_parser(
        "del", help="Delete an entry from the journal."
    )
    parser_delete.add_argument("filter", type=str, nargs="*", help="[[date:] [topic]")
    return parser


def command_add(journal: Journal, text: str) -> None:
    entry = JournalEntry.from_string(text, prompt_for_input=True)
    journal.add(entry)
    journal.save()


def command_cat(
    journal: Journal, filter_: str = "", simplified=False, compact=False
) -> None:
    filter_time_modifier, filter_ = _detect_time_modifier(filter_)
    entry_filter = JournalEntryFilter.from_string(filter_)
    simplify = False
    journal_filtered = journal
    if entry_filter.date:
        if filter_time_modifier == "since":
            journal_filtered = journal_filtered.since(entry_filter.date)
        else:
            journal_filtered = journal_filtered.on(entry_filter.date)
    if entry_filter.topic:
        simplify = True
        journal_filtered = journal_filtered.about(entry_filter.topic)
    print_with_external(
        journal_filtered.to_md(
            date_descending=False,
            simplified=(simplified and simplify),
            compact=compact,
        )
    )


def command_del(journal: Journal, filter_: str = ""):
    import sys

    entry_filter = JournalEntryFilter.from_string(filter_)
    if not entry_filter.date:
        print("ERROR: a date must be specified.", file=sys.stderr)
        return
    deleted_entries = journal.delete(entry_filter.date, entry_filter.topic)
    journal.save()
    print_with_external(f"Deleted entries:\n\n{deleted_entries.to_md()}")


def _detect_time_modifier(text: str) -> Tuple[str, str]:
    tokens = text.split()
    if tokens and tokens[0] in ["from", "since"]:
        return "since", " ".join(tokens[1:])
    else:
        return "on", text


def entrypoint() -> None:
    import sys

    main(sys.argv[1:])


if __name__ == "__main__":
    entrypoint()
