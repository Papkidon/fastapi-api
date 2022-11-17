from datetime import datetime, date
from pydantic import BaseModel


class QueryCar(BaseModel):
    """Represents validation schema of a '/car-info/{car}' endpoint"""
    id: int
    vin: str
    model: str
    made: str
    year: date
    current_soc: float

    class Config:
        schema_extra = {
            'example': [
                {
                    "made": "Porshe",
                    "model": "Taycan",
                    "year": "2020-01-25",
                    "vin": "PL110212",
                    "id": 2,
                    "current_soc": 80.0
                }
            ]
        }


class QueryAverage(BaseModel):
    """Represents validation schema of a '/average/{car}' endpoint"""
    id: int
    vin: str
    average: float

    class Config:
        schema_extra = {
            'example': [
                {
                    "vin": "PL110212",
                    "average": 198.0,
                    "id": 1
                }
            ]
        }


class QueryDataItems(BaseModel):
    """Represents validation schema of a '/usage-data/{car}' endpoint"""
    vin: str
    datetime: datetime
    chargingPower: float
    soc: float
    id: int
    status: str
