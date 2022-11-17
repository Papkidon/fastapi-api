from typing import Union
from datetime import datetime, date
from pydantic import BaseModel


class UsageDataNested(BaseModel):
    """This class represents schema validation for nested usage data of car"""
    datetime: datetime
    soc: int
    chargingPower: float
    status: str


class UsageDataInput(BaseModel):
    """This class represents schema validation for downloaded usage data of car"""
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
    """This class represents schema validation for usage data returned by API"""
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
    """This class represents schema validation for car info returned by API"""
    made: str
    model: str
    year: date
    vin: str


class CarInput(BaseModel):
    """This class represents scheme validation for car information"""
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
    """This class represents schema validation for the average charging power"""
    vin: str
    average: float

    class Config:
        schema_extra = {
            'example': {
                'vin': "PL110212",
                "average": 198.0
            }
        }
