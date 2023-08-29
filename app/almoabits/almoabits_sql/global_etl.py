from collections import deque

import numpy as np
import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.almoabits.almoabits_core import schema, model
from app.almoabits.almoabits_utils import database, config, sql


class GlobalEtl:
    def __init__(self, db: Session, schemma: str):
        print('inicio etl')
        self.db = db
        self.schema = schemma

    def insert(self, data: list):
        try:
            print(f'insertar:{self.schema}')

            if self.schema == 'control_cargue':
                mod = model.ControlArchivos
            elif self.schema == 'dim_date':
                mod = model.DwhDate
            elif self.schema == 'dim_mccmnc':
                mod = model.DwhMccmnc
            else:
                raise

            number_of_chunks = int(len(data) / config.MAX_DATAFRAME_SIZE) + 1
            # sub_df = list(self.split_list(data,number_of_chunks))

            # for i, chunk in enumerate(sub_df):
            #     if len(chunk)>0:
                    # chunk = chunk.reset_index()
            self.db.bulk_insert_mappings(mod, data)
            self.db.commit()

        except Exception as e:
            raise e


    def searchLoadFile(self, parameter):
        try:
            print(f'select proccess ')
            return pd.DataFrame(self.db.execute(text(sql.CARGUE_ARCHIVOS_SQL),[{"file_list":parameter}]).fetchall())
        except Exception as e:
            raise e

    def split_list(self, input_list, chunk_size):
        deque_obj = deque(input_list)
        # While the deque object is not empty
        chunk = []
        while deque_obj:
            # Pop chunk_size elements from the left side of the deque object
            # and append them to the chunk list
            for _ in range(chunk_size):
                if deque_obj:
                    chunk.append(deque_obj.popleft())
        return  chunk