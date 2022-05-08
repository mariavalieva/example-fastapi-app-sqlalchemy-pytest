import re
from typing import Any, Dict, Generic, List, Type, Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy import inspect
from sqlalchemy.orm import Session

from app.models import Base
from app.utilities.custom_typing_types import ModelType, SchemaType
from app.utilities.endpoints_helpers import FilterData


class CRUDBase(Generic[ModelType, SchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def __prepare_nested_data(
        self, db: Session, obj_in: SchemaType | dict[str, Any]
    ) -> dict[str, Any]:
        obj_in_data = jsonable_encoder(obj_in)
        relationships = [
            rel
            for rel in inspect(self.model).relationships
            if rel.key in obj_in_data.keys()
        ]
        for rel in relationships:
            rel_cls = rel.mapper.class_
            obj_in_data[rel.key] = (
                db.query(rel_cls).filter_by(**obj_in_data[rel.key]).first()
            )
        return obj_in_data

    def create(self, db: Session, *, obj_in: SchemaType) -> ModelType:
        obj_in_data = self.__prepare_nested_data(db, obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get(self, db: Session, id: Any) -> ModelType | None:
        return db.query(self.model).get(id)

    def get_multi(
        self,
        db: Session,
        *,
        join: List[Type[Base]] = None,
        filters: List[FilterData] = None,
        skip: int = 0,
        limit: int = 50
    ) -> List[ModelType]:
        q = db.query(self.model)
        if join:
            q = q.join(*join)
        if filters:
            for f in filters:
                f.model = f.model or self.model
                if f.comparison == "equal":
                    q = q.filter(getattr(f.model, f.col) == f.value)
                elif f.comparison == "ilike":
                    query = re.sub(r"\s+", "", str(f.value))
                    q = q.filter(getattr(f.model, f.col).ilike("%" + query + "%"))
        return q.offset(skip).limit(limit).all()

    def update(
        self, db: Session, *, db_obj: Any, obj_in: Union[SchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        update_data = self.__prepare_nested_data(db, update_data)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, id: Any) -> ModelType | None:
        obj = db.query(self.model).get(id)
        if not obj:
            return None
        db.delete(obj)
        db.commit()
        return obj
