from app.crud.base import CRUDBase
from app.models import Medal
from app.schemas.api_schemas.medal import MedalCreateUpdateSchema


class CRUDMedal(CRUDBase[Medal, MedalCreateUpdateSchema]):
    ...


medal_crud = CRUDMedal(Medal)
