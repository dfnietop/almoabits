from app.almoabits.almoabits_facade.dwh_facade import DataWareHouseFacade
from app.almoabits.almoabits_facade.files_facade import FilesFacade
from app.almoabits.almoabits_utils import database, sql


class almoabitsFacade:
    def __init__(self, db: database):
        self.database = db

    def run(self):
        print('inicia proceso de cargue de archivos')
        process = FilesFacade(self.database,'control_cargue')
        df = process.run()
        print('inicia proceso de cargue de preparacion de data wareHouse')
        if not df.empty:
            process_data = DataWareHouseFacade(self.database)
            process_data.run(df)


