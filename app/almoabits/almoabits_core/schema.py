from pydantic import BaseModel


class CargueArchivos(BaseModel):
    id: str
    name: str
    load_date: str

    class Config:
        orm_mode = True


class DWHDimDate(BaseModel):
    id: str
    date = str
    day = str
    day_num = int
    day_week_num = int
    week = int
    month_name = str
    month_num = int
    quarter = int
    year = int

    class Config:
        orm_mode = True


class DWHDimMccMnc(BaseModel):
    id = str
    id_pais = str
    country_code = str
    mcc = str
    mnc = str
    brand = str
    operator = str
    load_date = str

    class Config:
        orm_mode = True

class DWHDimCountry(BaseModel):
    id = str
    alpha_2 = str
    alpha_3 = str
    name = str
    numeric = str
    load_date = str

    class Config:
        orm_mode = True
