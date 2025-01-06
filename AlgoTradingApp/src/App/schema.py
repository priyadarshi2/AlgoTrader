from pydantic import BaseModel

class StockName(BaseModel):
    name : str

class KeyValues(BaseModel):
    data : dict

class TradeHistoryModel(StockName):
    hist : dict
    summary : dict