from typing import Type
from database import Database

def show_complete_db(database_class: Type[Database]):
    seperator = '-'*100
    for table in database_class.table_names:
        print(seperator)
        print(f'Table {table}')
        print(seperator)
        data = database_class.fetch_data(table_name=table)
        for row in data:
            print(row)
