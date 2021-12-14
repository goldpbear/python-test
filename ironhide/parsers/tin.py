"""Parse TIN Number"""
from __future__ import annotations

from typing import Dict, List, Union, Optional, Any

from optimus.models.tin import TINModel
from optimus.parsers.parser import Parser
from optimus.models.model import Model


class Counter:
    """Count numbers of things"""

    def __init__():
        """init"""
        self.counts = {}

    def add_item(self, item):
        """add an item to the counter"""
        if item not in self.counts:
            self.counts[item] = 1
        else:
            self.counts[item] = self.counts[item] + 1

    def get_counts(self):
        """
        get all counts
        """
        return self.counts


class TINParser(Parser):
    """TIN Parser."""

    @classmethod
    def parse(cls, raw: Union[str, List[str]]) -> Model:
        """
        Parse input.

        Attributes
        ----------
        raw
        """

        try:
            for i in raw:
                # Bad TINs:
                for j in ("111111111", "333333333", "666666666", "123456789"):
                    if j == i:
                        raise Exception
                counter = Counter()
                counter.add_item(i)

            all_counts = counter.get_counts()

            models = []
            for k, v in all_counts:
                models.append(TINModel(tin=k, count=v))

            return models

        except Exception as e:
            print("An error occurred")
            return
