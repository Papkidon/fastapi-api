from typing import Union

from sqlalchemy import func
from sqlalchemy.orm import Session
from ...models import models, schemas

"""QueryCarInfo implements querying 'cars' table"""


class QueryCarInfo:
    __db_session: Session = None  # Database session
    __cars_vin_list: dict = {
        'porsche': "PL110212",
        'tesla': "PL090201",
        'audi': "PL990011"
    }

    def __init__(self, db):
        self.__db_session = db

    def query_current_charge(self, model):
        """
        Query the current charge for the given model. Returns
        current charge if found, None otherwise.
        """
        return self.__db_session.query(model.soc, func.max(model.datetime)) \
            .group_by(model.soc, model.datetime) \
            .order_by(model.datetime.desc()) \
            .first()

    def query_car_info(self, vin: str):
        """
        Queries the 'cars' table and returns information about a car with given vin.
        """
        return self.__db_session.query(models.Cars) \
            .filter(models.Cars.vin == vin) \
            .first()

    def get_car_info(self, model) -> Union[list[models.QueryCar], None]:
        """
        Query car info, returns information about a car with given model.
        """
        if model is models.Porsche:
            car_info = self.query_car_info(vin=self.__cars_vin_list.get('porsche'))
        elif model is models.Audi:
            car_info = self.query_car_info(vin=self.__cars_vin_list.get('audi'))
        elif model is models.Tesla:
            car_info = self.query_car_info(vin=self.__cars_vin_list.get('tesla'))
        else:
            return None
        if car_info is not None:
            car_info = car_info.__dict__
            current_soc = self.query_current_charge(model)[0]
            if current_soc is not None:
                db_model = models.QueryCar(id=car_info.get('id'),
                                           made=car_info.get('made'),
                                           model=car_info.get('model'),
                                           year=car_info.get('year'),
                                           vin=car_info.get('vin'),
                                           current_soc=current_soc)
                return [db_model]
            return None

    def get_all_cars_info(self) -> list:
        """Get information about all cars, returns list of car information"""
        response_list = []
        porsche = self.get_car_info(models.Porsche)

        if porsche is not None:
            response_list.append(porsche.pop())
        audi = self.get_car_info(models.Audi)

        if audi is not None:
            response_list.append(audi.pop())
        tesla = self.get_car_info(models.Tesla)

        if tesla is not None:
            response_list.append(tesla.pop())

        # Remove all None values from response_list
        response_list = [element for element in response_list if element is not None]
        return response_list

    @classmethod
    def convert_to_schema(cls, response) -> list:
        """Convert response to schema"""
        response_list = []
        for model in response:
            response_list.append(schemas.QueryCar(id=model.id,
                                                  model=model.model,
                                                  made=model.made,
                                                  year=model.year,
                                                  vin=model.vin,
                                                  current_soc=model.current_soc))
        return response_list
