from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Dict, Any, Optional, Union, Callable
from src.source_metadata import param_strat_modified, params_keys
from datetime import date, timedelta

class StrategyParams(BaseModel):
    name: str = Field(..., description="Name of the strategy")
    optional_params: Dict[str, Union[int, float, bool]] = {}

    def __init__(self, **data):
        super().__init__(**data)
        self.optional_params = {}

        strategy_index = params_keys.get(data['name'])
        
        if strategy_index is None:
            raise ValueError(f"Invalid strategy name: {data['name']}")
        
        # Get strategy parameters from the param_strat_modified dictionary
        strategy_params = param_strat_modified.get(strategy_index, [])
        
        # For each parameter defined in the strategy, check if it's in the input data
        # If not, use the default value from the dictionary
        for param, default, _, _, ptype in strategy_params:
            # Use the provided value or the default from the dictionary
            self.optional_params[param] = ptype(data.get(param, default))
        
        

    def is_valid(self) -> bool:
        # Add strategy-specific validation logic
        return True

    def get_params_tuple(self):
        strategy_index = params_keys.get(self.name)
        if strategy_index is None:
            raise ValueError(f"Invalid strategy name: {self.name}")
        strategy_params = param_strat_modified.get(strategy_index, [])
        return tuple(
            (param, self.optional_params.get(param, default))
            for param, default, _, _, _ in strategy_params
        )
    
    #function that returns tuple of all values in optional_params dictionary
    def get_optional_params_tuple(self):
        return tuple(self.optional_params.values())


class AssetParams(BaseModel):
    ticker_symbol: str = Field(..., description="Ticker symbol of the asset")
    start_date: date = Field(..., description="Start date for the strategy")
    end_date: date = Field(..., description="End date for the strategy")
    amount: float = Field(..., description="Amount to be invested")
    time_delta: str = Field(default="1d", description="Time delta between start and end dates")
    data_length: Optional[int] = None

    @model_validator(mode='before')
    def validate_dates(cls, values):
        start_date = values.get("start_date")
        end_date = values.get("end_date")
        if start_date and end_date and start_date >= end_date:
            raise ValueError("End date must be after start date")
        return values

    def is_valid(self) -> bool:
        # Add asset-specific validation logic
        return True

    def get_params_tuple(self):
        return (self.ticker_symbol, self.start_date, self.end_date, self.time_delta)
    
    def set_data_length(self, data_length):
        self.data_length = data_length
    
class Params(BaseModel):
    strategy_params: StrategyParams
    asset_params: AssetParams

    @model_validator(mode='before')
    def validate_combined(cls, values):
        # Validate strategy and asset parameters
        strategy_data = values.get("strategy_params")
        print("values",strategy_data)
        asset_data = values.get("asset_params")
        print("asset", asset_data)

        if not strategy_data or not asset_data:
            raise ValueError("Both strategy_params and asset_params must be provided.")

        # Validate strategy name
        if params_keys.get(strategy_data["name"]) not in params_keys.values():
            print("strategy_data['name']",strategy_data["name"])
            raise ValueError(f"Invalid strategy name: {strategy_data['name']}")

        return values

    def validate(self) -> Dict[str, Union[bool, list]]:
        errors = []
        if not self.strategy_params.is_valid():
            errors.append("Invalid strategy parameters.")
        if not self.asset_params.is_valid():
            errors.append("Invalid asset parameters.")
        return {"is_valid": len(errors) == 0, "errors": errors}

    def get_combined_params(self):
        return {
            "strategy": self.strategy_params.get_params_tuple(),
            "asset": self.asset_params.get_params_tuple(),
        }
    
    def set_asset_data_length(self, data_length: int):
        """
        Set the data length in the AssetParams instance.
        
        Args:
            data_length (int): The length of the data to be set.
        """
        self.asset_params.set_data_length(data_length)
    
    @staticmethod
    def get_params_detail(strategy_name: str, custom_params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Static method to fetch and initialize the strategy parameters based on the strategy name.
        Args:
            strategy_name (str): The name of the strategy.
            custom_params (Optional[Dict[str, Any]]): A dictionary of custom parameters to override the defaults.

        Returns:
            Dict[str, Any]: A dictionary containing strategy parameters with values.
        """
        # Retrieve strategy index using the name of the strategy
        strategy_index = params_keys.get(strategy_name)

        if strategy_index is None:
            raise ValueError(f"Invalid strategy name: {strategy_name}")

        # Get default parameters for the strategy from the param_strat_modified dictionary
        strategy_params = param_strat_modified.get(strategy_index, [])
        default_params = {}

        # Initialize default parameters
        for param, default, _, _, ptype in strategy_params:
            default_params[param] = ptype(default)

        # Override with custom parameters if provided
        if custom_params:
            for param, value in custom_params.items():
                if param in default_params:
                    default_params[param] = value

        return default_params


