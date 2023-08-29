import pandas as pd

from app.almoabits.almoabits_facade.dim_country_facade import DimCountryFacade
from app.almoabits.almoabits_facade.dim_date_facade import DimDateFacade
from app.almoabits.almoabits_facade.dim_mccmnc_facade import DimMccmncFacade
from app.almoabits.almoabits_facade.fac_almoabits_facade import FactAlmoabitsFacade
from app.almoabits.almoabits_sql.global_etl import GlobalEtl
from app.almoabits.almoabits_utils import database, sql


class DataWareHouseFacade:

    def __init__(self, db: database):
        print('constructor DWH')
        self.db = db

    def run(self, data):
        try:
            print('comienzo proceso de DWH')
            dim_date, dim_mccmnc, dim_country = self.prepare_dim(data)
            self.prepare_fact_table(data, dim_date, dim_mccmnc, dim_country)
        except Exception as e:
            print('error en el ejecutor de DWH')
            raise e

    def prepare_dim(self, df):
        try:
            dim_date_facade = DimDateFacade(self.db, 'dim_date')
            dim_date = dim_date_facade.run()
            dim_country_facade = DimCountryFacade(self.db, 'dim_country')
            dim_country = dim_country_facade.run()
            dim_mccmnc_facade = DimMccmncFacade(self.db, 'dim_mccmnc', df, dim_country)
            dim_mccmnc = dim_mccmnc_facade.run()
            return dim_date, dim_mccmnc, dim_country
        except Exception as e:
            print('Error en el proceso de Creacion de Dimensiones')
            raise

    def prepare_fact_table(self, data: pd.DataFrame, dim_date: pd.DataFrame, dim_mccmnc: pd.DataFrame,
                           dim_country: pd.DataFrame):
        try:
            df_fact_almoabits= FactAlmoabitsFacade(self.db, 'fact_almoabits', data,dim_mccmnc, dim_country,dim_date)
            df_fact_almoabits.run()

        except Exception as e:
            print('Error en el proceso de Creacion de Dimensiones')
            raise
