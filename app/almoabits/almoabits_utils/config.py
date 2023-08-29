# app/config.py

import os

from pydantic import BaseSettings, Field

MAX_DATAFRAME_SIZE = 1000


class Settings(BaseSettings):
    db_url: str = Field(..., env='DATABASE_URL')
    PATH : str = Field(..., env='FILES_PATH')
    start_date:str = Field(..., env='DIM_DATA_START_DATE')#'2000-01-01'
    end_date: str = Field(..., env='DIM_DATA_END_DATE')#'2050-12-31'


settings = Settings()
