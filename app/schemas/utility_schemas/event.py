from pydantic import BaseModel

from app.schemas.utility_schemas.sport import SportSchema


class EventBase(BaseModel):
    name: str


class EventUpdateSchema(EventBase):
    ...


class EventSchema(EventBase):
    sport: SportSchema

    class Config:
        orm_mode = True
