import pandas as pd
import datetime
from app.almoabits.almoabits_sql.global_etl import GlobalEtl
from app.almoabits.almoabits_utils import database, utils, config
import pycountry


class DimCountryFacade:
    def __init__(self, db: database, table: str):
        self.database = db
        self.table = table
        self.__global_etl = GlobalEtl(self.database, self.table)

    def create_date_table(self):
        try:
            df_countries = self.__get_countries()
            df_countries =utils.synthetic_uuid(df_countries, 'id')
            df_countries['load_date'] = datetime.datetime.now()

            return df_countries
        except Exception as e:
            print('Error genernado dimension de tiempo')
            raise

    def run(self):
        df = self.create_date_table()
        self.__global_etl.insert(df.to_dict(orient='records'))
        return df

    def __get_countries(self):
        try:
            df_countries = pd.DataFrame()
            countries = pycountry.countries
            for country in countries:
                temp = dict
                temp = {'alpha_2':country.alpha_2,'alpha_3':country.alpha_3,'name':country.name,'numeric':country.numeric}
                df_countries=df_countries._append(pd.DataFrame.from_dict(temp, orient='index').T)

            return df_countries
        except Exception as e:
            print('error en obtencion de country')
            return 'n/a'
