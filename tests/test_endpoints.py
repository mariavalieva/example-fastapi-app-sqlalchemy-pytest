from typing import List, Tuple

import pytest
from fastapi.encoders import jsonable_encoder
from starlette.testclient import TestClient

from app.models import Athlete, Event, Game
from app.schemas.api_schemas.athlete import AthleteCreateUpdateSchema
from app.schemas.api_schemas.connected import (
    AthleteListSchema,
    AthleteSchema,
    MedalListSchema,
    MedalSchema,
)
from app.schemas.api_schemas.medal import MedalCreateUpdateSchema
from app.utilities.custom_typing_types import ModelFactoryType, ModelType, SchemaType
from tests.schemas_factories import AthleteSchemaFactory, MedalSchemaFactory


def test_add_athlete(
    client: TestClient,
    create_athlete_schema: List[ModelType | SchemaType],
) -> None:
    _, athlete = create_athlete_schema
    response = client.post(
        "/athletes/",
        json=jsonable_encoder(athlete),
    )
    data = response.json()
    assert response.status_code == 201
    assert AthleteSchema(**data)


def test_add_medal(
    client: TestClient,
    create_medal_schema: List[ModelType | SchemaType],
) -> None:
    *_, medal = create_medal_schema
    response = client.post(
        "/medals/",
        json=jsonable_encoder(medal),
    )
    data = response.json()
    assert response.status_code == 201
    assert MedalSchema(**data)


def test_get_athlete(
    client: TestClient,
    athlete_factory: ModelFactoryType,
) -> None:
    item = athlete_factory.create()
    response = client.get(
        f"/athletes/{item.id}",
    )
    data = response.json()
    assert response.status_code == 200
    assert AthleteSchema(**data)


def test_get_medal(
    client: TestClient,
    medal_factory: ModelFactoryType,
) -> None:
    item = medal_factory.create()
    response = client.get(
        f"/medals/{item.id}",
    )
    data = response.json()
    assert response.status_code == 200
    assert MedalSchema(**data)


def test_delete_athlete(
    client: TestClient,
    athlete_factory: ModelFactoryType,
) -> None:
    item = athlete_factory.create()
    response = client.delete(
        f"/athletes/{item.id}",
    )
    data = response.json()
    assert response.status_code == 200
    assert AthleteSchema(**data)


def test_delete_medal(
    client: TestClient,
    medal_factory: ModelFactoryType,
) -> None:
    item = medal_factory.create()
    response = client.delete(
        f"/medals/{item.id}",
    )
    data = response.json()
    assert response.status_code == 200
    assert MedalSchema(**data)


def test_update_athlete(
    client: TestClient,
    athlete_factory: ModelFactoryType,
    create_athlete_schema: Tuple[Athlete, AthleteCreateUpdateSchema],
) -> None:
    athlete = athlete_factory.create()
    _, athlete_in = create_athlete_schema
    response = client.put(f"/athletes/{athlete.id}", json=jsonable_encoder(athlete_in))
    data = response.json()
    assert response.status_code == 200
    assert AthleteSchema(**data)


def test_update_medal(
    client: TestClient,
    medal_factory: ModelFactoryType,
    create_medal_schema: Tuple[Athlete, Game, Event, MedalCreateUpdateSchema],
) -> None:
    medal = medal_factory.create()
    *_, medal_in = create_medal_schema
    response = client.put(f"/medals/{medal.id}", json=jsonable_encoder(medal_in))
    data = response.json()
    assert response.status_code == 200
    assert MedalSchema(**data)


@pytest.mark.parametrize(
    "query_parameter, value",
    [("limit", 5), ("skip", 5), ("name", "test"), ("country", "test")],
)
def test_get_multi_athlete(
    client: TestClient,
    athlete_factory: ModelFactoryType,
    query_parameter: str,
    value: str | int,
) -> None:
    athlete_factory.create_batch(10)
    response = client.get(
        f"/athletes/?{query_parameter}={value}",
    )
    data = response.json()
    assert response.status_code == 200
    assert AthleteListSchema(**data)


@pytest.mark.parametrize(
    "query_parameter, value",
    [
        ("limit", 5),
        ("skip", 5),
        ("athlete", "test"),
        ("event", "test"),
        ("year", 2000),
        ("medal", "test"),
    ],
)
def test_get_multi_medal(
    client: TestClient,
    medal_factory: ModelFactoryType,
    query_parameter: str,
    value: str | int,
) -> None:
    medal_factory.create_batch(10)
    response = client.get(
        f"/medals/?{query_parameter}={value}",
    )
    data = response.json()
    assert response.status_code == 200
    assert MedalListSchema(**data)


@pytest.mark.parametrize(
    "route, method, status_code, message",
    [
        ("athletes", "GET", 404, "Athlete with ID 1 not found"),
        ("athletes", "PUT", 204, "There is no Athlete with ID 1 to update"),
        ("athletes", "DELETE", 204, "There is no Athlete with ID 1 to delete"),
        ("medals", "GET", 404, "Medal with ID 1 not found"),
        ("medals", "PUT", 204, "There is no Medal with ID 1 to update"),
        ("medals", "DELETE", 204, "There is no Medal with ID 1 to delete"),
    ],
)
def test_not_found_item(
    client: TestClient,
    route: str,
    method: str,
    status_code: int,
    message: str,
) -> None:
    if method == "PUT":
        schema = AthleteSchemaFactory if route == "athletes" else MedalSchemaFactory
        response = client.request(
            method, f"/{route}/1", json=jsonable_encoder(schema.build())  # type: ignore
        )
    else:
        response = client.request(method, f"/{route}/1")
    data = response.json()
    assert response.status_code == status_code
    assert data["detail"] == message
