from fastapi import Depends, APIRouter, HTTPException
from fastapi.openapi.models import APIKey
from sqlalchemy.orm import Session

from ..db import crud
from ..models import schemas
from ..db.db import SessionLocal
from ..auth.auth import get_api_key

store = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@store.get('/', status_code=200, include_in_schema=False)
def store_check():
    return {'detail': 'Store service is up.'}


# Insert cars
@store.post('/cars/', response_model=list[schemas.CreateCar], status_code=201)
async def store_cars(car: schemas.Car,
                     db: Session = Depends(get_db),
                     api_key: APIKey = Depends(get_api_key)):
    """
    Store information about cars in the database.
    """
    response = crud.store_cars(car=car, db=db)
    schema_list = []  # List of models converted to schemas
    if not response:
        raise HTTPException(status_code=409, detail='Data already exists in database.')
    # Conversion from models to schemas
    for model in response:
        schema_list.append(schemas.CreateCar(made=model.made,
                                             model=model.model,
                                             year=model.year,
                                             vin=model.vin))
    return schema_list


@store.post('/porsche/', response_model=list[schemas.CreatePorsche], status_code=201)
async def store_porsche(porsche: schemas.Porsche,
                        db: Session = Depends(get_db),
                        api_key: APIKey = Depends(get_api_key)):
    """
    Store information about porsche in database.
    """
    response = crud.store_porsche(db=db, porsche=porsche)
    schema_list = []  # List of models converted to schemas
    if not response:
        raise HTTPException(status_code=409, detail='Data already exists in database.')
    # Conversion from models to schemas
    for model in response:
        schema_list.append(schemas.CreatePorsche(vin=model.vin,
                                                 datetime=model.datetime,
                                                 soc=model.soc,
                                                 chargingPower=model.chargingPower,
                                                 status=model.status))
    return schema_list


# Inserts audi into database
@store.post('/audi/', response_model=list[schemas.CreateAudi], status_code=201)
async def store_audi(audi: schemas.Audi,
                     db: Session = Depends(get_db),
                     api_key: APIKey = Depends(get_api_key)):
    """
    Store information about audi in database.
    """
    response = crud.store_audi(db=db, audi=audi)
    schema_list = []
    if not response:
        raise HTTPException(status_code=409, detail='Data already exists in database.')
    for model in response:
        schema_list.append(schemas.CreateAudi(vin=model.vin,
                                              datetime=model.datetime,
                                              soc=model.soc,
                                              chargingPower=model.chargingPower,
                                              status=model.status))
        return schema_list


# Inserts tesla into database
@store.post('/tesla/', response_model=list[schemas.CreateTesla], status_code=201)
async def store_tesla(tesla: schemas.Tesla,
                      db: Session = Depends(get_db),
                      api_key: APIKey = Depends(get_api_key)):
    """
    Store information about tesla in database.
    """
    response = crud.store_tesla(db=db, tesla=tesla)
    schema_list = []
    if not response:
        raise HTTPException(status_code=409, detail='Data already exists in database.')
    for model in response:
        schema_list.append(schemas.CreateTesla(vin=model.vin,
                                               datetime=model.datetime,
                                               soc=model.soc,
                                               chargingPower=model.chargingPower,
                                               status=model.status))
        return schema_list


@store.get('/average/', response_model=list[schemas.Average], status_code=200)
async def store_average(db: Session = Depends(get_db),
                        api_key: APIKey = Depends(get_api_key)):
    """
    Store information about average in database.
    """
    response = crud.store_average(db=db)
    schema_list = []  # List of models converted to schemas
    if not response:
        raise HTTPException(status_code=409, detail='Data already exists in database or there was no cars to be stored.')
    for model in response:
        schema_list.append(schemas.Average(vin=model.vin,
                                           average=model.average))
    return schema_list
