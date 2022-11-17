from datetime import datetime
from sqlalchemy.orm import Session
from ...models import schemas

"""StoreUsage implements storing usage information of cars in the database"""


class StoreUsage:
    _db_session: Session = None  # Database session
    _schema = None  # Schema of data to be put into database
    _model = None  # Model to be converted to from schema

    def __init__(self, db: Session, schema, model):
        self._db_session = db
        self._schema = schema
        self._model = model

    def get_usage_by_timestamp(self, timestamp: datetime):
        """Get usage information for a given timestamp"""
        return self._db_session.query(self._model).filter(self._model.datetime == timestamp).first()

    def create_model(self) -> list:
        """Create list of models from the usage data"""
        model_list = []
        schema_dict = self._schema.dict()
        for i in range(len(schema_dict['carStatistics'])):
            model_list.append(self._model(vin=schema_dict['vin'],
                                          datetime=schema_dict['carStatistics'][i]['datetime'],
                                          soc=schema_dict['carStatistics'][i]['soc'],
                                          chargingPower=schema_dict['carStatistics'][i]['chargingPower'],
                                          status=schema_dict['carStatistics'][i]['status']))
        return model_list

    def store_usage(self) -> list:
        """Store usage data in the database"""
        model_list = self.create_model()
        output_list = []
        for model in model_list:
            if not self.get_usage_by_timestamp(timestamp=model.datetime):
                self._db_session.add(model)
                self._db_session.commit()
                self._db_session.refresh(model)
                output_list.append(model)
        return output_list

    @classmethod
    def convert_to_schema(cls, response):
        """Convert to schema"""
        schema_list = []
        for model in response:
            schema_list.append(schemas.UsageDataOutput(vin=model.vin,
                                                       datetime=model.datetime,
                                                       soc=model.soc,
                                                       chargingPower=model.chargingPower,
                                                       status=model.status))
        return schema_list
