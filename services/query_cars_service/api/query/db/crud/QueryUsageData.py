from typing import Union
from ...models import schemas, models

from sqlalchemy.orm import Session


class QueryUsageData:
    _db_session: Session = None  # Database session

    def __init__(self, db):
        self._db_session = db

    def get_usage_data(self, model) -> Union[list, None]:
        """
        Return given car usage data
        """
        models_list = []
        query = self._db_session.query(model).all()
        if query:
            for data in query:
                new_model = model(id=data.id,
                                  datetime=data.datetime,
                                  vin=data.vin,
                                  soc=data.soc,
                                  status=data.status,
                                  chargingPower=data.chargingPower)
                models_list.append(new_model)
            return models_list
        return None

    def get_usage_data_by_vin(self):
        query = []
        models_list = []
        porsche = self._db_session.query(models.Porsche).all()
        if porsche:
            query.append(porsche)
        audi = self._db_session.query(models.Audi).all()
        if audi:
            query.append(audi)
        tesla = self._db_session.query(models.Tesla).all()
        if tesla:
            query.append(tesla)
        return models_list

    @classmethod
    def convert_to_schema(cls, response):
        schema_list = []
        for model in response:
            schema_list.append(schemas.QueryDataItems(vin=model.vin,
                                                      id=model.id,
                                                      datetime=model.datetime,
                                                      chargingPower=model.chargingPower,
                                                      soc=model.soc,
                                                      status=model.status))
        return schema_list
