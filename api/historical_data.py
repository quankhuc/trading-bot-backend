import json
import httpx
from schemas.schemas import HistoricalData, ContentQuote, ContentTrade
import os
from supabase import create_client, Client
from dotenv import load_dotenv
import pandas as pd
import numpy as np
from supafunc import FunctionsClient
import asyncio
from datetime import datetime

load_dotenv(dotenv_path="../.env")

# read from .env file
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)
func = supabase.functions()


def insert_one_day_data(data: HistoricalData) -> HistoricalData:
    print("insert_one_day_data ", data)

def find_data_between_time(start_time: str, end_time: str) -> pd.DataFrame:
    try:
        quote_res, trade_res = get_quote_and_trade_between(start_time, end_time)
        quote_dataframe = pd.DataFrame(quote_res)
        trade_dataframe = pd.DataFrame(trade_res)
        if len(quote_dataframe) == 0 and len(trade_dataframe) == 0:
            return pd.DataFrame()
        quote_trade_dataframe = pd.merge(quote_dataframe, trade_dataframe, how="outer")
        quote_trade_dataframe = quote_trade_dataframe.sort_values(
            by=["TradingDateTime"]
        )
        quote_trade_dataframe = quote_trade_dataframe.fillna(np.nan).ffill().bfill()
        quote_trade_dataframe = quote_trade_dataframe.dropna(axis=1, how="all")
        return quote_trade_dataframe
    except Exception as e:
        print(e)
        return pd.DataFrame()

def get_quote_and_trade_between(start_time: str, end_time: str) -> tuple[list[ContentQuote], list[ContentTrade]]:
    try:
        quote_res = supabase.table("ContentQuote").select("*").range(70000, 1800000).execute()
        trade_res = supabase.table("ContentTrade").select("*").range(2000, 3000).execute()
        return quote_res.data, trade_res.data
    except Exception as e:
        print(e)
        return [], []
    