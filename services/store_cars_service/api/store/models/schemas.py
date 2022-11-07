from typing import Union
from datetime import datetime, date
from pydantic import BaseModel


class ModelItem(BaseModel):
    datetime: datetime
    soc: int
    chargingPower: float
    status: str


class Tesla(BaseModel):
    vin: str
    carStatistics: Union[list[ModelItem], None] = None

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


class CreateTesla(ModelItem):
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


class Porsche(BaseModel):
    vin: str
    carStatistics: Union[list[ModelItem], None] = None

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
                        }
                    ]
            }
        }


class CreatePorsche(ModelItem):
    vin: str

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
                        }
                    ]
            }
        }


class Audi(BaseModel):
    vin: str
    carStatistics: Union[list[ModelItem], None] = None

    class Config:
        schema_extra = {
            'example': {
                "vin": "PL990011",
                "carStatistics":
                    [
                        {
                            "datetime": "2020-03-10T11:00:00",
                            "soc": "0",
                            "chargingPower": 35,
                            "status": "waiting"
                        }
                    ]
            }
        }


class CreateAudi(ModelItem):
    vin: str

    class Config:
        schema_extra = {
            'example': {
                "vin": "PL990011",
                "carStatistics":
                    [
                        {
                            "datetime": "2020-03-10T11:00:00",
                            "soc": "0",
                            "chargingPower": 50,
                            "status": "waiting"
                        },
                        {
                            "datetime": "2020-03-10T12:00:00",
                            "soc": "0",
                            "chargingPower": 100,
                            "status": "waiting"
                        }
                    ]
            }
        }


class CarItem(BaseModel):
    made: str
    model: str
    year: date
    vin: str


class Car(BaseModel):
    cars: Union[list[CarItem], None]

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


class CreateCar(CarItem):
    pass


class CreateCarItem(CarItem):
    id: int


# class CarCreate(Cars):
#

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
