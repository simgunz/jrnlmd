from argparse import ArgumentParser
from pathlib import Path


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
    parser_delete = subparsers.add_parser(
        "del", help="Delete an entry from the journal."
    )
    parser_delete.add_argument("filter", type=str, nargs="*", help="[[date:] [topic]")
    return parser
