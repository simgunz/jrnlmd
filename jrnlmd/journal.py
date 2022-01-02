from collections import defaultdict

from .usertypes import JDictDDateDTopic


class Journal:
    def __init__(self):
        self._j: JDictDDateDTopic = defaultdict(lambda: defaultdict(str))
