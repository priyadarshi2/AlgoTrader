from pydantic import BaseModel
from typing import List

class StockName(BaseModel):
    name : str

class KeyValues(BaseModel):
    data : dict

class TradeHistoryModel(StockName):
    hist : dict
    summary : dict

class ListModel(BaseModel):
    data : List

class ActionHistoryModel(StockName):
    hist : list
    summary : dict