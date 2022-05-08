import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.utilities.custom_typing_types import ModelFactoryType


def test_db_team_insert_data(
    db_session: Session, team_factory: ModelFactoryType
) -> None:
    result = team_factory.create(region="New Zealand", noc="NZL")
    assert result.region == "New Zealand"
    assert result.noc == "NZL"
    assert repr(result) == "<Team: New Zealand>"


def test_db_team_region_noc_uniqueness_integrity(
    db_session: Session, team_factory: ModelFactoryType
) -> None:
    team_factory.create(region="not_unique_region", noc="NUR")
    with pytest.raises(IntegrityError):
        team_factory.create(region="not_unique_region", noc="NUR")


def test_db_sport_insert_data(
    db_session: Session, sport_factory: ModelFactoryType
) -> None:
    result = sport_factory.create(name="sport_1")
    assert result.name == "sport_1"
    assert repr(result) == "<Sport: sport_1>"


def test_db_sport_name_uniqueness_integrity(
    db_session: Session, sport_factory: ModelFactoryType
) -> None:
    sport_factory.create(name="not_unique")
    with pytest.raises(IntegrityError):
        sport_factory.create(name="not_unique")


def test_db_event_insert_data(
    db_session: Session,
    event_factory: ModelFactoryType,
    sport_factory: ModelFactoryType,
) -> None:
    sport = sport_factory.build()
    result = event_factory.create(name="event_1", sport=sport)
    assert result.name == "event_1"
    assert result.sport == sport
    assert repr(result) == "<Event: event_1>"


def test_db_event_name_uniqueness_integrity(
    db_session: Session, event_factory: ModelFactoryType
) -> None:
    event_factory.create(name="not_unique")
    with pytest.raises(IntegrityError):
        event_factory.create(name="not_unique")


def test_db_game_insert_data(
    db_session: Session, game_factory: ModelFactoryType
) -> None:
    result = game_factory.create(year=2000, season="Summer", city="Sydney")
    assert result.year == 2000
    assert result.season == "Summer"
    assert result.city == "Sydney"
    assert repr(result) == "<Game: 2000 Summer>"


def test_db_game_year_season_uniqueness_integrity(
    db_session: Session, game_factory_not_get_or_create: ModelFactoryType
) -> None:
    game_factory_not_get_or_create.create(year=2000, season="Summer")
    with pytest.raises(IntegrityError):
        game_factory_not_get_or_create.create(year=2000, season="Summer")


def test_db_game_db_year_validation(
    db_session: Session, game_factory: ModelFactoryType
) -> None:
    with pytest.raises(ValueError):
        game_factory.create(year=1890)


def test_db_athlete_insert_data(
    db_session: Session,
    athlete_factory: ModelFactoryType,
    team_factory: ModelFactoryType,
) -> None:
    team = team_factory.build()
    result = athlete_factory.create(
        name="Jane Smith", team=team, sex="F", height=169, weight=58.5
    )
    assert result.name == "Jane Smith"
    assert result.team == team
    assert result.sex == "F"
    assert result.height == 169
    assert result.weight == 58.5
    assert repr(result) == "<Athlete: Jane Smith>"


def test_db_athlete_name_uniqueness_integrity(
    db_session: Session, athlete_factory: ModelFactoryType
) -> None:
    athlete_factory.create(name="not_unique")
    with pytest.raises(IntegrityError):
        athlete_factory.create(name="not_unique")


def test_db_medal_insert_data(
    db_session: Session,
    medal_factory: ModelFactoryType,
    athlete_factory: ModelFactoryType,
    event_factory: ModelFactoryType,
    game_factory: ModelFactoryType,
) -> None:
    athlete = athlete_factory.build()
    event = event_factory.build()
    game = game_factory.build()
    result = medal_factory.create(athlete=athlete, event=event, game=game, medal="Gold")
    assert result.athlete == athlete
    assert result.event == event
    assert result.game == game
    assert result.medal == "Gold"
    assert repr(result) == f"<Medal: {game.year} {game.season} {event.name} Gold medal>"


def test_db_medal_uniqueness_integrity(
    db_session: Session,
    medal_factory: ModelFactoryType,
    athlete_factory: ModelFactoryType,
    game_factory: ModelFactoryType,
    event_factory: ModelFactoryType,
) -> None:
    athlete = athlete_factory.build()
    game = game_factory.build()
    event = event_factory.build()
    medal_factory.create(athlete=athlete, game=game, event=event, medal="Bronze")
    with pytest.raises(IntegrityError):
        medal_factory.create(athlete=athlete, game=game, event=event, medal="Bronze")
