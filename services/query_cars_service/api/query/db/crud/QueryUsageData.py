from typing import Union
from ...models import schemas
from sqlalchemy.orm import Session

"""QueryUsageData implements querying 'audi', 'porsche', 'tesla' tables"""


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

    @classmethod
    def convert_to_schema(cls, response) -> list:
        schema_list = []
        for model in response:
            schema_list.append(schemas.QueryDataItems(vin=model.vin,
                                                      id=model.id,
                                                      datetime=model.datetime,
                                                      chargingPower=model.chargingPower,
                                                      soc=model.soc,
                                                      status=model.status))
        return schema_list
