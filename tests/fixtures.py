from typing import Any, Generator, Tuple

import pytest
from fastapi import FastAPI
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from app.api.dependencies import get_db
from app.db import TestingSessionLocal, sqlalchemy_engine
from app.main import get_application
from app.models import Athlete, Base, Event, Game, Team
from app.schemas.api_schemas.athlete import AthleteCreateUpdateSchema
from app.schemas.api_schemas.medal import MedalCreateUpdateSchema
from tests.models_factories import (
    AthleteFactory,
    EventFactory,
    GameFactory,
    TeamFactory,
)
from tests.schemas_factories import AthleteSchemaFactory, MedalSchemaFactory


@pytest.fixture(scope="module")
def app() -> Generator[FastAPI, Any, None]:
    Base.metadata.create_all(sqlalchemy_engine)
    _app = get_application()
    yield _app
    Base.metadata.drop_all(sqlalchemy_engine)


@pytest.fixture(scope="function")
def db_session(app: FastAPI) -> Generator[Session, Any, None]:
    connection = sqlalchemy_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session

    session.close()
    transaction.rollback()
    connection.close()
    TestingSessionLocal.remove()


@pytest.fixture()
def client(app: FastAPI, db_session: Session) -> Generator[TestClient, Any, None]:
    def _get_test_db() -> Generator[Session, Any, None]:
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client


@pytest.fixture()
def create_athlete_schema(
    team_factory: TeamFactory,
) -> Tuple[Team, AthleteCreateUpdateSchema]:
    team = team_factory.create()
    athlete = AthleteSchemaFactory.build(team={"noc": team.noc})
    return team, athlete


@pytest.fixture()
def create_medal_schema(
    athlete_factory: AthleteFactory,
    game_factory: GameFactory,
    event_factory: EventFactory,
) -> Tuple[Athlete, Game, Event, MedalCreateUpdateSchema]:
    athlete = athlete_factory.create()
    game = game_factory.create()
    event = event_factory.create()
    medal = MedalSchemaFactory.build(
        athlete={"name": athlete.name},
        game={"year": game.year, "season": game.season},
        event={"name": event.name},
    )
    return athlete, game, event, medal
