from fastapi import APIRouter
from schemas.schemas import TradingDate, HistoricalData
import ast
import json
import glob2
from api import migrate_data
from datetime import datetime
from celery_tasks.tasks import insert_data_task
from celery import group

router = APIRouter(prefix='/migrate_data', tags=['Migrate Historical Data'], responses={404: {"description": "Not found"}})


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
    # for index, file in enumerate(list_files):
    #     print("Process file number: ", index)
    #     data = read_data_into_json(file)
    #     migrate_data.insert_data(data)
    tasks = []
    for index, file in enumerate(list_files):
        print("Process file number: ", index)
        data_list = read_data_into_json(file_name=file)
        for data in data_list:
            tasks.append(insert_data_task.s(data))
        job = group(tasks)
        result = job.apply_async()
        ret_values = result.get(disable_sync_subtasks=False)
    for result in ret_values:
        data.update(result)
    return data

@router.delete("/delete_all_data")
def delete_all_data(delete_confirmation: bool):
    if delete_confirmation is False:
        return False
    migrate_data.delete_all_data()
    return True

def get_list_of_files():
    list_files:list[str] = glob2.glob("data/*.txt", recursive=True)
    sorted_list_files = sorted(list_files, key=lambda x: datetime.strptime(x.split("/")[-1].split("_")[1].replace(".txt", ""), '%d.%m.%Y'))
    return sorted_list_files
       
def construct_file_name(query_date: str) -> str:
    month = query_date.split('/')[0]
    date = query_date.split('/')[1]
    year = query_date.split('/')[2]
    file_name = f'VN30F20{month}_{date}.{month}.{year}.txt'
    return file_name

def read_data_into_json(file_name: str) -> list[HistoricalData]:
    data: list(HistoricalData) = []
    with open(file_name, 'r') as f:
        for line in f:
            json_line:dict = ast.literal_eval(line)
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
            trading_date = trading_date.split('T')[0]
            content_["TradingDate"] = trading_date
            json_data = {
                "DataType": data_type,
                "Content": content_
            }
            data.append(json_data)
    return data
    