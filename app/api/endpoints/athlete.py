from typing import Any, Dict, Union

from fastapi import APIRouter, Depends, status
from fastapi.params import Query
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.api.endpoints import base as base_endpoint
from app.crud.athlete import athlete_crud
from app.models import Athlete, Team
from app.schemas.api_schemas.athlete import AthleteCreateUpdateSchema
from app.schemas.api_schemas.connected import AthleteListSchema, AthleteSchema
from app.utilities.endpoints_helpers import FilterData

router = APIRouter()

endpoint_settings = ("Athlete", athlete_crud)


@router.post(
    "/",
    response_model=AthleteSchema,
    response_model_exclude_unset=True,
    status_code=status.HTTP_201_CREATED,
)
def add_athlete(
    *, athlete_in: AthleteCreateUpdateSchema, db: Session = Depends(get_db)
) -> Athlete:
    return base_endpoint.add_object(
        obj_in=athlete_in, db=db, endpoint_settings=endpoint_settings
    )


@router.get(
    "/{athlete_id}", response_model=AthleteSchema, response_model_exclude_unset=True
)
def get_athlete(athlete_id: int, db: Session = Depends(get_db)) -> Athlete | None:
    return base_endpoint.get_object(
        id=athlete_id, db=db, endpoint_settings=endpoint_settings
    )


@router.put(
    "/{athlete_id}", response_model=AthleteSchema, response_model_exclude_unset=True
)
def update_athlete(
    *,
    athlete_id: int,
    athlete_in: Union[AthleteCreateUpdateSchema, Dict[str, Any]],
    db: Session = Depends(get_db)
) -> Athlete:
    return base_endpoint.update_object(
        id=athlete_id, obj_in=athlete_in, db=db, endpoint_settings=endpoint_settings
    )


@router.delete(
    "/{athlete_id}", response_model=AthleteSchema, response_model_exclude_unset=True
)
def delete_athlete(athlete_id: int, db: Session = Depends(get_db)) -> Athlete | None:
    return base_endpoint.delete_object(
        id=athlete_id, db=db, endpoint_settings=endpoint_settings
    )


@router.get("/", response_model=AthleteListSchema)
def get_athlete_list(
    skip: int | None = None,
    limit: int | None = None,
    name: str | Query = Query(None, description="Search query in athlete's name"),
    country: str | None = None,
    db: Session = Depends(get_db),
) -> dict[str, list[Athlete]]:
    filters_dict: dict[str, Any] = {}
    if name:
        filters_dict.setdefault("filters", []).append(FilterData("name", name, "ilike"))
    if country:
        filters_dict.setdefault("join", []).append(Team)
        filters_dict.setdefault("filters", []).append(
            FilterData("region", country, "equal", Team)
        )
    return base_endpoint.get_object_list(
        db=db,
        skip=skip,
        limit=limit,
        filters=filters_dict,
        endpoint_settings=endpoint_settings,
    )
