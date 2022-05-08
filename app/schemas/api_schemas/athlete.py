from pydantic import BaseModel, PositiveFloat, PositiveInt

from app.schemas.utility_schemas.team import TeamSchema, TeamUpdateSchema
from app.utilities.enums import Sex


class AthleteBase(BaseModel):
    name: str

    class Config:
        orm_mode = True


class AthleteCreateUpdateSchema(AthleteBase):
    team: TeamUpdateSchema
    sex: Sex
    height: PositiveInt | None = None
    weight: PositiveFloat | None = None

    class Config:
        schema_extra = {
            "example": {
                "name": "Robert Leroux",
                "team": {
                    "noc": "FRA",
                },
                "sex": "M",
                "height": 182,
                "weight": 72,
            }
        }


class MedalAthleteSchema(AthleteBase):
    team: TeamSchema


class MedalAthleteUpdateSchema(AthleteBase):
    ...
