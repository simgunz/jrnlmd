import dateparser
from collections import defaultdict
from typing import DefaultDict


def md_to_dict(text: str) -> DefaultDict:
    d: DefaultDict[str, DefaultDict[str, str]] = defaultdict(lambda: defaultdict(str))
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


def parse_date(text: str) -> str:
    import warnings

    # Ignore dateparser warnings regarding pytz
    warnings.filterwarnings(
        "ignore",
        message="The localize method is no longer necessary, as this time zone supports the fold attribute",
    )
    a_date = dateparser.parse(text, settings={"DATE_ORDER": "DMY"})
    return a_date.strftime("%Y-%m-%d")
