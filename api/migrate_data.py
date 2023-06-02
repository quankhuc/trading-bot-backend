from dotenv import load_dotenv
import os
from supabase import create_client, Client
from schemas.schemas import HistoricalData


load_dotenv()
url: str = os.getenv('SUPABASE_URL')
key: str = os.getenv('SUPABASE_KEY')
supabase: Client = create_client(url, key)

def insert_data(data: HistoricalData):
    try: 
        data_type = data.get("DataType")
        content = data.get("Content")
        if content is None or data_type is None:
            return False
        if data_type == "Trade":
            data, count = supabase.table("ContentTrade").insert(content).execute()
            return True
        elif data_type == "Quote":
            data, count = supabase.table("ContentQuote").insert(content).execute()
            return True
    except Exception as e:
        print(e)
        return False

def delete_all_data():
    _, content_trade_length = supabase.table("ContentTrade").select("id", count='exact').execute()
    _, content_quote_length = supabase.table("ContentQuote").select("id", count='exact').execute()
    if content_trade_length[1] > 0:
        data = supabase.table("ContentTrade").delete().neq("id", 0).execute()
    if content_quote_length[1] > 0:
        data = supabase.table("ContentQuote").delete().neq("id", 0).execute()
