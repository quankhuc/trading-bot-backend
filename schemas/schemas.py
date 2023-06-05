from typing import List, Optional

from pydantic import BaseModel


class Country(BaseModel):
    countries: List[str]

    class Config:
        schema_extra = {
            "example": {
                "countries": ['turkey', 'india'],
            }
        }
        
class TradingDate(BaseModel):
    trading_date: str
    
    class Config:
        schema_extra = {
            "example": {
                "trading_date": '01/13/2020',
            }
        }

class TradingYear(BaseModel):
    trading_year: str
    
    class Config:
        schema_extra = {
            "example": {
                "trading_year": '2020',
            }
        }

class University(BaseModel):
    country: Optional[str] = None
    web_pages: List[str] = []
    name: Optional[str] = None
    alpha_two_code: Optional[str] = None
    domains: List[str] = []
    
class ContentTrade(BaseModel):
    stock_type: object = None
    trading_date: str
    trading_time: str
    exchange: object = None
    confirm_no: object = None
    stock_no: str
    stock_symbol: str
    matched_vol: float = 0
    price: float = 0
    side: object = None
    accumulated_vol: float = 0
    accumulated_val: float = 0
    highest: float = 0
    lowest: float = 0
    prior_price: float = 0
    avg_price: float = 0
    open_price: float = 0
    close_price: float = 0
    remain_room: float = 0
    
class ContentQuote(BaseModel):
    ask_price1: float = 0
    ask_price2: float = 0
    ask_price3: float = 0
    ask_price4: float = 0
    ask_price5: float = 0
    ask_price6: float = 0
    ask_price7: float = 0
    ask_price8: float = 0
    ask_price9: float = 0
    ask_price10: float = 0
    ask_vol1: str = "0"
    ask_vol2: str = "0"
    ask_vol3: str = "0"
    ask_vol4: str = "0"
    ask_vol5: str = "0"
    ask_vol6: str = "0"
    ask_vol7: str = "0"
    ask_vol8: str = "0"
    ask_vol9: str = "0"
    ask_vol10: str = "0"
    bid_price1: float = 0
    bid_price2: float = 0
    bid_price3: float = 0
    bid_price4: float = 0
    bid_price5: float = 0
    bid_price6: float = 0
    bid_price7: float = 0
    bid_price8: float = 0
    bid_price9: float = 0
    bid_price10: float = 0
    bid_vol1: str = "0"
    bid_vol2: str = "0"
    bid_vol3: str = "0"
    bid_vol4: str = "0"
    bid_vol5: str = "0"
    bid_vol6: str = "0"
    bid_vol7: str = "0"
    bid_vol8: str = "0"
    bid_vol9: str = "0"
    bid_vol10: str = "0"
    
class HistoricalData(BaseModel):
    data_type: str
    content: ContentTrade | ContentQuote
