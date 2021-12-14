"""Testing module for social security models."""

from random import randint

import pytest
from faker import Faker

from optimus.parsers.tin import TINParser


Faker.seed(randint(0, 1000000))
fake = Faker(["en-US"])

SSNS = [[fake.ssn("SSN"), "SSN"] for _ in range(50)]
INVALID_NUMS = [[f"{_}{_+3}", "INVALID"] for _ in range(50)]
ITINS = [[fake.ssn("ITIN"), "ITIN"] for _ in range(50)]
EINS = [[fake.ssn("EIN"), "EIN"] for _ in range(50)]


@pytest.mark.parametrize("tin, tin_type", ITINS)
def test_tin(tin, tin_type):
    # TODO: add tests
    pass
