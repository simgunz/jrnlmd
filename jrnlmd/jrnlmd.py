import sys
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