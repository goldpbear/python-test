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
