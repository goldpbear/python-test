"""Parse TIN Number"""
from __future__ import annotations

from typing import Dict, List, Union, Optional, Any

from ironhide.models.tin import TINModel
from ironhide.parsers.parser import Parser
from ironhide.models.model import Model

import re
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class Counter:
    """Count numbers of things"""

    def __init__(self):
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
    def is_valid_tin(cls, tin):
        """Validates a TIN.  May be a SSN or ITIN.  The rules for validation are:
            Valid TIN - ITIN: /^9\d{2}-?((5[0-9]|6[0-5])|(8[3-8])|(9[0-2])|(9[4-9]))-?\d{4}$/
            Valid TIN - SSN: /^((?!666|000)[0-8][0-9\_]{2}\-(?!00)[0-9\_]{2}\-(?!0000)[0-9\_]{4})*$/
            Invalid TIN - SSN: 111111111, 333333333, 666666666, 123456789 (666666666 is checked in the regex)
            Invalid TIN - SSN: Area Numbers (first 3 digits) - 000, 666 (900 – 999 could be a valid ITIN))
            Invalid TIN - SSN: Group Numbers (4th / 5th digits) - 00
            Invalid TIN - SSN: Serial Numbers (last 4 digits) - 0000

        Args:
        tin: A string representing a Tax Identification Number.

        Returns:
        True if passed TIN is valid, False if not

        Raises:
        Exception: If there is an issue validating the tin
        """

        ssn_regex = re.compile(r'^((?!666|000)[0-8][0-9\_]{2}\-(?!00)[0-9\_]{2}\-(?!0000)[0-9\_]{4})*$')
        itin_regex = re.compile(r'^9\d{2}-?((5[0-9]|6[0-5])|(8[3-8])|(9[0-2])|(9[4-9]))-?\d{4}$')
        invalid_ssns_explicit = ['111-11-1111', '333-33-3333', '123-45-6789']

        try:
            if not tin:
                return False
            if (re.match(ssn_regex, tin) and (tin not in invalid_ssns_explicit)) or re.match(itin_regex, tin):
                return True
        except Exception as e:
            print(f'An error occurred validating tin {tin}: {e}')
            logger.error(f'An error occurred validating tin {tin}: {e}')
            return False

        return False

    @classmethod
    def parse(cls, raw: Union[str, List[str]]) -> Model:
        """Parse input.

        Args:
        raw: A string or list representing a TIN and type of TIN.

        Returns:
        A list of valid TINModels.

        Raises:
        Exception: If there is an issue parsing the input
        """

        try:
            counter = Counter()

            for i in raw:
                if len(i) > 0:
                    tin = i[0]
                    valid_tin = cls.is_valid_tin(tin)

                    if valid_tin:
                        counter.add_item(tin)
                    else:
                        print(f'Invalid TIN: {tin}')
                        logger.info(f'Invalid TIN: {tin}')

            models = []
            for k, v in counter.get_counts().items():
                models.append(TINModel(tin=k, count=v))

            return models

        except Exception as e:
            print(f'An error occured parsing TINs: {e}')
            logger.error(f'An error occured parsing TINs: {e}')
            return