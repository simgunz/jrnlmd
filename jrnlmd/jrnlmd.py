from pathlib import Path
from typing import Tuple

import click
import click_config_file

from . import config
from .ioutils import print_with_external
from .journal import Journal
from .journal_entry import JournalEntry
from .journal_entry_filter import JournalEntryFilter


@click.group(name="jrnlmd", invoke_without_command=True)
@click.option(
    "-j",
    "--journal",
    type=click.Path(path_type=Path),
    required=True,
    help="The journal file",
)
@click.pass_context
@click_config_file.configuration_option(config_file_name=config.DEFAULT_CONFIG_FILE)
def cli(ctx: click.Context, journal: Path):
    ctx.ensure_object(dict)
    ctx.obj["JOURNAL"] = Journal(journal)
    if ctx.invoked_subcommand is None:
        ctx.invoke(cat, filter_="")


@cli.command()
@click.argument(
    "text",
    metavar="[DATE:] [TOPIC [ . NOTE1 [, NOTE2 [ ... ]]]]",
    nargs=-1,
    callback=lambda x, y, z: " ".join(z),
)
@click.pass_context
def add(ctx: click.Context, text: str) -> None:
    entry = JournalEntry.from_string(text, prompt_for_input=True)
    if not entry.is_valid():
        return
    journal = ctx.obj["JOURNAL"]
    journal.add(entry)
    journal.save()
    print_with_external(journal.on(entry.date).about(entry.topic).to_md())


@cli.command()
@click.option("--default-filter", default="", hidden=True)
@click.option(
    "--compact/--no-compact",
    default=False,
    help="Reduce the number of blank lines in the output.",
)
@click.option(
    "--simplified/--no-simplified",
    default=False,
    help="Do not print the topic when the filter match a single topic.",
)
@click.argument(
    "filter_",
    metavar="[DATE:] [TOPIC]",
    nargs=-1,
    callback=lambda x, y, z: " ".join(z),
)
@click.pass_context
def cat(
    ctx: click.Context,
    filter_: str = "",
    simplified=False,
    compact=False,
    default_filter: str = "",
) -> None:
    if not filter_:
        filter_ = default_filter
    filter_time_modifier, filter_ = _detect_time_modifier(filter_)
    entry_filter = JournalEntryFilter.from_string(filter_)
    simplify = False
    journal_filtered = ctx.obj["JOURNAL"]
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


@cli.command(name="del")
@click.argument(
    "filter_",
    metavar="DATE: [TOPIC]",
    nargs=-1,
    callback=lambda x, y, z: " ".join(z),
)
@click.pass_context
def delete(ctx: click.Context, filter_: str = ""):
    import sys

    journal = ctx.obj["JOURNAL"]
    entry_filter = JournalEntryFilter.from_string(filter_)
    if not entry_filter.date:
        print("ERROR: a date must be specified.", file=sys.stderr)
        return
    deleted_entries = journal.delete(entry_filter.date, entry_filter.topic)
    journal.save()
    print_with_external(f"Deleted entries:\n\n{deleted_entries.to_md()}")


@cli.command()
@click.pass_context
def top(ctx: click.Context):
    journal = ctx.obj["JOURNAL"]
    print("\n".join(journal.topics()))


def _detect_time_modifier(text: str) -> Tuple[str, str]:
    tokens = text.split()
    if tokens and tokens[0] in ["from", "since"]:
        return "since", " ".join(tokens[1:])
    else:
        return "on", text


if __name__ == "__main__":
    cli()
