from pydantic import BaseModel, Field
from typing import Literal

symbol_schema: str = Field(..., min_length=1, max_length=6)

class StockLookupParams(BaseModel):
    query: str = Field(..., min_length=1, max_length=50) 

class StockChartParams(BaseModel):
    symbol: str = symbol_schema
    timeline: Literal['1d','5d','1mo', '6mo', '1y', '5y', 'ytd', 'max']

class NewsParams(BaseModel):
    symbol: str = symbol_schema
    limit: int = Field(20, ge=1, le=50)

class AnalysisParams(BaseModel):
    symbol: str = symbol_schema 

