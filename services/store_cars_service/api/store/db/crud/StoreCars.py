from ...models import schemas, models
from sqlalchemy.orm import Session

"""StoreCars implements storing cars information in the database"""


class StoreCars:
    __db_session: Session = None  # Database session
    __car: schemas.CarInput = None  # Car schema

    def __init__(self, db, car):
        self.__db_session = db
        self.__car = car

    def get_car_by_vin(self, vin: str):
        """
        Query the database for a car with the given vin
        :param vin: vin of the given car
        :return: result of the query
        """
        return self.__db_session.query(models.Cars).filter(models.Cars.vin == vin).first()

    @classmethod
    def convert_to_schema(cls, response) -> list:
        """
        Convert models to schemas
        :parameter response: list of models to be converted
        :return: list of schemas
        """
        schema_list = []
        for model in response:
            schema_list.append(schemas.CarOutput(made=model.made,
                                                 model=model.model,
                                                 year=model.year,
                                                 vin=model.vin))
        return schema_list

    def store_information(self):
        """
        Store information about given car/cars in the database
        :return: list of stored car/cars
        """
        car_dict = self.__car.dict()
        db_car_list = []
        for i in range(0, len(car_dict['cars'])):
            check_if_exists = self.get_car_by_vin(vin=car_dict['cars'][i]['vin'])
            # If it doesn't exist then store it in the database
            if not check_if_exists:
                db_car = models.Cars(made=car_dict['cars'][i]['made'],
                                     model=car_dict['cars'][i]['model'],
                                     year=car_dict['cars'][i]['year'],
                                     vin=car_dict['cars'][i]['vin'])
                self.__db_session.add(db_car)
                self.__db_session.commit()
                self.__db_session.refresh(db_car)
                db_car_list.append(db_car)
        return db_car_list
