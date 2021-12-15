"""TIN Parser"""
from dataclasses import dataclass

from ironhide.models.model import Model


@dataclass
class TINModel(Model):
    """taxpayer id data model, holds TIN and a count of that TIN in each roster."""

    tin: str
    count: int
