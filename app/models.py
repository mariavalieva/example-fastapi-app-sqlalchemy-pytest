from typing import Any, List

from sqlalchemy import Column as Col
from sqlalchemy import Enum, Float, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import backref, relationship, validates

from app.utilities.enums import MedalType, Season, Sex


def Column(*args: Any, **kwargs: Any) -> Any:
    kwargs.setdefault("nullable", False)
    return Col(*args, **kwargs)


@as_declarative()
class Base:
    id = Column(Integer, primary_key=True, index=True)
    name: str

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.name}>"

    @classmethod
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"


class Team(Base):
    __table_args__ = (UniqueConstraint("region", "noc", name="_region_noc"),)

    region = Column(String(50))
    noc = Column(String(3))

    athletes: List["Athlete"] = relationship(
        "Athlete", backref=backref("team", lazy="joined")
    )

    def __repr__(self) -> str:
        return f"<Team: {self.region}>"


class Sport(Base):
    name = Column(String(50), unique=True)

    events: List["Event"] = relationship("Event", backref="sport")


class Event(Base):
    name = Column(String(100), unique=True)
    sport_id = Column(Integer, ForeignKey("sports.id"))

    medals: List["Medal"] = relationship(
        "Medal", backref=backref("event", lazy="joined")
    )


class Game(Base):
    __table_args__ = (UniqueConstraint("year", "season", name="_games_name"),)

    year = Column(Integer)
    season = Column(Enum(Season))
    city = Column(String(100))

    medals: List["Medal"] = relationship(
        "Medal", backref=backref("game", lazy="joined")
    )

    @validates("year")
    def validate_year(self, key: Any, year: int) -> int:
        if year < 1896:
            raise ValueError("year must be greater or equal to 1896")
        return year

    def __repr__(self) -> str:
        return f"<Game: {self.year} {self.season}>"


class Athlete(Base):
    name = Column(String(50), unique=True)
    team_id = Column(Integer, ForeignKey("teams.id"))
    sex = Column(Enum(Sex))
    height = Column(Integer, nullable=True)
    weight = Column(Float, nullable=True)

    team: Team = relationship(Team)
    medals: List["Medal"] = relationship(
        "Medal", backref=backref("athlete", lazy="joined")
    )


class Medal(Base):
    __table_args__ = (
        UniqueConstraint(
            "athlete_id", "game_id", "event_id", "medal", name="_games_event_medal"
        ),
    )

    athlete_id = Column(Integer, ForeignKey("athletes.id"))
    game_id = Column(Integer, ForeignKey("games.id"))
    event_id = Column(Integer, ForeignKey("events.id"))
    medal = Column(Enum(MedalType))

    athlete: Athlete = relationship(Athlete)
    game: Game = relationship(Game)
    event: Event = relationship(Event)

    def __repr__(self) -> str:
        return f"<Medal: {self.game.year} {self.game.season} {self.event.name} {self.medal} medal>"
