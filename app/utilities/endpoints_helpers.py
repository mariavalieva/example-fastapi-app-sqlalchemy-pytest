from dataclasses import dataclass
from typing import Type

from fastapi.params import Query

from app.models import Base


@dataclass
class FilterData:
    col: str
    value: str | int | Query
    comparison: str
    model: Type[Base] | None = None
