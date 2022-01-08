from typing import Set

from .usertypes import JournalDict


def dict_to_md(
    d: JournalDict,
    date_descending: bool = True,
    simplified: bool = False,
    compact: bool = False,
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
