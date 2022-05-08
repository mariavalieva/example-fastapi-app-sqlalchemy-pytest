from typing import Any, Dict, Union

from fastapi import APIRouter, Depends, status
from fastapi.params import Query
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.api.endpoints import base as base_endpoint
from app.crud.medal import medal_crud
from app.models import Athlete, Event, Game, Medal
from app.schemas.api_schemas.connected import MedalListSchema, MedalSchema
from app.schemas.api_schemas.medal import MedalCreateUpdateSchema
from app.utilities.endpoints_helpers import FilterData

router = APIRouter()

endpoint_settings = ("Medal", medal_crud)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=MedalSchema,
    response_model_exclude_unset=True,
)
def add_medal(
    *, medal_in: MedalCreateUpdateSchema, db: Session = Depends(get_db)
) -> Medal:
    return base_endpoint.add_object(
        obj_in=medal_in, db=db, endpoint_settings=endpoint_settings
    )


@router.get(
    "/{medal_id}", response_model=MedalSchema, response_model_exclude_unset=True
)
def get_medal(medal_id: int, db: Session = Depends(get_db)) -> Medal | None:
    return base_endpoint.get_object(
        id=medal_id, db=db, endpoint_settings=endpoint_settings
    )


@router.put(
    "/{medal_id}", response_model=MedalSchema, response_model_exclude_unset=True
)
def update_medal(
    *,
    medal_id: int,
    medal_in: Union[MedalCreateUpdateSchema, Dict[str, Any]],
    db: Session = Depends(get_db)
) -> Medal:
    return base_endpoint.update_object(
        id=medal_id, obj_in=medal_in, db=db, endpoint_settings=endpoint_settings
    )


@router.delete(
    "/{medal_id}", response_model=MedalSchema, response_model_exclude_unset=True
)
def delete_medal(medal_id: int, db: Session = Depends(get_db)) -> Medal | None:
    return base_endpoint.delete_object(
        id=medal_id, db=db, endpoint_settings=endpoint_settings
    )


@router.get("/", response_model=MedalListSchema)
def get_medal_list(
    skip: int | None = None,
    limit: int | None = None,
    medal: str | None = None,
    athlete: str | Query = Query(None, description="Search query in athlete's name"),
    event: str | Query = Query(None, description="Search query in event"),
    year: int | None = None,
    db: Session = Depends(get_db),
) -> dict[str, list[Medal]]:
    filters_dict: dict[str, Any] = {}
    if medal:
        filters_dict.setdefault("filters", []).append(
            FilterData("medal", medal, "equal")
        )
    if athlete:
        filters_dict.setdefault("join", []).append(Athlete)
        filters_dict.setdefault("filters", []).append(
            FilterData("name", athlete, "ilike", Athlete)
        )
    if event:
        filters_dict.setdefault("join", []).append(Event)
        filters_dict.setdefault("filters", []).append(
            FilterData("name", event, "ilike", Event)
        )
    if year:
        filters_dict.setdefault("join", []).append(Game)
        filters_dict.setdefault("filters", []).append(
            FilterData("year", year, "equal", Game)
        )
    return base_endpoint.get_object_list(
        db=db,
        skip=skip,
        limit=limit,
        filters=filters_dict,
        endpoint_settings=endpoint_settings,
    )
