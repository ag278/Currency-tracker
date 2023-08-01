from pydantic import BaseModel, validator, Field, field_validator
from exceptions.error_messages import *
from exceptions.custom_exceptions import custom_exception_handler
from pydantic import BaseModel, ValidationError


class RemoveModel(BaseModel):
    currency: str

    @validator('currency', pre=True)
    def convert_to_single_value(cls, value):
        return value[0] if isinstance(value, list) else value


class FetchModel(BaseModel):
    symbols: str
    base: str
    interval: int

    @validator('symbols', pre=True)
    def convert_to_single_value(cls, value):
        return value[0] if isinstance(value, list) else value

    @validator('base', 'interval', pre=True)
    def check_single_string(cls, value):
        if len(value) != 1 or ',' in value[0]:
            raise ValueError(QUERY_INPUT_COMMA_MESSAGE)
        return value[0]


class ConvertModel(BaseModel):
    to: str
    from_: str = Field(..., alias='from')
    amount: float

    @validator('amount', pre=True)
    def convert_to_single_value(cls, value):
        if len(value) != 1 or ',' in value[0]:
            raise ValueError(QUERY_INPUT_COMMA_MESSAGE)
        return value[0]
        # return value[0] if isinstance(value, list) else value

    @validator('to', 'from_', pre=True)
    def check_single_string(cls, value):
        if len(value) != 1 or ',' in value[0]:
            raise ValueError(QUERY_INPUT_COMMA_MESSAGE)
        return value[0]
