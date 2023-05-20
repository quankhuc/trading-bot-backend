import json
import httpx
from schemas.schemas import HistoricalData
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv(dotenv_path='../.env')

# read from .env file
url:str = os.getenv('SUPABASE_URL')
key:str = os.getenv('SUPABASE_KEY')
supabase:Client = create_client(url, key)

def insert_one_day_data(data: HistoricalData) -> HistoricalData:
    print('insert_one_day_data ', data)
    
