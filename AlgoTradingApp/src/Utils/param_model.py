from pydantic import BaseModel, Field, field_validator
from typing import Dict, Any, Optional, Union, Callable
from src.source_metadata import param_strat_modified, params_keys
from src.Utils.validatators import input_validations
from datetime import date, timedelta

class StrategyParams(BaseModel):
    '''This class stores Parameters required to execute a trading strategy'''
    name: str = Field(..., description="Name of the strategy")
    optional_params: Dict[str, Union[int,float,bool]] = {}

    def __init__(self, **data):
        '''Initialise'''
        strategy_index = params_keys.get(data['name']) 
        if strategy_index is None: #Check if the key exists
            raise ValueError(f"Invalid strategy name: {data['name']}") 
        strategy_params = param_strat_modified.get(strategy_index, []) 
        for param, default, _, _, ptype in strategy_params: 
            self.optional_params[param] = ptype(data.get(param, default)) 

        super().__init__(**data) 
        

    def get_param(self, key: str):
        '''Get the exact param you want'''
        return self.optional_params.get(key, 'default')

    def is_valid(self): 
        errors = self.model_validate() 
        return len(errors) == 0,errors
    
    def apply_params(self):
        """
        Return the tuple of parameters to be assigned to the strategy class.
        """
        strategy_index = params_keys.get(self.name)
        if strategy_index is None:
            raise ValueError(f"Invalid strategy name: {self.name}")

        strategy_params = param_strat_modified.get(strategy_index, [])
        params_tuple = tuple((param, self.optional_params.get(param, default)) for param, default, _, _, _ in strategy_params)
        return params_tuple

class AssetParams(BaseModel):
    '''This class stores the data required to acquire the asset data'''
    ticker_symbol: str = Field(..., description="Ticker symbol of the asset")
    start_date: date = Field(..., description="Start date for the strategy")
    end_date: date = Field(..., description="End date for the strategy")
    amount: float = Field(..., description="Amount to be invested")
    time_delta: float = Field(..., description="Timw delta between start and end dates")

    def __init__(self, **data): 
        super().__init__(**data) # Call the BaseModel initializer

    @field_validator("start_date", "end_date", mode="before")
    def check_date_format(cls, v):
        if not isinstance(v, date):
            raise ValueError("Date must be in YYYY-MM-DD format")
        return v

    @field_validator("end_date", mode="before")
    def check_dates(cls, v, values):
        if "start_date" in values and v < values["start_date"]:
            raise ValueError("End date must be after start date")
        return v

    @field_validator("amount", mode="before")
    def check_amount(cls, v):
        if v <= 0:
            raise ValueError("Amount must be greater than 0")
        return v

    def check_dates_order(self) -> bool:
        """
        Check if the start date is earlier than the end date.
        Returns True if valid, raises ValueError otherwise.
        """
        if self.start_date >= self.end_date:
            raise ValueError("End date must be after start date")
        return True
    
    def compute_total_data_points(self) -> int:
        """
        Compute the total number of data points within the specified time frame.
        Returns the total number of data points.
        """
        if not self.check_dates_order():
            raise ValueError("Invalid date order: Start datetime must be earlier than end datetime")

        total_seconds = (self.end_date - self.start_date).total_seconds()
        total_data_points = total_seconds // self.time_delta.total_seconds()
        return int(total_data_points)
    
class Params(StrategyParams, AssetParams):
    """
    A class that combines StrategyParams and AssetParams.
    Inherits from both StrategyParams and AssetParams.
    """
    def __init__(self, **data): # Separate strategy parameters and asset parameters 
        strategy_params = {key: data[key] for key in StrategyParams.model_fields.keys() if key in data} 
        asset_params = {key: data[key] for key in AssetParams.model_fields.keys() if key in data} 
        # Initialize the parent classes with their respective parameters 
        StrategyParams.__init__(self, **strategy_params) 
        AssetParams.__init__(self, **asset_params) 
        # Compute data length using the AssetParams method 
        self.data_length = self.compute_total_data_points() 
        # Perform validation upon initialization 
        errors = self.validate() 
        if errors: 
            raise ValueError(f"Invalid input parameters: {errors}") 
        
    def validate(self):
        """
        Validate both strategy and asset parameters.
        Returns a list of errors if any.
        """
        errors = []

        # Validate strategy parameters
        strategy_index = params_keys.get(self.name)
        if strategy_index is None:
            errors.append(f"Invalid strategy name: {self.name}")
        else:
            validation_func = input_validations.get(strategy_index)
            if validation_func:
                validation_results = validation_func(**self.optional_params, data_length=self.data_length)
                if not validation_results["is_valid"]:
                    errors.extend(validation_results["errors"])

        # Validate asset parameters
        try:
            self.check_dates_order()  # Check date order
        except ValueError as e:
            errors.append(str(e))

        return errors
    

    


