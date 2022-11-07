from datetime import datetime, date
from pydantic import BaseModel


class ModelItem(BaseModel):
    datetime: datetime
    soc: int
    chargingPower: float
    status: str


class CarItem(BaseModel):
    made: str
    model: str
    year: date
    vin: str


class QueryCar(CarItem):
    id: int
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


class Average(BaseModel):
    vin: str
    average: float


class QueryAverage(Average):
    id: int

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
    vin: str
    datetime: datetime
    chargingPower: float
    soc: float
    id: int
    status: str
