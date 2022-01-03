from collections import defaultdict

from .usertypes import JDict, JDictDDateDTopic


class Journal:
    @classmethod
    def from_dict(cls, dictionary: JDict):
        journal = cls()
        for date, v in dictionary.items():
            journal._j[date] = defaultdict(str, v)
        return journal

    def __init__(self):
        self._j: JDictDDateDTopic = self._empty_dict()

    def _empty_dict(self):
        return defaultdict(lambda: defaultdict(str))
