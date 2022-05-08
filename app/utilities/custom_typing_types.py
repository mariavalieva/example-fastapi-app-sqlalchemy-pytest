from typing import TypeVar

from pydantic import BaseModel

from app.models import Base
from tests.models_factories import BaseSQLAlchemyModelFactory

ModelType = TypeVar("ModelType", bound=Base)
SchemaType = TypeVar("SchemaType", bound=BaseModel)
ModelFactoryType = TypeVar("ModelFactoryType", bound=BaseSQLAlchemyModelFactory)
