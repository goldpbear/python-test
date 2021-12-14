"""Superclass of all parsers"""
from abc import ABCMeta, abstractmethod

from ironhide.models.model import Model


class Parser(metaclass=ABCMeta):
    """This is the parser class.  For typing purposes"""

    @classmethod
    @abstractmethod
    def parse(cls, raw) -> Model:
        """Requires parse method"""
