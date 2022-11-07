from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from ..models import models

# param -
# all - all cars
# tesla, porsche itd. - one car
# plus current charge

cars_vin_list = {
    'porsche': "PL110212",
    'tesla': "PL090201",
    'audi': "PL990011"
}


def query_car_info(db: Session, vin: str):
    """
    Queries the 'cars' table and returns information about a car with given vin.
    """
    return db.query(models.Cars) \
        .filter(models.Cars.vin == vin) \
        .first()


def query_current_charge_porsche(db: Session):
    """

    """
    return db.query(models.Porsche.soc, func.max(models.Porsche.datetime)) \
        .group_by(models.Porsche.soc, models.Porsche.datetime) \
        .order_by(models.Porsche.datetime.desc()) \
        .first()


def query_current_charge_audi(db: Session):
    return db.query(models.Audi.soc, func.max(models.Audi.datetime)) \
        .group_by(models.Audi.soc, models.Audi.datetime) \
        .order_by(models.Audi.datetime.desc()) \
        .first()


def query_current_charge_tesla(db: Session):
    return db.query(models.Tesla.soc, func.max(models.Tesla.datetime)) \
        .group_by(models.Tesla.soc, models.Tesla.datetime) \
        .order_by(models.Tesla.datetime.desc()) \
        .first()


# Get porsche info
def get_porsche_info(db: Session):
    porsche_info = query_car_info(db=db, vin=cars_vin_list.get('porsche'))
    if porsche_info is not None:
        porsche_info = porsche_info.__dict__
        current_soc = query_current_charge_porsche(db=db)[0]
        db_porsche = models.QueryCar(id=porsche_info.get('id'),
                                     made=porsche_info.get('made'),
                                     model=porsche_info.get('model'),
                                     year=porsche_info.get('year'),
                                     vin=porsche_info.get('vin'),
                                     current_soc=current_soc)
        return db_porsche
    return None


# Get Audi info
def get_audi_info(db: Session):
    audi_info = query_car_info(db=db, vin=cars_vin_list.get('audi'))
    if audi_info is not None:
        audi_info = audi_info.__dict__
        current_soc = query_current_charge_audi(db=db)[0]
        db_audi = models.QueryCar(id=audi_info.get('id'),
                                  made=audi_info.get('made'),
                                  model=audi_info.get('model'),
                                  year=audi_info.get('year'),
                                  vin=audi_info.get('vin'),
                                  current_soc=current_soc)
        return db_audi
    return None


# Get Tesla info
def get_tesla_info(db: Session):
    tesla_info = query_car_info(db=db, vin=cars_vin_list.get('tesla'))
    if tesla_info is not None:
        tesla_info = tesla_info.__dict__
        current_soc = query_current_charge_tesla(db=db)[0]
        db_tesla = models.QueryCar(id=tesla_info.get('id'),
                                   made=tesla_info.get('made'),
                                   model=tesla_info.get('model'),
                                   year=tesla_info.get('year'),
                                   vin=tesla_info.get('vin'),
                                   current_soc=current_soc)
        return db_tesla
    return None


def get_cars_info(db: Session, which: str):
    response_list = []
    if which == 'all':
        porsche = get_porsche_info(db=db)
        if porsche is not None:
            response_list.append(porsche)
        audi = get_audi_info(db=db)
        if audi is not None:
            response_list.append(audi)
        tesla = get_tesla_info(db=db)
        if tesla is not None:
            response_list.append(tesla)
    elif which == 'audi':
        audi = get_audi_info(db=db)
        if audi is not None:
            response_list.append(audi)
    elif which == 'porsche':
        porsche = get_porsche_info(db=db)
        if porsche is not None:
            response_list.append(porsche)
    elif which == 'tesla':
        tesla = get_tesla_info(db=db)
        if tesla is not None:
            response_list.append(tesla)
    return response_list


def get_porsche_data(db: Session):
    """
    Return Porsche data (usage info).
    """
    models_list = []
    query = db.query(models.Porsche).all()
    if query:
        for data in query:
            model = models.Porsche(id=data.id,
                                   datetime=data.datetime,
                                   vin=data.vin,
                                   soc=data.soc,
                                   status=data.status,
                                   chargingPower=data.chargingPower)
            models_list.append(model)
        return models_list
    return None


def get_audi_data(db: Session):
    """
    Return Audi data (usage info).
    """
    models_list = []
    query = db.query(models.Audi).all()
    if query:
        for data in query:
            model = models.Audi(id=data.id,
                                datetime=data.datetime,
                                vin=data.vin,
                                soc=data.soc,
                                status=data.status,
                                chargingPower=data.chargingPower)
            models_list.append(model)
        return models_list
    return None


def get_tesla_data(db: Session):
    """
    Return Tesla data (usage info).
    """
    models_list = []
    query = db.query(models.Tesla).all()
    if query:
        for data in query:
            model = models.Tesla(id=data.id,
                                 datetime=data.datetime,
                                 vin=data.vin,
                                 soc=data.soc,
                                 status=data.status,
                                 chargingPower=data.chargingPower)
            models_list.append(model)
        return models_list
    return None


def query_average_charging_power(vin: str, db: Session):
    """
    Query database for average charging power of a car with a given vin
    """
    return db.query(models.Average.id, models.Average.vin, models.Average.average) \
        .filter(models.Average.vin == vin) \
        .first()


def create_average_model(id: int, vin: str, average: float):
    """
    Creates and returns new average model, used in function get_average()
    """
    return models.Average(id=id,
                          vin=vin,
                          average=average)


def get_average(which: str, db: Session):
    """
    Queries the database for the average of a given car or all cars
    and returns list of results.
    :param which: porsche, tesla, audi, all
    :param db:
    :return:
    """
    response_list = []
    if which == 'all' or which == '':
        avg_porsche = query_average_charging_power(db=db, vin=cars_vin_list.get('porsche'))
        avg_audi = query_average_charging_power(db=db, vin=cars_vin_list.get('audi'))
        avg_tesla = query_average_charging_power(db=db, vin=cars_vin_list.get('tesla'))

        if avg_porsche is not None:
            db_porsche = create_average_model(avg_porsche[0], avg_porsche[1], avg_porsche[2])
            response_list.append(db_porsche)

        if avg_audi is not None:
            db_audi = create_average_model(avg_audi[0], avg_audi[1], avg_audi[2])
            response_list.append(db_audi)

        if avg_tesla is not None:
            db_tesla = create_average_model(avg_tesla[0], avg_tesla[1], avg_tesla[2])
            response_list.append(db_tesla)

    elif which == 'porsche' or which == cars_vin_list.get('porsche'):
        avg_porsche = query_average_charging_power(db=db, vin=cars_vin_list.get('porsche'))
        if avg_porsche is not None:
            db_porsche = create_average_model(avg_porsche[0], avg_porsche[1], avg_porsche[2])
            response_list.append(db_porsche)
    elif which == 'audi' or which == cars_vin_list.get('audi'):
        avg_audi = query_average_charging_power(db=db, vin=cars_vin_list.get('audi'))
        if avg_audi is not None:
            db_audi = create_average_model(avg_audi[0], avg_audi[1], avg_audi[2])
            response_list.append(db_audi)
    elif which == 'tesla' or which == cars_vin_list.get('tesla'):
        avg_tesla = query_average_charging_power(db=db, vin=cars_vin_list.get('tesla'))
        if avg_tesla is not None:
            db_tesla = create_average_model(avg_tesla[0], avg_tesla[1], avg_tesla[2])
            response_list.append(db_tesla)

    return response_list
