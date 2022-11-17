from typing import Union
from sqlalchemy.orm import Session

from ...models import schemas, models

"""QueryAverage class implements querying the 'average' table"""


class QueryAverage:
    __db_session: Session = None  # Database session
    # Dictionary containing vins of corresponding cars
    __cars_vin_list = {
        'porsche': "PL110212",
        'tesla': "PL090201",
        'audi': "PL990011"
    }

    def __init__(self, db):
        self.__db_session = db

    def query_average_charging_power(self, vin: str):
        """Query database for average charging power of a car with a given vin"""
        return self.__db_session.query(models.Average.id, models.Average.vin, models.Average.average) \
            .filter(models.Average.vin == vin) \
            .first()

    @staticmethod
    def create_average_model(query: list) -> Union[models.Average, None]:
        """Create new average model from a query if query is not empty"""
        if query is not None:
            return models.Average(id=query[0],
                                  vin=query[1],
                                  average=query[2])
        return None

    def create_model_if_not_none(self, query) -> Union[models.Average, None]:
        if query is not None:
            return self.create_average_model(query)
        return None

    def get_average(self, car: str) -> list:
        """
        Queries the database for the average of a given car or all cars
        and returns list of results
        :parameter: porsche, tesla, audi, all
        :return: list of results
        """

        response_list = []
        if car == 'all' or car == '':
            avg_porsche = self.query_average_charging_power(vin=self.__cars_vin_list.get('porsche'))
            avg_audi = self.query_average_charging_power(vin=self.__cars_vin_list.get('audi'))
            avg_tesla = self.query_average_charging_power(vin=self.__cars_vin_list.get('tesla'))

            response_list.append(self.create_model_if_not_none(avg_porsche))
            response_list.append(self.create_model_if_not_none(avg_audi))
            response_list.append(self.create_model_if_not_none(avg_tesla))

        elif car == 'porsche' or car == self.__cars_vin_list.get('porsche'):
            avg_porsche = self.query_average_charging_power(vin=self.__cars_vin_list.get('porsche'))
            response_list.append(self.create_model_if_not_none(avg_porsche))

        elif car == 'audi' or car == self.__cars_vin_list.get('audi'):
            avg_audi = self.query_average_charging_power(vin=self.__cars_vin_list.get('audi'))
            response_list.append(self.create_model_if_not_none(avg_audi))

        elif car == 'tesla' or car == self.__cars_vin_list.get('tesla'):
            avg_tesla = self.query_average_charging_power(vin=self.__cars_vin_list.get('tesla'))
            response_list.append(self.create_model_if_not_none(avg_tesla))

        # Remove None values if they exist from the response list
        response_list = [element for element in response_list if element is not None]
        return response_list

    @classmethod
    def convert_to_schema(cls, response) -> list:
        response_schema = []
        for model in response:
            response_schema.append(schemas.QueryAverage(id=model.id,
                                                        vin=model.vin,
                                                        average=model.average))
        return response_schema
