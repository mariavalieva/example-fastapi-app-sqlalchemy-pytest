from typing import Any, Dict, Tuple, Union

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.utilities.custom_typing_types import ModelType, SchemaType


def add_object(
    *,
    obj_in: SchemaType,
    db: Session,
    endpoint_settings: Tuple[str, CRUDBase[ModelType, SchemaType]],
) -> ModelType:
    obj_name, crud = endpoint_settings
    result = crud.create(db=db, obj_in=obj_in)

    return result


def get_object(
    id: int, db: Session, endpoint_settings: Tuple[str, CRUDBase[ModelType, SchemaType]]
) -> Any:
    obj_name, crud = endpoint_settings
    result = crud.get(db=db, id=id)
    if not result:
        raise HTTPException(
            status_code=404, detail=f"{obj_name} with ID {id} not found"
        )

    return result


def update_object(
    *,
    id: int,
    obj_in: Union[SchemaType, Dict[str, Any]],
    db: Session,
    endpoint_settings: Tuple[str, CRUDBase[ModelType, SchemaType]],
) -> ModelType:
    obj_name, crud = endpoint_settings
    obj = crud.get(db=db, id=id)
    if not obj:
        raise HTTPException(
            status_code=204, detail=f"There is no {obj_name} with ID {id} to update"
        )

    result = crud.update(db=db, db_obj=obj, obj_in=obj_in)

    return result


def delete_object(
    id: int, db: Session, endpoint_settings: Tuple[str, CRUDBase[ModelType, SchemaType]]
) -> Any:
    obj_name, crud = endpoint_settings
    result = crud.delete(db=db, id=id)
    if not result:
        raise HTTPException(
            status_code=204, detail=f"There is no {obj_name} with ID {id} to delete"
        )

    return result


def get_object_list(
    db: Session,
    skip: int | None,
    limit: int | None,
    filters: dict[str, Any],
    endpoint_settings: Tuple[str, CRUDBase[ModelType, SchemaType]],
) -> dict[str, list[ModelType]]:
    obj_name, crud = endpoint_settings
    if skip:
        filters["skip"] = skip
    if limit:
        filters["limit"] = limit
    results = crud.get_multi(db=db, **filters)
    return {"results": results}
