"""Testing module for TIN models."""

from random import randint

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
