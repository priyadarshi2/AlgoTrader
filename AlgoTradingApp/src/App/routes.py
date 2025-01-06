import src.App.schema as schm
import src.App.services as srv
from fastapi import APIRouter, HTTPException, Request

router = APIRouter()

@router.get("/common-backtest", response_model=schm.TradeHistoryModel)
async def show_common_backtest(request : Request):
    symbol = request.query_params.get('ticker_symbol',"")
    start_date = request.query_params.get('start_date',"")
    end_date = request.query_params.get('end_date',"")
    amount = float(request.query_params.get('amount',""))
    backtest_key = int(request.query_params.get('key',0))
    if not srv.isValidBacktestKey(backtest_key):
        raise HTTPException(status_code=400, detail="Not a valid key!")
    if not symbol or not start_date or not end_date:
        raise HTTPException(status_code=400, detail="Insufficient data")
    if start_date > end_date:
        raise HTTPException(status_code=406, detail="Wrong dates entry")
    else:
        return srv.get_rsi_backtest(symbol, start_date, end_date, amount, backtest_key)

@router.get("/common-strategies", response_model=schm.KeyValues)
async def show_common_strategies():
    return srv.get_common_strategies()
