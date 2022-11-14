from sqlalchemy import func
from sqlalchemy.orm import Session
from ...models import models


class StoreAverage:

    _db_session : Session = None  # Database session


    def __init__(self, db):
        self._db_session = db

    def find_average_by_vin(self, vin: str):
        """
        Check if average for given vin is already in the database
        """
        return self._db_session.query(models.Average).filter(models.Average.vin == vin).first()

    def calculate_average(self, model):
        """
        Calculate average for given model.
        :parameter: model - model for which to calculate average
        """
        return self._db_session.query(func.avg(model.chargingPower).
                                      label('average'), model.vin.label('vin')). \
                                      filter(model.chargingPower != 0). \
                                      group_by(model.vin). \
                                      first()

    def store_model(self, result):
        """
        If the average was calculated, then result shouldn't be None.
        If this is the case, then store the result in the database.
        If not, return None.
        :parameter result:
        :return: if
        """
        if result is not None:
            db_avg_model = models.Average(vin=result[1],
                                          average=result[0])
            # Store it in the database if it doesn't already exist
            if not self.find_average_by_vin(vin=db_avg_model.vin):
                self._db_session.add(db_avg_model)
                self._db_session.commit()
                self._db_session.refresh(db_avg_model)
                return db_avg_model
            return None

    # Calculate and store average chargingPower of every car
    def store_averages(self):
        """
        Calculate averages for every car from usage data and if usage data
        exists, then store them in the database.
        :return: list of models of stored averages
        """
        averages = []
        # Calculate average of Porsche
        result = self.calculate_average(models.Porsche)
        store = self.store_model(result)
        if store is not None:
            averages.append(store)

        # Calculate average of Tesla
        result = self.calculate_average(models.Tesla)
        store = self.store_model(result)
        if store is not None:
            averages.append(store)

        # Calculate average of Audi
        result = self.calculate_average(models.Audi)
        store = self.store_model(result)
        if store is not None:
            averages.append(store)

        return averages
