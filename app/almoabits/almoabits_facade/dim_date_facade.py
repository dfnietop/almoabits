import pandas as pd

from app.almoabits.almoabits_sql.global_etl import GlobalEtl
from app.almoabits.almoabits_utils import database, utils, config


class DimDateFacade:
    def __init__(self,db:database,table:str):
        self.database= db
        self.table = table
        self.start_date = config.settings.start_date
        self.end_date = config.settings.end_date
        self.__global_etl = None

    def create_date_table(self):
        try:
            df = pd.DataFrame({"date": pd.date_range(self.start_date, self.end_date)})
            df = utils.synthetic_uuid(df, 'id')
            df["day"] = df['date'].dt.day_name()
            df["day_week_num"] = df['date'].dt.weekday
            df["day_num"] = df['date'].dt.day
            df["month_name"] = df['date'].dt.month_name()
            df["month_num"] = df['date'].dt.month
            df["quarter"] = df['date'].dt.quarter
            df["year"] = df['date'].dt.year

            return df.dropna()
        except Exception as e:
            print('Error genernado dimension de tiempo')
            raise 

    def run(self):
        self.__global_etl = GlobalEtl(self.database, self.table)
        df = self.create_date_table()
        self.__global_etl.insert(df.to_dict(orient='records'))
        return df



