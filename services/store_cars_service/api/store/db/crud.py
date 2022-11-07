from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from ..models import schemas, models


def get_car_by_vin(db: Session, vin: str):
    return db.query(models.Cars).filter(models.Cars.vin == vin).first()


def store_cars(db: Session, car: schemas.Car):
    car_dict = car.dict()
    db_car_list = []
    for i in range(0, len(car_dict['cars'])):
        check_if_exists = get_car_by_vin(db=db, vin=car_dict['cars'][i]['vin'])
        if not check_if_exists:
            db_car = models.CreateCar(made=car_dict['cars'][i]['made'],
                                      model=car_dict['cars'][i]['model'],
                                      year=car_dict['cars'][i]['year'],
                                      vin=car_dict['cars'][i]['vin'])
            db.add(db_car)
            db.commit()
            db.refresh(db_car)
            db_car_list.append(db_car)
    return db_car_list


# Check if there exists a porsche with that timestamp in database
def get_porsche_by_timestamp(db: Session, timestamp: datetime):
    return db.query(models.Porsche).filter(models.Porsche.datetime == timestamp).first()


# Store porsche
def store_porsche(db: Session, porsche: schemas.Porsche):
    porsche_dict = porsche.dict()
    db_porsche_list = []
    for i in range(0, len(porsche_dict['carStatistics'])):
        check_if_exists = get_porsche_by_timestamp(db=db, timestamp=porsche_dict['carStatistics'][i]['datetime'])
        if not check_if_exists:
            db_porsche = models.CreatePorsche(vin=porsche_dict['vin'],
                                              datetime=porsche_dict['carStatistics'][i]['datetime'],
                                              soc=porsche_dict['carStatistics'][i]['soc'],
                                              chargingPower=porsche_dict['carStatistics'][i]['chargingPower'],
                                              status=porsche_dict['carStatistics'][i]['status'])
            db.add(db_porsche)
            db.commit()
            db.refresh(db_porsche)
            db_porsche_list.append(db_porsche)
    return db_porsche_list


def get_audi_by_timestamp(db: Session, timestamp: datetime):
    return db.query(models.Audi).filter(models.Audi.datetime == timestamp).first()


# Store Audi
def store_audi(db: Session, audi: schemas.Audi):
    audi_dict = audi.dict()
    db_audi_list = []
    for i in range(0, len(audi_dict['carStatistics'])):
        check_if_exists = get_audi_by_timestamp(db=db, timestamp=audi_dict['carStatistics'][i]['datetime'])
        if not check_if_exists:
            db_audi = models.CreateAudi(vin=audi_dict['vin'],
                                        datetime=audi_dict['carStatistics'][i]['datetime'],
                                        soc=audi_dict['carStatistics'][i]['soc'],
                                        chargingPower=audi_dict['carStatistics'][i]['chargingPower'],
                                        status=audi_dict['carStatistics'][i]['status'])
            db.add(db_audi)
            db.commit()
            db.refresh(db_audi)
            db_audi_list.append(db_audi)
    return db_audi_list


def get_tesla_by_timestamp(db: Session, timestamp: datetime):
    return db.query(models.Tesla).filter(models.Tesla.datetime == timestamp).first()


# Store Tesla
def store_tesla(db: Session, tesla: schemas.Tesla):
    tesla_dict = tesla.dict()
    db_tesla_list = []
    for i in range(0, len(tesla_dict['carStatistics'])):
        check_if_exists = get_tesla_by_timestamp(db=db, timestamp=tesla_dict['carStatistics'][i]['datetime'])
        if not check_if_exists:
            db_tesla = models.CreateTesla(vin=tesla_dict['vin'],
                                          datetime=tesla_dict['carStatistics'][i]['datetime'],
                                          soc=tesla_dict['carStatistics'][i]['soc'],
                                          chargingPower=tesla_dict['carStatistics'][i]['chargingPower'],
                                          status=tesla_dict['carStatistics'][i]['status'])
            db.add(db_tesla)
            db.commit()
            db.refresh(db_tesla)
            db_tesla_list.append(db_tesla)
    return db_tesla_list


def find_average_by_vin(db: Session, vin: str):
    return db.query(models.Average).filter(models.Average.vin == vin).first()


# Calculate and store average chargingPower of every car
def store_average(db: Session):
    averages = []
    # Calculate average of Porsche
    result = db.query(func.avg(models.Porsche.chargingPower).
                      label('average'), models.Porsche.vin.label('vin')). \
        filter(models.Porsche.chargingPower != 0). \
        group_by(models.Porsche.vin). \
        first()
    if result is not None:
        db_avg_porsche = models.CreateAverage(vin=result[1],
                                              average=result[0])
        check_if_exists = find_average_by_vin(db=db, vin=db_avg_porsche.vin)
        # Store it in the database if it doesn't already exist
        if not check_if_exists:
            db.add(db_avg_porsche)
            db.commit()
            db.refresh(db_avg_porsche)
        averages.append(db_avg_porsche)

    # Calculate average of Tesla
    result = db.query(func.avg(models.Tesla.chargingPower).
                      label('average'), models.Tesla.vin.label('vin')). \
        filter(models.Tesla.chargingPower != 0). \
        group_by(models.Tesla.vin). \
        first()
    if result is not None:
        db_avg_tesla = models.CreateAverage(vin=result[1],
                                            average=result[0])
        check_if_exists = find_average_by_vin(db=db, vin=db_avg_tesla.vin)
        # Store it in the database if it doesn't already exist
        if not check_if_exists:
            db.add(db_avg_tesla)
            db.commit()
            db.refresh(db_avg_tesla)
            averages.append(db_avg_tesla)

    # Calculate average of Audi
    result = db.query(func.avg(models.Audi.chargingPower).
                      label('average'), models.Audi.vin.label('vin')). \
        filter(models.Audi.chargingPower != 0). \
        group_by(models.Audi.vin). \
        first()
    if result is not None:
        db_avg_audi = models.CreateAverage(vin=result[1],
                                           average=result[0])
        check_if_exists = find_average_by_vin(db=db, vin=db_avg_audi.vin)
        # Store it in the database if it doesn't already exist
        if not check_if_exists:
            db.add(db_avg_audi)
            db.commit()
            db.refresh(db_avg_audi)
            averages.append(db_avg_audi)

    return averages
