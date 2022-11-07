from typing import Union
from datetime import datetime, date
from pydantic import BaseModel


class CarData(BaseModel):
    datetime: datetime
    soc: str
    chargingPower: int
    status: str


class Tesla(BaseModel):
    vin: str
    carStatistics: Union[list[CarData], None] = None


class Porsche(BaseModel):
    vin: str
    carStatistics: Union[list[CarData], None] = None


class Audi(BaseModel):
    vin: str
    carStatistics: Union[list[CarData], None] = None


class CarInfo(BaseModel):
    made: str
    model: str
    year: date
    vin: str


class Car(BaseModel):
    cars: Union[list[CarInfo], None] = None
