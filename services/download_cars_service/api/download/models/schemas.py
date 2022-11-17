from typing import Union
from datetime import datetime, date
from pydantic import BaseModel


class UsageDataNested(BaseModel):
    """This class represents schema validation for nested usage data of car
    Applicable to: Porsche, Tesla, Audi"""
    datetime: datetime
    soc: str
    chargingPower: int
    status: str


class UsageData(BaseModel):
    """This class represents schema validation for downloaded usage data of car
    Applicable to: Porsche, Tesla, Audi"""
    vin: str
    carStatistics: Union[list[UsageDataNested]]

    class Config:
        schema_extra = {
            'example': {
                "vin": "PL110212",
                "carStatistics":
                    [
                        {
                            "datetime": "2020-03-10T11:00:00",
                            "soc": "30",
                            "chargingPower": 200,
                            "status": "charging"
                        },
                        {"datetime": "2020-03-10T11:15:00",
                         "soc": "40",
                         "chargingPower": 200,
                         "status": "charging"
                         }
                    ]
            }}


# Car Information
class CarInfoNested(BaseModel):
    """This class represents nested car information"""
    made: str
    model: str
    year: date
    vin: str


# Porsche, Tesla, Audi
class CarInfo(BaseModel):
    """This class represents scheme validation for car information"""
    cars: list[CarInfoNested]

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
                        },
                        {
                            "made": "Porshe",
                            "model": "Taycan",
                            "year": "2020-01-25",
                            "vin": "PL110212"
                        }
                    ]
            }
        }
