from app.crud.base import CRUDBase
from app.models import Athlete
from app.schemas.api_schemas.athlete import AthleteCreateUpdateSchema


class CRUDAthlete(CRUDBase[Athlete, AthleteCreateUpdateSchema]):
    ...


athlete_crud = CRUDAthlete(Athlete)
