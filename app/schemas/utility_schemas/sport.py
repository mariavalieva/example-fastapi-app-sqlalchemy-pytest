from pydantic import BaseModel


class SportSchema(BaseModel):
    name: str

    class Config:
        orm_mode = True
