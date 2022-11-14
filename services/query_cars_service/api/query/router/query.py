from fastapi import Depends, HTTPException
from fastapi.openapi.models import APIKey
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from sqlalchemy.orm import Session

from ..db.connect.db import SessionLocal
from ..db.crud.QueryCarInfo import QueryCarInfo
from ..db.crud.QueryUsageData import QueryUsageData
from ..db.crud.QueryAverage import QueryAverage
from ..models import schemas, models
from ..auth.auth import get_api_key

query = InferringRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@cbv(query)
class Query:
    db: Session = Depends(get_db)
    api_key: APIKey = Depends(get_api_key)

    @query.get('/', status_code=200, include_in_schema=False)
    async def query_check(self):
        return {'detail': 'Query service is up.'}

    @query.get('/car-info/{car}', response_model=list[schemas.QueryCar], status_code=200, tags=['query'])
    async def query_car_info(self, car: str):
        """
        Get information about a given car or all cars with current <b>soc</b>.\n
        Available parameters are: <b>porsche, tesla, audi, all</b>
        """
        car_info = QueryCarInfo(db=self.db)

        if car == 'porsche':
            response = car_info.get_car_info(models.Porsche)
        elif car == 'tesla':
            response = car_info.get_car_info(models.Tesla)
        elif car == 'audi':
            response = car_info.get_car_info(models.Audi)
        elif car == 'all':
            response = car_info.get_all_cars_info()
        else:
            raise HTTPException(status_code=422, detail='Wrong car name')
        if not response:
            raise HTTPException(status_code=404, detail='Could not get specified car/cars info')
        response_schema = car_info.convert_to_schema(response)
        return response_schema

    @query.get('/usage-data/{car}', status_code=200, response_model=list[schemas.QueryDataItems], tags=['query'])
    async def get_car_data(self, car: str):
        """
        Get usage data about a given car or all cars.\n
        Available parameters are: <b>porsche, tesla, audi, all</b>
        """

        def is_none(response):
            """Raise HTTPException if response is None
                It means that no data was found."""
            if response is None:
                raise HTTPException(status_code=404, detail='Data not found')

        def extend_if_not_none(response, schema_list):
            """Extend schema_list if response is not None
                It means"""
            if response is not None:
                schema_list.extend(QueryUsageData.convert_to_schema(response))

        query_usage_data = QueryUsageData(db=self.db)

        if car == 'porsche':
            response = query_usage_data.get_usage_data(models.Porsche)
            is_none(response=response)
            schema_list = query_usage_data.convert_to_schema(response)
            return schema_list

        elif car == 'audi':
            response = query_usage_data.get_usage_data(models.Audi)
            is_none(response=response)
            schema_list = query_usage_data.convert_to_schema(response)
            return schema_list

        elif car == 'tesla':
            response = query_usage_data.get_usage_data(models.Tesla)
            is_none(response=response)
            schema_list = query_usage_data.convert_to_schema(response)
            return schema_list

        elif car == 'all':
            schema_list = []
            porsche = query_usage_data.get_usage_data(models.Porsche)
            audi = query_usage_data.get_usage_data(models.Audi)
            tesla = query_usage_data.get_usage_data(models.Tesla)

            # Extend schema list if response is not None
            extend_if_not_none(porsche, schema_list)
            extend_if_not_none(audi, schema_list)
            extend_if_not_none(tesla, schema_list)

            if not schema_list:
                raise HTTPException(status_code=404, detail='No data was found.')
            return schema_list
        else:
            raise HTTPException(status_code=404, detail='Car with a given name not found.')

    @query.get('/average/{car}', response_model=list[schemas.QueryAverage], status_code=200, tags=['query'])
    async def query_car_average(self, car: str):
        """
        Averages first must be stored in the database by api/v1/store/average\n
        Get average of all cars or selected car.\n
        Available parameters are:  <b>porsche, tesla, audi, all</b>
        """
        response = QueryAverage(db=self.db).get_average(car=car)
        if not response:
            raise HTTPException(status_code=404, detail='Could not find average for a given car/cars')
        response_schema = QueryAverage.convert_to_schema(response)
        return response_schema
