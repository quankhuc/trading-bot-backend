from fastapi import APIRouter
from schemas.schemas import TradingDate, HistoricalData
import ast
import json
import glob2
from api import migrate_data
from datetime import datetime
from celery_tasks.tasks import insert_data_task
from celery import group
import csv
from itertools import groupby

router = APIRouter(
    prefix="/migrate_data",
    tags=["Migrate Historical Data"],
    responses={404: {"description": "Not found"}},
)


@router.post("/one_day")
def migrate_one_day_data(date: TradingDate):
    """
    Migrate one day of data into the database

    Args:
        date (TradingDate): date with TradingDate format

    Returns:
        _type_: boolean if the data is inserted or not
    """
    data: list[HistoricalData] = []
    query_date = date.trading_date
    file_name = construct_file_name(query_date)
    data = read_data_into_json(file_name)
    migrate_data.insert_data(data)
    return True


@router.post("/all_days")
def migrate_all_days_data(migrate_confirmation: bool):
    """
    Migrate all data that can be founded in the data folder

    Args:
        migrate_confirmation (bool): it needs a confirmation to migrate all of data because there can be a lot of data in this folder

    Returns:
        _type_: boolean if the data is inserted or not
    """
    if migrate_confirmation is False:
        return False
    list_files = get_list_of_files()
    trading_quotes: list[HistoricalData] = []
    trading_trade: list[HistoricalData] = []
    for index, file in enumerate(list_files):
        print("Process file number: ", index)
        data_list = read_data_into_json(file_name=file)
        for data in data_list:
            if data == {}:
                continue
            data_type = data.get("DataType")
            content = data.get("Content")
            if data_type == "Quote":
                trading_quotes.append(content)
            elif data_type == "Trade":
                trading_trade.append(content)
    trading_quotes = [
        next(v) for _, v in groupby(trading_quotes, key=lambda x: x["TradingDateTime"])
    ]
    trading_trade = [
        next(v) for _, v in groupby(trading_trade, key=lambda x: x["TradingDateTime"])
    ]
    trading_quotes = sorted(
        trading_quotes,
        key=lambda x: datetime.strptime(x["TradingDateTime"], "%Y-%m-%d %H:%M:%S"),
    )
    trading_trade = sorted(
        trading_trade,
        key=lambda x: datetime.strptime(x["TradingDateTime"], "%Y-%m-%d %H:%M:%S"),
    )
    with open("data/trading_quotes.csv", "w", newline="") as f:
        dict_writer = csv.DictWriter(f, trading_quotes[0].keys())
        dict_writer.writeheader()
        dict_writer.writerows(trading_quotes)
    with open("data/trading_trade.csv", "w", newline="") as f:
        dict_writer = csv.DictWriter(f, trading_trade[0].keys())
        dict_writer.writeheader()
        dict_writer.writerows(trading_trade)
    return True


@router.delete("/delete_all_data")
def delete_all_data(delete_confirmation: bool):
    if delete_confirmation is False:
        return False
    migrate_data.delete_all_data()
    return True


def get_list_of_files():
    list_files: list[str] = glob2.glob("data/*.txt", recursive=True)
    sorted_list_files = sorted(
        list_files,
        key=lambda x: datetime.strptime(
            x.split("/")[-1].split("_")[1].replace(".txt", ""), "%d.%m.%Y"
        ),
    )
    return sorted_list_files


def construct_file_name(query_date: str) -> str:
    month = query_date.split("/")[0]
    date = query_date.split("/")[1]
    year = query_date.split("/")[2]
    file_name = f"VN30F20{month}_{date}.{month}.{year}.txt"
    return file_name


def read_data_into_json(file_name: str) -> list[HistoricalData]:
    data: list(HistoricalData) = []
    with open(file_name, "r") as f:
        for line in f:
            json_line: dict = ast.literal_eval(line)
            data_type = json_line.get("DataType")
            if data_type is None:
                data.append({})
                continue
            content = json_line.get("Content")
            if content is None:
                data.append({})
                continue
            content_ = json.loads(content)
            trading_date = content_.get("TradingDate")
            trading_date = trading_date.split("T")[0]
            trading_date_time = f'{trading_date} {content_.get("TradingTime")}'
            content_["TradingDateTime"] = trading_date_time
            content_.pop("TradingDate")
            content_.pop("TradingTime")
            json_data = {"DataType": data_type, "Content": content_}
            data.append(json_data)
    return data
