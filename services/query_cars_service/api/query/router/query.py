from fastapi import Depends, APIRouter, HTTPException
from fastapi.openapi.models import APIKey
from sqlalchemy.orm import Session

from ..db.db import SessionLocal
from ..models import schemas
from ..db import crud
from ..auth.auth import get_api_key

query = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@query.get('/', status_code=200, include_in_schema=False)
def query_check():
    return {'detail': 'Query service is up.'}


@query.get('/car-info/{car}', response_model=list[schemas.QueryCar], status_code=200, tags=['query'])
async def query_car_info(car: str,
                         db: Session = Depends(get_db),
                         api_key: APIKey = Depends(get_api_key)):
    """
    Get information about a given car or all cars with current <b>soc</b>.\n
    Available parameters are: <b>porsche, tesla, audi, all</b>
    """
    response = crud.get_cars_info(db=db, which=car)
    if not response:
        raise HTTPException(status_code=404, detail='Could not get specified car/cars info')
    response_schema = []
    for model in response:
        response_schema.append(schemas.QueryCar(id=model.id,
                                                model=model.model,
                                                made=model.made,
                                                year=model.year,
                                                vin=model.vin,
                                                current_soc=model.current_soc))
    return response_schema


@query.get('/usage-data/{car}', status_code=200, response_model=list[schemas.QueryDataItems], tags=['query'])
async def get_car_data(car: str,
                       db: Session = Depends(get_db),
                       api_key: APIKey = Depends(get_api_key)):
    """
    Get usage data about a given car or all cars.\n
    Available parameters are: <b>porsche, tesla, audi, all</b>
    """
    if car == 'porsche':
        schema_list = []
        response = crud.get_porsche_data(db=db)
        if response is None:
            raise HTTPException(status_code=404, detail='Data not found')
        for model in response:
            schema_list.append(schemas.QueryDataItems(vin=model.vin,
                                                      id=model.id,
                                                      datetime=model.datetime,
                                                      chargingPower=model.chargingPower,
                                                      soc=model.soc,
                                                      status=model.status))
        return schema_list
    elif car == 'audi':
        schema_list = []
        response = crud.get_audi_data(db=db)
        if response is None:
            raise HTTPException(status_code=404, detail='Data not found.')
        for model in response:
            schema_list.append(schemas.QueryDataItems(vin=model.vin,
                                                      id=model.id,
                                                      datetime=model.datetime,
                                                      chargingPower=model.chargingPower,
                                                      soc=model.soc,
                                                      status=model.status))
        return schema_list
    elif car == 'tesla':
        schema_list = []
        response = crud.get_tesla_data(db=db)
        if response is None:
            raise HTTPException(status_code=404, detail='Data not found.')
        for model in response:
            schema_list.append(schemas.QueryDataItems(vin=model.vin,
                                                      id=model.id,
                                                      datetime=model.datetime,
                                                      chargingPower=model.chargingPower,
                                                      soc=model.soc,
                                                      status=model.status))
        return schema_list
    elif car == 'all':
        schema_list = []
        porsche = crud.get_porsche_data(db=db)
        audi = crud.get_audi_data(db=db)
        tesla = crud.get_tesla_data(db=db)

        if porsche is not None:
            for model in porsche:
                schema_list.append(schemas.QueryDataItems(vin=model.vin,
                                                          id=model.id,
                                                          datetime=model.datetime,
                                                          chargingPower=model.chargingPower,
                                                          soc=model.soc,
                                                          status=model.status))
        if audi is not None:
            for model in audi:
                schema_list.append(schemas.QueryDataItems(vin=model.vin,
                                                          id=model.id,
                                                          datetime=model.datetime,
                                                          chargingPower=model.chargingPower,
                                                          soc=model.soc,
                                                          status=model.status))

        if tesla is not None:
            for model in tesla:
                schema_list.append(schemas.QueryDataItems(vin=model.vin,
                                                          id=model.id,
                                                          datetime=model.datetime,
                                                          chargingPower=model.chargingPower,
                                                          soc=model.soc,
                                                          status=model.status))

        if not schema_list:
            raise HTTPException(status_code=404, detail='No data was found.')
        return schema_list
    else:
        raise HTTPException(status_code=404, detail='Car with a given name not found.')


@query.get('/average/{car}', response_model=list[schemas.QueryAverage], status_code=200, tags=['query'])
async def query_car_average(car: str,
                            db: Session = Depends(get_db),
                            api_key: APIKey = Depends(get_api_key)):
    """
    Averages first must be stored in the database by api/v1/store/average\n
    Get average of all cars or selected car.\n
    Available parameters are:  <b>porsche, tesla, audi, all</b>
    """
    response = crud.get_average(db=db, which=car)
    if not response:
        raise HTTPException(status_code=404, detail='Could not find average for a given car/cars')
    response_schema = []
    for model in response:
        response_schema.append(schemas.QueryAverage(id=model.id,
                                                    vin=model.vin,
                                                    average=model.average))
    return response_schema
