from fastapi import APIRouter
from schemas.schemas import TradingDate

router = APIRouter(prefix='/historical_data', tags=['Historical Data'], responses={404: {"description": "Not found"}})

@router.post("/one_day")
def get_one_day_data(date: TradingDate):
    """
    Return the data of a given day
    """
    data: list = []
    return data