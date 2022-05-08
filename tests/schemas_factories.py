from pydantic_factories import ModelFactory

from app.schemas.api_schemas.athlete import AthleteCreateUpdateSchema
from app.schemas.api_schemas.medal import MedalCreateUpdateSchema


class AthleteSchemaFactory(ModelFactory[AthleteCreateUpdateSchema]):
    __model__ = AthleteCreateUpdateSchema


class MedalSchemaFactory(ModelFactory[MedalCreateUpdateSchema]):
    __model__ = MedalCreateUpdateSchema
