from sqlalchemy import DateTime, Column, Float, String, Date, Integer
from ..db.connection.db import Base


class Cars(Base):
    __tablename__ = 'cars'

    id = Column(Integer, primary_key=True)
    made = Column(String(20))
    model = Column(String(20))
    year = Column(Date)
    vin = Column(String(20))

    class Config:
        orm_mode = True


class Tesla(Base):
    __tablename__ = 'tesla'

    id = Column(Integer, primary_key=True)
    vin = Column(String(20))
    datetime = Column(DateTime, index=True)
    soc = Column(Integer, index=True)
    chargingPower = Column(Float, index=True)
    status = Column(String, index=True)

    class Config:
        orm_mode = True


class Audi(Base):
    __tablename__ = 'audi'

    id = Column(Integer, primary_key=True)
    vin = Column(String(20))
    datetime = Column(DateTime, index=True)
    soc = Column(Integer, index=True)
    chargingPower = Column(Float, index=True)
    status = Column(String, index=True)

    class Config:
        orm_mode = True


class Porsche(Base):
    __tablename__ = 'porsche'

    id = Column(Integer, primary_key=True)
    vin = Column(String, index=True)
    datetime = Column(DateTime, index=True)
    soc = Column(Integer, index=True)
    chargingPower = Column(Float, index=True)
    status = Column(String, index=True)

    class Config:
        orm_mode = True


class Average(Base):
    __tablename__ = 'average'

    id = Column(Integer, primary_key=True)
    vin = Column(String, index=True)
    average = Column(Float, index=True)

    class Config:
        orm_mode = True
