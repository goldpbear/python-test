"""TIN Parser"""
from dataclasses import dataclass

from ironhide.models.model import Model


@dataclass
class TINModel(Model):
    """taxpayer id data model"""

    area_number: str
    group_number: str
    serial_number: str
