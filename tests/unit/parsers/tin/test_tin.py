"""Testing module for TIN models."""

from random import randint

import pytest
from faker import Faker

from optimus.parsers.tin import TINParser
from optimus.models.tin import TINModel


Faker.seed(randint(0, 1000000))
fake = Faker(["en-US"])

# SSNs can be used as a TINs
SSNS = [[fake.ssn("SSN"), "SSN"] for _ in range(50)]
INVALID_NUMS = [[f"{_}{_+3}", "INVALID"] for _ in range(50)]


@pytest.mark.parametrize("tin, tin_type", SSNS)
def test_tin(tin, tin_type):
    # TODO: add tests
    pass
