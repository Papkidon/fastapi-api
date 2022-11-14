from typing import Union
from datetime import datetime, date
from pydantic import BaseModel


class UsageDataNested(BaseModel):
    datetime: datetime
    soc: int
    chargingPower: float
    status: str


class UsageDataInput(BaseModel):
    vin: str
    carStatistics: list[UsageDataNested]

    class Config:
        schema_extra = {
            'example': {
                "vin": "PL090201",
                "carStatistics":
                    [
                        {
                            "datetime": "2020-03-10T11:00:00",
                            "soc": "0",
                            "chargingPower": 25,
                            "status": "waiting"
                        }
                    ]
            }
        }


class UsageDataOutput(UsageDataNested):
    vin: str

    class Config:
        schema_extra = {
            'example': {
                "vin": "PL090201",
                "carStatistics":
                    [
                        {
                            "datetime": "2020-03-10T11:00:00",
                            "soc": "0",
                            "chargingPower": 25,
                            "status": "waiting"
                        }
                    ]
            }
        }


class CarOutput(BaseModel):
    made: str
    model: str
    year: date
    vin: str


class CarInput(BaseModel):
    cars: list[CarOutput]

    class Config:
        schema_extra = {
            'example': {
                "cars":
                    [
                        {
                            "made": "Tesla",
                            "model": "Model S",
                            "year": "2020-08-10",
                            "vin": "PL090201"
                        }
                    ]
            }
        }


class Average(BaseModel):
    vin: str
    average: float

    class Config:
        schema_extra = {
            'example': {
                'vin': "PL110212",
                "average": 198.0
            }
        }
