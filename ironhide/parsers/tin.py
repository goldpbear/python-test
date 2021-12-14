"""Parse TIN Number"""
from __future__ import annotations

from contextlib import suppress
from typing import Dict, List, Union, Optional, Any

from optimus.models.tin import TINModel
from optimus.parsers.parser import Parser
from optimus.models.model import Model


class TINParser(Parser):
    """TIN Parser."""

    @classmethod
    def parse(cls, raw: Union[str, Dict[str, str]]) -> Model:
        """
        Parse input.

        Atributes
        ---------
        raw
        """

        try:
            for k, v in raw.items():
                for i in ("111111111", "333333333", "666666666", "123456789"):
                    if i == v:
                        raise Exception
                elif not k:
                    raise Exception
                else:
                    return TINModel(**v)

        except Exception as e:
            raise e
