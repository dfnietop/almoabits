from app.almoabits.almoabits_facade.dim_country_facade import DimCountryFacade
from app.almoabits.almoabits_facade.dim_date_facade import DimDateFacade
from app.almoabits.almoabits_facade.dim_mccmnc_facade import DimMccmncFacade
from app.almoabits.almoabits_sql.global_etl import GlobalEtl
from app.almoabits.almoabits_utils import database, sql


class DataWareHouseFacade:

    def __init__(self, db: database):
        print('constructor DWH')
        self.db = db
        


    def run(self, df):
        try:
            print('comienzo proceso de DWH')
            df_dwh=self.prepare_dim(df)
        except Exception as e:
            print('error en el ejecutor de DWH')
            raise e

    def prepare_dim(self, df):
        dim_date_facade = DimDateFacade(self.db,'dim_date')
        dim_date_facade.run()
        dim_country_facade = DimCountryFacade(self.db,'dim_country')
        dim_country_facade.run()
        dim_mccmnc_facade = DimMccmncFacade(self.db,'dim_mccmnc',df)
        dim_mccmnc_facade.run()

    def load_dim(self, df_dwh):
        pass


