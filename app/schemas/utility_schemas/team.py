from pydantic import BaseModel, Field


class TeamBase(BaseModel):
    noc: str = Field(..., min_length=3, max_length=3)


class TeamUpdateSchema(TeamBase):
    ...


class TeamSchema(TeamBase):
    region: str

    class Config:
        orm_mode = True
