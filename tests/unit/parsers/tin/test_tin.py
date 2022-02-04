"""Testing module for TIN models."""

from random import randint
from unittest import skip

import pytest
from faker import Faker

from ironhide.parsers.tin import TINParser
from ironhide.models.tin import TINModel


Faker.seed(randint(0, 1000000))
fake = Faker(["en-US"])

# SSNs can be used as a TINs
SSNS = [[fake.ssn("SSN"), "SSN"] for _ in range(50)]
INVALID_NUMS = [[f"{_}{_+3}", "INVALID"] for _ in range(50)]


@pytest.mark.parametrize("tin, tin_type", SSNS)
# @pytest.mark.skip(reason="not testing right now")
def test_tin(tin, tin_type):
    
    assert TINParser.is_valid_tin(tin) is True
    assert tin_type == "SSN"
    
    parsed_list_of_valid_ssns = TINParser.parse(SSNS)

    assert parsed_list_of_valid_ssns
    assert len(parsed_list_of_valid_ssns) == 50

    for tinmodel in parsed_list_of_valid_ssns:
        assert type(tinmodel).__name__ is "TINModel"
        assert tinmodel.count > 0

# @pytest.mark.skip(reason="not testing right now")
def test_duplicate_tins():
    list_of_duplicate_tins = [["500-50-1234", "SSN"], ["500-50-1234", "SSN"], ["999-88-1234", "ITIN"], ["999-88-1234", "ITIN"]]

    parsed_duplicate_tins = TINParser.parse(list_of_duplicate_tins)

    for item in parsed_duplicate_tins:
        assert item.count == 2

# @pytest.mark.skip(reason="not testing right now")
def test_tin_itin():
    # Valid ITIN: 1st digit is 9, 4th/5th digits not in the ranges: 50 – 65, 88, 90 – 92, 94 – 99
    list_of_valid_itins = [["900-50-1234", "ITIN"], ["999-88-1234", "ITIN"]]

    for itin in list_of_valid_itins:
        assert TINParser.is_valid_tin(itin[0]) is True

    parsed_valid_itins = TINParser.parse(list_of_valid_itins)

    assert len(parsed_valid_itins) == 2

# @pytest.mark.skip(reason="not testing right now")
def test_empty_tins():
    empty_string = TINParser.parse("")
    assert len(empty_string) == 0

    empty_list = TINParser.parse([])
    assert len(empty_list) == 0

    mixed_set_of_empty_elements = TINParser.parse([[], ["",""], "", ["", "INVALID"]])
    assert len(mixed_set_of_empty_elements) == 0

# @pytest.mark.skip(reason="not testing right now")
def test_invalid_tins():
    # Build list of invalid TINs
    invalid_tins = []

    # Invalid TIN - SSN: 111-11-1111, 333-33-3333, 666-66-6666, 123-45-6789
    invalid_tins.append(["111-11-1111", "INVALID"])
    invalid_tins.append(["333-33-3333", "INVALID"])
    invalid_tins.append(["666-66-6666", "INVALID"])
    invalid_tins.append(["123-45-6789", "INVALID"])

    # Invalid TIN - SSN: Area Numbers (first 3 digits) - 000, 666
    invalid_tins.append(["000-45-6789", "INVALID"])
    invalid_tins.append(["666-45-6789", "INVALID"])

    # Invalid TIN - SSN: Group Numbers (4th / 5th digits) - 00
    invalid_tins.append(["123-00-6789", "INVALID"])

    # Invalid TIN - SSN: Serial Numbers (last 4 digits) - 0000
    invalid_tins.append(["123-45-0000", "INVALID"])

    # Invalid TIN - ITIN: 1st digit is 9, 4th/5th digits not in the ranges: 50 – 65, 88, 90 – 92, 94 – 99
    invalid_tins.append(["923-45-6789", "INVALID"])
    invalid_tins.append(["923-67-6789", "INVALID"])
    invalid_tins.append(["923-89-6789", "INVALID"])
    invalid_tins.append(["923-93-6789", "INVALID"])

    # invalid format
    invalid_tins.append(["92-345-4444", "INVALID"])
    invalid_tins.append(["92-345-4-444", "INVALID"])
    invalid_tins.append(["923454444", "INVALID"])

    # non-numeric characters
    invalid_tins.append(["abcdefghi", "INVALID"])
    invalid_tins.append(["abc-de-fghi", "INVALID"])

    # non-string TIN
    invalid_tins.append([9234544444, "INVALID"])

    # incorrect number of digits
    invalid_tins.append(["923-45-", "INVALID"])
    invalid_tins.append(["923-45-44444", "INVALID"])

    list_of_invalid_combinations = TINParser.parse(invalid_tins)
    assert len(list_of_invalid_combinations) == 0
