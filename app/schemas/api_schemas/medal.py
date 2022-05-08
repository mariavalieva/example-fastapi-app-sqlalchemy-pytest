from pydantic import BaseModel

from app.schemas.api_schemas.athlete import MedalAthleteUpdateSchema
from app.schemas.utility_schemas.event import EventBase, EventSchema, EventUpdateSchema
from app.schemas.utility_schemas.game import GameBase, GameSchema, GameUpdateSchema
from app.utilities.enums import MedalType


class MedalBase(BaseModel):
    game: GameBase
    event: EventBase
    medal: MedalType

    class Config:
        orm_mode = True


class AthleteMedalSchema(MedalBase):
    game: GameSchema
    event: EventSchema


class MedalCreateUpdateSchema(MedalBase):
    athlete: MedalAthleteUpdateSchema
    game: GameUpdateSchema
    event: EventUpdateSchema

    class Config:
        schema_extra = {
            "example": {
                "game": {
                    "year": 2000,
                    "season": "Summer",
                },
                "event": {
                    "name": "Fencing Men's Foil, Individual",
                },
                "medal": "Bronze",
                "athlete": {
                    "name": "Dmitry Stepanovich Shevchenko",
                },
            }
        }
