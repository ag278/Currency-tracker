from pydantic import BaseModel, validator, Field, field_validator


class AvailableModel(BaseModel):
    success: bool
    symbols: dict


class ConvertModel(BaseModel):
    success: bool
    query: dict
    info: dict
    date: str
    result: float


class FetchModel(BaseModel):
    success: bool
    timestamp: int
    base: str
    date: str
    rates: dict
