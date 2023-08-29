from app.almoabits.almoabits_utils.database import Base
from sqlalchemy import Column, String, Integer


class ControlArchivos(Base):
    __tablename__ = 'control_cargue'
    id = Column(String, primary_key=True, nullable=False)
    name = Column(String)
    load_date = Column(String)


class DwhMccmnc(Base):
    __tablename__ = 'dim_mccmnc'
    id = Column(String, primary_key=True, nullable=False)
    id_pais = Column(String)
    country_code = Column(String)
    mcc = Column(String)
    mnc = Column(String)
    brand = Column(String)
    operator = Column(String)
    load_date = Column(String)


class DwhCountry(Base):
    __tablename__ = 'dim_country'
    id = Column(String, primary_key=True, nullable=False)
    alpha_2=Column(String)
    alpha_3=Column(String)
    name=Column(String)
    numeric=Column(String)
    official_name=Column(String)
    load_date = Column(String)

class DwhDate(Base):
    __tablename__ = 'dim_date'
    id = Column(String, primary_key=True, nullable=False)
    date=Column(String)
    day=Column(String)
    day_num =Column(Integer)
    day_week_num =Column(Integer)
    week=Column(Integer)
    month_name = Column(String)
    month_num = Column(Integer)
    quarter=Column(Integer)
    year=Column(Integer)
