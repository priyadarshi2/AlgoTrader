import src.App.schema as schm
import src.App.services as srv
from fastapi import APIRouter, HTTPException, Request, Query
from typing import Dict

router = APIRouter()

@router.get("/common-backtest", response_model=schm.TradeHistoryModel)
async def show_common_backtest(request : Request):
    symbol = request.query_params.get('ticker_symbol',"")
    start_date = request.query_params.get('start_date',"")
    end_date = request.query_params.get('end_date',"")
    amount = float(request.query_params.get('amount',""))
    backtest_key = int(request.query_params.get('key',0))
    # Extract additional parameters from the query
    paramets = {key: value for key, value in request.query_params.items() if key not in ['ticker_symbol', 'start_date', 'end_date', 'amount', 'key']}
    if not srv.isValidBacktestKey(backtest_key):
        raise HTTPException(status_code=400, detail="Not a valid key!")
    if not symbol or not start_date or not end_date:
        raise HTTPException(status_code=400, detail="Insufficient data")
    if start_date > end_date:
        raise HTTPException(status_code=406, detail="Wrong dates entry")
    else:
        return srv.get_backtest(symbol, start_date, end_date, amount, backtest_key, paramets)

@router.get("/common-strategies", response_model=schm.KeyValues)
async def show_common_strategies():
    return srv.get_common_strategies()

@router.get("/get-parameter", response_model=schm.ListModel)
async def show_parameters(request : Request):
    key = int(request.query_params.get('key',0))
    if not srv.isValidBacktestKey(key):
        raise HTTPException(status_code=400, detail="Not a valid key!")
    return srv.get_parameters(key)

@router.get("/param-validation", response_model=schm.KeyValues)
async def show_param_validation(request : Request):
    symbol = request.query_params.get('ticker_symbol',"")
    start_date = request.query_params.get('start_date',"")
    end_date = request.query_params.get('end_date',"")
    key = int(request.query_params.get('key',0))
    # Extract additional parameters from the query
    paramets = {key: value for key, value in request.query_params.items() if key not in ['ticker_symbol', 'start_date', 'end_date', 'key']}
    return srv.get_validate_params(symbol, start_date, end_date, key, paramets)