import datetime

import pandas as pd
from sqlalchemy.dialects.mssql.information_schema import columns

from app.almoabits.almoabits_sql.global_etl import GlobalEtl
from app.almoabits.almoabits_utils import database, utils, config
import mobile_codes


class DimMccmncFacade:
    def __init__(self, db: database, table: str, data: pd.DataFrame(), df_country: pd.DataFrame()):
        self.database = db
        self.table = table
        self.data = data
        self.df_country = df_country
        self.__global_etl = GlobalEtl(self.database, self.table)

    def create_date_table(self):
        try:

            dim_mccmnc = self.data[['COUNTRY_ISO3', 'MCC', 'MNC']]
            dim_mccmnc = dim_mccmnc.rename(columns={'COUNTRY_ISO3': 'country_code', 'MCC': 'mcc', 'MNC': 'mnc'})
            dim_mccmnc = dim_mccmnc.drop_duplicates()

            dim_mccmnc = utils.synthetic_uuid(dim_mccmnc, 'id')
            dim_mccmnc['brand'] = dim_mccmnc.apply(lambda x: self.__get_brand(x['mcc'], x['mnc']), axis=1)
            dim_mccmnc['operator'] = dim_mccmnc.apply(lambda x: self.__get_operator(x['mcc'], x['mnc']), axis=1)
            dim_mccmnc['load_date'] = datetime.datetime.now()
            dim_mccmnc = dim_mccmnc.merge(self.df_country[['id', 'alpha_3']], left_on='country_code',
                                          right_on='alpha_3', how='left')
            dim_mccmnc = dim_mccmnc.rename(columns={'id_x': 'id', 'id_y': 'id_pais'})
            dim_mccmnc = dim_mccmnc[['id', 'brand', 'operator', 'load_date', 'id_pais','mcc','mnc']]
            dim_mccmnc = dim_mccmnc.drop_duplicates()
            return dim_mccmnc
        except Exception as e:
            print('Error genernado dimension de tiempo')
            raise

    def run(self):
        try:
            df = self.create_date_table()
            self.__global_etl.insert(df.to_dict(orient='records'))
            return df
        except Exception as e:
            print('Error procesando dimension mccmcn')
            raise

    def __get_brand(self, mcc_code, mnc_code: str):
        try:
            brand = mobile_codes.mcc_mnc(mcc_code, mnc_code)
            return brand.brand
        except Exception as e:
            print('error en obtencion de brand')
            return 'n/a'

    def __get_operator(self, mcc_code, mnc_code: str):
        try:
            brand = mobile_codes.mcc_mnc(mcc_code, mnc_code)
            return brand.operator
        except Exception as e:
            print('error en obtencion de operador')
            return 'n/a'
