from pydantic import BaseModel, Field

from app.utilities.enums import Season


class GameBase(BaseModel):
    year: int = Field(..., ge=1896)
    season: Season


class GameUpdateSchema(GameBase):
    ...


class GameSchema(GameBase):
    city: str

    class Config:
        orm_mode = True
