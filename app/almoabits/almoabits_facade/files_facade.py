import datetime
import os
import pandas as pd
from app.almoabits.almoabits_sql.global_etl import GlobalEtl
from app.almoabits.almoabits_utils import database, config
from app.almoabits.almoabits_utils.utils import synthetic_uuid, csv_dtype


class FilesFacade:
    def __init__(self, db: database = None, schema: str = None):
        self.__global_etl = None
        print(f'inicio de fachada de archivos')
        self.path = config.settings.PATH
        self.db = db
        self.schema = schema

    def run(self):
        self.__global_etl = GlobalEtl(self.db, self.schema)
        print('validar los archivos')
        df = self.validate_load()
        print('carga todos los archivos')
        self.__load_files(df)
        print('procesar los archivos a cargar')
        df = self.read_files(df)
        return df
    def validate_load(self) -> pd.DataFrame():
        try:
            print('validar el archivo en bd si el archivo esta cargado')
            df = pd.DataFrame()
            files = os.listdir(self.path)
            print('empieza a buscar cuales archivos se han cargado y cuales no')
            df_exist = self.__global_etl.searchLoadFile(files)
            print('lista de existentes')
            df_new_files = pd.DataFrame(files, columns=['name'])
            if not df_exist.empty:
                df = df_exist.merge(df_new_files, left_on='name', right_on='name', how='right').query(
                    'load_date.isna()')
            else:
                df = df_new_files

            df['load_date'] = datetime.datetime.today()
            df = synthetic_uuid(df, 'id')
            return df
        except Exception as e:
            raise e

    def __load_files(self, df: pd.DataFrame()):
        print('carga de la carpeta local todos los archivos')
        self.__global_etl.insert(df.to_dict(orient='records'))

    def read_files(self, df: pd.DataFrame()) -> pd.DataFrame():
        try:
            print('leer los archivos y retornar dataframe con los datos de los arhivos a cargar')
            df_file = pd.DataFrame()
            for file in df['name']:
                temp = pd.read_csv(self.path + file,dtype = csv_dtype)
                temp['origin'] = self.path + file
                df_file = df_file._append(temp, ignore_index=True)
            return df_file
        except Exception as e:
            print('ERROR LEYENDO ARCHIVOS')
            raise


# #
# database1 = database.SessionLocal()
# FilesFacade(database1, 'control_cargue').run()
