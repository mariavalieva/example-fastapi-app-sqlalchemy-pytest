import factory
from factory import Faker
from factory.fuzzy import FuzzyChoice, FuzzyInteger
from pytest_factoryboy import register

from app import models
from app.db import TestingSessionLocal
from app.utilities.enums import MedalType, Season, Sex


class BaseSQLAlchemyModelFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        sqlalchemy_session = TestingSessionLocal
        sqlalchemy_session_persistence = "commit"


@register
class TeamFactory(BaseSQLAlchemyModelFactory):
    class Meta:
        model = models.Team

    region = Faker("country")
    noc = Faker("country_code", representation="alpha-3")


@register
class SportFactory(BaseSQLAlchemyModelFactory):
    class Meta:
        model = models.Sport

    name = factory.Sequence(lambda n: "sport_%d" % n)


@register
class EventFactory(BaseSQLAlchemyModelFactory):
    class Meta:
        model = models.Event

    name = factory.Sequence(lambda n: "event_%d" % n)
    sport = factory.SubFactory(SportFactory)


@register
class GameFactory(BaseSQLAlchemyModelFactory):
    class Meta:
        model = models.Game
        sqlalchemy_get_or_create = ("year", "season")

    year = FuzzyInteger(1896, 2050)
    season = FuzzyChoice(Season.__members__.values())
    city = Faker("city")


@register
class GameFactoryNotGetOrCreate(GameFactory):
    class Meta:
        sqlalchemy_get_or_create = None


@register
class AthleteFactory(BaseSQLAlchemyModelFactory):
    class Meta:
        model = models.Athlete

    name = Faker("name")
    team = factory.SubFactory(TeamFactory)
    sex = FuzzyChoice(Sex.__members__.values())
    height = FuzzyInteger(150, 220)
    weight = Faker("pyfloat", right_digits=1, min_value=50, max_value=120)


@register
class MedalFactory(BaseSQLAlchemyModelFactory):
    class Meta:
        model = models.Medal

    athlete = factory.SubFactory(AthleteFactory)
    game = factory.SubFactory(GameFactory)
    event = factory.SubFactory(EventFactory)
    medal = FuzzyChoice(MedalType.__members__.values())
