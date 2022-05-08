from copy import deepcopy
from typing import Tuple

from faker import Faker
from sqlalchemy.orm import Session

from app.crud.athlete import athlete_crud
from app.crud.medal import medal_crud
from app.models import Athlete, Event, Game, Medal, Team
from app.schemas.api_schemas.athlete import AthleteCreateUpdateSchema
from app.schemas.api_schemas.medal import MedalCreateUpdateSchema
from app.utilities.custom_typing_types import ModelFactoryType
from app.utilities.endpoints_helpers import FilterData


def test_athlete_create(
    db_session: Session,
    create_athlete_schema: Tuple[Athlete, AthleteCreateUpdateSchema],
) -> None:
    team, obj_in = create_athlete_schema
    item = athlete_crud.create(db_session, obj_in=obj_in)

    assert item.name == obj_in.name
    assert item.team == team
    assert item.sex == obj_in.sex
    assert item.height == obj_in.height
    assert item.weight == obj_in.weight


def test_medal_create(
    db_session: Session,
    create_medal_schema: Tuple[Athlete, Game, Event, MedalCreateUpdateSchema],
) -> None:
    athlete, game, event, obj_in = create_medal_schema
    item = medal_crud.create(db_session, obj_in=obj_in)

    assert item.athlete == athlete
    assert item.game == game
    assert item.event == event
    assert item.medal == obj_in.medal


def test_athlete_get(db_session: Session, athlete_factory: ModelFactoryType) -> None:
    item = athlete_factory.create()
    item2 = athlete_crud.get(db_session, id=item.id)
    assert item == item2


def test_medal_get(db_session: Session, medal_factory: ModelFactoryType) -> None:
    item = medal_factory.create()
    item2 = medal_crud.get(db_session, id=item.id)
    assert item == item2


def test_athlete_delete(db_session: Session, athlete_factory: ModelFactoryType) -> None:
    id = athlete_factory.create().id
    assert athlete_crud.get(db_session, id=id)
    athlete_crud.delete(db_session, id=id)
    assert not athlete_crud.get(db_session, id=id)


def test_medal_delete(db_session: Session, medal_factory: ModelFactoryType) -> None:
    id = medal_factory.create().id
    assert medal_crud.get(db_session, id=id)
    medal_crud.delete(db_session, id=id)
    assert not medal_crud.get(db_session, id=id)


def test_athlete_update(
    db_session: Session,
    athlete_factory: ModelFactoryType,
    create_athlete_schema: Tuple[Athlete, AthleteCreateUpdateSchema],
) -> None:
    item_id = athlete_factory.create().id

    team_in, obj_in = create_athlete_schema

    item = db_session.query(Athlete).get(item_id)
    item_old = deepcopy(item)

    item_updated = athlete_crud.update(db_session, db_obj=item, obj_in=obj_in)
    assert item_updated.name == obj_in.name
    assert item_updated.team == team_in
    assert item_updated.sex == obj_in.sex
    assert item_updated.height == obj_in.height
    assert item_updated.weight == obj_in.weight
    assert item_updated.id == item_id
    assert item_updated is not item_old


def test_medal_update(
    db_session: Session,
    medal_factory: ModelFactoryType,
    create_medal_schema: Tuple[Athlete, Game, Event, MedalCreateUpdateSchema],
) -> None:
    item_id = medal_factory.create().id

    athlete_in, game_in, event_in, obj_in = create_medal_schema

    item = db_session.query(Medal).get(item_id)
    item_old = deepcopy(item)

    item_updated = medal_crud.update(db_session, db_obj=item, obj_in=obj_in)
    assert item_updated.medal == obj_in.medal
    assert item_updated.athlete == athlete_in
    assert item_updated.game == game_in
    assert item_updated.event == event_in
    assert item_updated.id == item_id
    assert item_updated is not item_old


def test_athlete_list_skip_limit(
    db_session: Session, athlete_factory: ModelFactoryType
) -> None:
    for i in range(1, 20):
        athlete_factory.create(name=f"item{i}")
    item_list = athlete_crud.get_multi(db_session, skip=5, limit=8)
    for i, item in enumerate(item_list, start=6):
        assert item.name == f"item{i}"
    assert len(item_list) == 8


def test_athlete_list_country(
    db_session: Session,
    athlete_factory: ModelFactoryType,
    team_factory: ModelFactoryType,
) -> None:
    athlete_factory.create_batch(10)
    team = team_factory.create(region="test_country", noc="TCN")
    for _ in range(5):
        athlete_factory.create(team=team)
    item_list = athlete_crud.get_multi(
        db_session,
        join=[Team],
        filters=[FilterData("region", "test_country", "equal", Team)],
    )
    for item in item_list:
        assert item.team.region == "test_country"
    assert len(item_list) == 5


def test_athlete_list_name(
    db_session: Session, athlete_factory: ModelFactoryType
) -> None:
    athlete_factory.create_batch(10)
    for _ in range(5):
        athlete_factory.create(
            name=Faker().first_name() + " test_name " + Faker().last_name()
        )
    item_list = athlete_crud.get_multi(
        db_session, filters=[FilterData("name", "test_name", "ilike")]
    )
    for item in item_list:
        assert "test_name" in item.name
    assert len(item_list) == 5


def test_medal_list_medal(db_session: Session, medal_factory: ModelFactoryType) -> None:
    medal_factory.create_batch(4, medal="Bronze")
    medal_factory.create_batch(6, medal="Silver")
    medal_factory.create_batch(5, medal="Gold")
    item_list = medal_crud.get_multi(
        db_session, filters=[FilterData("medal", "Gold", "equal")]
    )
    for item in item_list:
        assert item.medal == "Gold"
    assert len(item_list) == 5


def test_medal_list_athlete(
    db_session: Session,
    medal_factory: ModelFactoryType,
    athlete_factory: ModelFactoryType,
) -> None:
    medal_factory.create_batch(10)
    athlete = athlete_factory.create(
        name=Faker().first_name() + " test_name " + Faker().last_name()
    )

    for _ in range(5):
        medal_factory.create(athlete=athlete)

    item_list = medal_crud.get_multi(
        db_session,
        join=[Athlete],
        filters=[FilterData("name", "test_name", "ilike", Athlete)],
    )
    for item in item_list:
        assert "test_name" in item.athlete.name
    assert len(item_list) == 5


def test_medal_list_event(
    db_session: Session,
    medal_factory: ModelFactoryType,
    event_factory: ModelFactoryType,
) -> None:
    medal_factory.create_batch(10)
    event = event_factory.create(name=Faker().word() + " test_name " + Faker().word())

    for _ in range(5):
        medal_factory.create(event=event)

    item_list = medal_crud.get_multi(
        db_session,
        join=[Event],
        filters=[FilterData("name", "test_name", "ilike", Event)],
    )
    for item in item_list:
        assert "test_name" in item.event.name
    assert len(item_list) == 5


def test_medal_list_year(
    db_session: Session, medal_factory: ModelFactoryType, game_factory: ModelFactoryType
) -> None:
    game_2000 = game_factory.create(year=2000)
    game_2004 = game_factory.create(year=2004)
    game_2008 = game_factory.create(year=2008)

    medal_factory.create_batch(4, game=game_2000)
    medal_factory.create_batch(6, game=game_2004)
    medal_factory.create_batch(5, game=game_2008)

    item_list = medal_crud.get_multi(
        db_session, join=[Game], filters=[FilterData("year", 2008, "equal", Game)]
    )
    for item in item_list:
        assert item.game.year == 2008
    assert len(item_list) == 5
