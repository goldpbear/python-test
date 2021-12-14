"""Base class for models"""
from dataclasses import dataclass

from dataclasses_jsonschema import JsonSchemaMixin


@dataclass
class Model(JsonSchemaMixin):
    """Base class for models"""
