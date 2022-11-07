from typing import Union
from datetime import datetime, date
from pydantic import BaseModel


# Cars
class CarData(BaseModel):
    datetime: datetime
    soc: str
    chargingPower: int
    status: str


# Porsche, Tesla, Audi
class CarStats(BaseModel):
    vin: str
    carStatistics: Union[list[CarData], None] = None

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
class CarInfo(BaseModel):
    made: str
    model: str
    year: date
    vin: str


# Porsche, Tesla, Audi
class Car(BaseModel):
    cars: Union[list[CarInfo], None] = None

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
