from typing import Any, List, Sequence

from pydantic import BaseModel, PositiveFloat, PositiveInt, validator

from app.schemas.api_schemas.athlete import AthleteBase, MedalAthleteSchema
from app.schemas.api_schemas.medal import AthleteMedalSchema, MedalBase
from app.schemas.utility_schemas.team import TeamSchema
from app.utilities.enums import Sex


class MedalSchema(MedalBase):
    id: int
    athlete: MedalAthleteSchema

    @validator("athlete", always=True)
    def medal_athlete(
        cls, name_value: MedalAthleteSchema, values: Any
    ) -> dict[str, Any]:
        return {
            "name": name_value.name,
            "team": {"region": name_value.team.region, "noc": name_value.team.noc},
        }

    class Config:
        schema_extra = {
            "example": {
                "game": {"year": 2000, "season": "Summer", "city": "Sydney"},
                "event": {
                    "name": "Fencing Men's Foil, Individual",
                    "sport": {"name": "Fencing"},
                },
                "medal": "Bronze",
                "athlete": {
                    "name": "Dmitry Stepanovich Shevchenko",
                    "team": {"noc": "RUS", "region": "Russia"},
                },
            }
        }


class AthleteSchema(AthleteBase):
    id: int
    team: TeamSchema
    sex: Sex
    height: PositiveInt | None = None
    weight: PositiveFloat | None = None
    medals: List[AthleteMedalSchema] | None = None

    class Config:
        schema_extra = {
            "example": {
                "name": "Robert Leroux",
                "team": {"noc": "FRA", "region": "France"},
                "medals": [
                    {
                        "game": {"year": 1996, "season": "Summer", "city": "Atlanta"},
                        "event": {
                            "name": "Fencing Men's epee, Team",
                            "sport": {"name": "Fencing"},
                        },
                        "medal": "Bronze",
                    }
                ],
                "sex": "M",
                "height": 182,
                "weight": 72,
            }
        }


class AthleteListSchema(BaseModel):
    results: Sequence[AthleteSchema]


class MedalListSchema(BaseModel):
    results: Sequence[MedalSchema]
