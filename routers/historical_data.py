from fastapi import APIRouter
from schemas.schemas import TradingDate, TradingYear
from api.historical_data import *
import asyncio

router = APIRouter(
    prefix="/historical_data",
    tags=["Historical Data"],
    responses={404: {"description": "Not found"}},
)


@router.post("/one_day")
def get_one_day_data(date: TradingDate):
    """
    Return the data of a given day
    """
    date_with_start_time = date.trading_date + " 00:00:00"
    date_with_end_time = date.trading_date + " 23:59:59"
    data_dataframe = find_data_between_time(date_with_start_time, date_with_end_time)
    return data_dataframe.to_dict(orient="records")


@router.post("/one_year")
def get_one_year_data(year: TradingYear):
    """
    Return the data of a given year
    """
    start_time = year.trading_year + "-01-01 00:00:00"
    end_time = year.trading_year + "-12-31 23:59:59"
    # data_dataframe = find_data_between_time(start_time, end_time)
    df = find_data_between_time(start_time, end_time)
    if len(df) == 0:
        return {"message": "No data found", "data": []}
    # return {"data": df.to_dict(orient="records"), "message": "Success"}
    head_dataframe = df.head(1)
    return {"message": "Success", "data": head_dataframe.to_dict(orient="records")}
