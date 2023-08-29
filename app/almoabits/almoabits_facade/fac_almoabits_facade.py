import datetime

import pandas as pd
from sqlalchemy.dialects.mssql.information_schema import columns

from app.almoabits.almoabits_sql.global_etl import GlobalEtl
from app.almoabits.almoabits_utils import database, utils, config
import mobile_codes


class FactAlmoabitsFacade:
    def __init__(self, db: database, table: str,
                 data: pd.DataFrame,
                 dim_mccmnc: pd.DataFrame,
                 dim_country: pd.DataFrame,
                 dim_date: pd.DataFrame):

        self.database = db
        self.table = table
        self.data = data
        self.dim_country = dim_country
        self.dim_mccmnc = dim_mccmnc
        self.dim_date = dim_date
        self.__global_etl = GlobalEtl(self.database, self.table)

    def create_date_table(self):
        try:
            fact_almoabits = pd.DataFrame()
            fact_almoabits = self.prepare_date()
            fact_almoabits = self.prepare_mccmnc(fact_almoabits)
            fact_almoabits = self.prepare_country(fact_almoabits)
            fact_almoabits = utils.synthetic_uuid(fact_almoabits, 'id')
            return fact_almoabits
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

    def prepare_date(self) -> pd.DataFrame:
        try:
            print('prepare dimension tiempo')
            df = self.data
            df['start_date'] = df['CONNECT_TIME'].astype(str).apply(self.prepare_date_format)
            self.dim_date['date'] = pd.to_datetime(self.dim_date['date'].astype(str), format='%Y-%m-%d')
            df['start_date'] = pd.to_datetime(df['start_date'].astype(str), format='%Y-%m-%d')
            df = self.data.merge(self.dim_date[['id', 'date']], left_on='start_date', right_on='date', how='left')
            df = df[['CDR_ID', 'ICCID', 'TYPE', 'CONNECT_TIME', 'CLOSE_TIME', 'DURATION',
                     'DIRECTION', 'CALLED_PARTY', 'CALLING_PARTY', 'COUNTRY_ISO3',
                     'MCC', 'MNC', 'IMSI_ID', 'IMSI_NO', 'INVENTORY_ID',
                     'COMPANY_NAME', 'PACKAGE_ID', 'id']]
            df = df.rename(columns={'CDR_ID': 'cdr_id', 'ICCID': 'iccid', 'TYPE': 'type',
                                    'CONNECT_TIME': 'connect_time', 'CLOSE_TIME': 'close_time',
                                    'DURATION': 'duration', 'DIRECTION': 'direction',
                                    'CALLED_PARTY': 'called_party', 'CALLING_PARTY': 'calling_party',
                                    'COUNTRY_ISO3': 'country_code', 'MCC': 'mcc', 'MNC': 'mnc',
                                    'IMSI_ID': 'imsi_id', 'IMSI_NO': 'imsi_no', 'INVENTORY_ID': 'inventory_id',
                                    'COMPANY_NAME': 'company_name', 'PACKAGE_ID': 'package_id', 'id': 'date_id'})
            return df
        except Exception as e:
            print('error prapare dimension de tiempo')
            raise e

    def prepare_mccmnc(self, data: pd.DataFrame) -> pd.DataFrame:
        try:
            print('prepare dimension mccmnc')
            data = data.merge(self.dim_mccmnc[['id', 'mcc', 'mnc']], left_on=['mcc', 'mnc'], right_on=['mcc', 'mnc'],
                              how='left')
            data = data.rename(columns={'id': 'mmc_mnc_id'})
            data = data[['cdr_id', 'iccid', 'type', 'connect_time', 'close_time', 'duration',
                         'direction', 'called_party', 'calling_party', 'country_code',
                         'imsi_id', 'imsi_no', 'inventory_id',
                         'company_name', 'package_id', 'date_id', 'mmc_mnc_id']]
            return data
        except Exception as e:
            print('error prapare dimension de mccmnc')

    def prepare_country(self, data) -> pd.DataFrame:
        try:
            print('prepare dimension country')
            data = data.merge(self.dim_country[['id', 'alpha_3']], left_on=['country_code'], right_on=['alpha_3'],
                              how='left')
            data = data.rename(columns={'id': 'country_id'})
            data = data[['cdr_id', 'iccid', 'type', 'connect_time', 'close_time', 'duration',
                         'direction', 'called_party', 'calling_party',
                         'imsi_id', 'imsi_no', 'inventory_id',
                         'company_name', 'package_id', 'date_id', 'mmc_mnc_id','country_id']]
            return data
        except Exception as e:
            print('error prapare dimension de pais')

    def prepare_date_format(self, string_date):
        return datetime.datetime.strptime(string_date, '%Y-%m-%dT%H:%M:%S.%f%z').date()
