from fastapi import Depends, HTTPException
from fastapi.openapi.models import APIKey
from fastapi_utils.inferring_router import InferringRouter
from sqlalchemy.orm import Session
from fastapi_utils.cbv import cbv

from ..db.crud.StoreCars import StoreCars
from ..db.crud.StoreUsage import StoreUsage
from ..db.crud.StoreAverage import StoreAverage
from ..models import schemas, models
from ..db.connection.db import SessionLocal
from ..auth.auth import get_api_key

# Create router
store = InferringRouter()


"""Store cars service implements the following endpoints :

1. '/' - check if Store car service is available,
2. '/cars/' - store information about cars in the database,
3. '/usage/{model}' - store information about given car usage in the database,
4. '/average/' - store information about averages calculated from information already stored in the database.

"""

def get_db():
    """Get new database connection from connection pool
    and close after code execution"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@cbv(store)
class StoreCBV:
    db: Session = Depends(get_db)  # Database session
    api_key: APIKey = Depends(get_api_key)  # API key

    @store.get('/', status_code=200, include_in_schema=False)
    def store_check(self):
        return {'detail': 'Store service is up.'}

    @store.post('/cars/', response_model=list[schemas.CarOutput], status_code=201)
    async def store_cars(self, car: schemas.CarInput):
        """
        Store information about cars in the database.
        """
        response = StoreCars(car=car, db=self.db).store_information()
        if not response:
            raise HTTPException(status_code=409, detail='Data already exists in database.')
        # Conversion from models to schemas
        schema_list = StoreCars.convert_to_schema(response)
        return schema_list

    @store.post('/usage/{model}', response_model=list[schemas.UsageDataOutput], status_code=201)
    async def store_usage(self, model: str,  car: schemas.UsageDataInput):
        """
        Store information about given car usage in the database
        :param model: car type, possible values are porsche, audi, tesla.
        :param car: schema of data posted to API
        :return: schema list of stored usage data
        """
        if model == 'porsche':
            response = StoreUsage(db=self.db, schema=car, model=models.Porsche).store_usage()
        elif model == 'audi':
            response = StoreUsage(db=self.db, schema=car, model=models.Audi).store_usage()
        elif model == 'tesla':
            response = StoreUsage(db=self.db, schema=car, model=models.Tesla).store_usage()
        else:
            raise HTTPException(status_code=422, detail='Wrong car name')
        if not response:
            raise HTTPException(status_code=409, detail='Data already exists in database.')
        schema_list = StoreUsage.convert_to_schema(response)
        return schema_list

    @store.get('/average/', response_model=list[schemas.Average], status_code=200)
    async def store_average(self):
        """
        Store information about average in database.
        """
        response = StoreAverage(db=self.db).store_averages()
        schema_list = []  # List of models converted to schemas
        if not response:
            raise HTTPException(status_code=409,
                                detail='Data already exists in database or there was no cars to be stored.')
        for model in response:
            schema_list.append(schemas.Average(vin=model.vin,
                                               average=model.average))
        return schema_list
