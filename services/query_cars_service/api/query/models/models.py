from sqlalchemy import DateTime, Column, Float, String, Date, Integer
from ..db.connect.db import Base


class Cars(Base):
    """Represents a database table of information about cars"""
    __tablename__ = 'cars'

    id = Column(Integer, primary_key=True)
    made = Column(String(20))
    model = Column(String(20))
    year = Column(Date)
    vin = Column(String(20))

    class Config:
        orm_mode = True


class QueryCar(Cars):
    """Represents model of creating query result of a car with current soc"""
    current_soc = Column(Float, index=True)


class Tesla(Base):
    """Represents a database table of information about tesla car usage"""
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
    """Represents a database table of information about audi car usage"""
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
    """Represents a database table of information about porsche car usage"""
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
    """Represents a database table of information about cars average charging power"""
    __tablename__ = 'average'

    id = Column(Integer, primary_key=True)
    vin = Column(String, index=True)
    average = Column(Float, index=True)

    class Config:
        orm_mode = True
