import src.App.schema as schm
import src.App.services as srv
from fastapi import APIRouter, HTTPException, Request, Query
from typing import Dict
from src.Utils.param_model import Params, CustomParams

router = APIRouter()

@router.post("/common-backtest", response_model=schm.TradeHistoryModel)
async def show_common_backtest(params: Params):
    # Perform overall validation
    print("params")
    is_valid, errors = params.validate()
    print("is_valid", is_valid)
    if not is_valid:
        raise HTTPException(status_code=400, detail=errors)

    # Fetch the backtest result
    result = srv.get_backtest(params)
    return result


@router.get("/common-strategies", response_model=schm.KeyValues)
async def show_common_strategies():
    return srv.get_common_strategies()

@router.get("/get-parameter", response_model=schm.ListModel)
async def show_parameters(request: Request):
    key = request.query_params.get('key', None)
    if not srv.isValidBacktestKey(key):
        raise HTTPException(status_code=400, detail="Not a valid key!")
    return srv.get_parameters(key)

@router.post("/param-validation", response_model=schm.KeyValues)
async def show_param_validation(params : Params):
    # Perform overall validation
    print("params")
    is_valid, errors = params.validate()
    print("is_valid", is_valid)
    if not is_valid:
        raise HTTPException(status_code=400, detail=errors)

    # Fetch the backtest result
    result = srv.get_validate_params(params)
    return result

@router.post("/custom-backtest", response_model=schm.ActionHistoryModel)
async def show_ufo_backtesting(params : CustomParams):
    # Perform overall validation
    print("params")
    is_valid, errors = params.validate()
    print("is_valid", is_valid)
    if not is_valid:
        raise HTTPException(status_code=400, detail=errors)

    # Fetch the backtest result
    result = srv.get_custom_backtest(params)
    return result