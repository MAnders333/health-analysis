import sqlite3
import os
import re
from typing import List, Optional
from errors import TableDoesNotExistError


class Database:

    def __init__(self, db_name: str, path: str=os.getcwd()) -> None:
        self.db_name = db_name
        self.path = path
        self.conn = sqlite3.connect(f'{self.path}{self.db_name}')
        self.c = self.conn.cursor()
        self.table_names = [name[0] for name in self.c.execute("""SELECT name from sqlite_master where type='table'""").fetchall()]
        print(f'Successfully connected to {db_name}')

    def generate_sql_create_table_command(self, table_name:str, column_names: list, data_types: list) -> str:
        if len(column_names) != len(data_types):
            raise ValueError('Specified lists of column names and data types do not have equal length.')  
        
        sql_create_table_command = f'CREATE TABLE {table_name} ('
        for i, column_name in enumerate(column_names):
            data_type = data_types[i]
            if column_name != column_names[-1]:
                sql_create_table_command = f'{sql_create_table_command}{column_name} {data_type.upper()}, '
            else:
                sql_create_table_command = f'{sql_create_table_command}{column_name} {data_type.upper()})'
        return sql_create_table_command

    def table_exists(self, table_name: str) -> bool:
        return table_name in self.table_names

    def create_table(self, table_name: str, column_names: list, data_types: list) -> None:
        if self.table_exists(table_name):
            raise ValueError('Specified table already exists.')
        
        self.c.execute(self.generate_sql_create_table_command(table_name, column_names, data_types))
        self.table_names.append(table_name)
        print(f'Table {table_name} successfully created')
    
    def get_column_names_of_table(self, table_name:str) -> list:
        if not self.table_exists(table_name):
            raise TableDoesNotExistError
        
        cursor = self.c.execute(f"""SELECT * FROM {table_name}""")
        column_names = list(map(lambda x: x[0], cursor.description))
        return column_names

    def add_rows(self, table_name: str, data: List[tuple]) -> None:  
        if not self.table_exists(table_name):
            raise TableDoesNotExistError
        
        column_names = self.get_column_names_of_table(table_name)
        for i, row in enumerate(data):
            if len(row) == len(column_names):
                self.c.execute(f'INSERT INTO {table_name} VALUES {row}')
                print(f'{row} added to {table_name}')
            else:
                raise ValueError(f'Row {i+1} has invalid length.')
        self.conn.commit()

    def delete_rows(self, table_name: str, condition: Optional[str]=None) -> None:
        if not self.table_exists(table_name):
            raise TableDoesNotExistError
        
        if condition is None:
            self.c.execute(f'DELETE FROM {table_name}')
            print('Table {table_name} was successfully deleted.')
        else:
            try:
                self.c.execute(f"""DELETE FROM {table_name} WHERE {condition}""")
                print(f'Row(s) successfully deleted where {condition}')
            except:
                raise ValueError('Specified condition is invalid. Try again.')
        self.conn.commit()

    def genereate_sql_update_command(self, table_name: str, column_names: List[str], set_values: list, condition: str) -> str:
        if len(column_names) != len(set_values):
            raise ValueError('Specified column names and set values do not match.')

        sql_update_command = f'UPDATE {table_name} SET '
        for i, column_name in enumerate(column_names):
            set_value = set_values[i]
            if i != len(column_names) - 1:
                sql_update_command = f'{sql_update_command}{column_name}={set_value}, '
            else:
                sql_update_command = f'{sql_update_command}{column_name}={set_value} WHERE {condition}'
        return sql_update_command

    def update_rows(self, table_name: str, column_names: List[str], set_values: list, condition: str) -> None:
        if not self.table_exists(table_name):
            raise TableDoesNotExistError
        
        if condition is None:
            raise ValueError('Please specify a condition to update rows.')

        self.c.execute(self.genereate_sql_update_command(table_name, column_names, set_values, condition))
        print(f'Table {table_name} successfully updated where {condition}')
        self.conn.commit()
        
    def generate_sql_select_command(self, table_name: str, column_names: Optional[List[str]]=None, condition: Optional[str]=None) -> str:
        if column_names is None and condition is None:
            sql_select_command = f'SELECT * FROM {table_name}'
        elif column_names is None and condition is not None:
            sql_select_command = f'SELECT * FROM {table_name} WHERE {condition}'
        else:
            sql_select_command = f'SELECT '
            for column_name in column_names:
                if column_name != column_names[-1]:
                    sql_select_command = f'{sql_select_command}{column_name}, '
                else:
                    sql_select_command = f'{sql_select_command}{column_name} '
            sql_select_command = f'{sql_select_command}FROM {table_name}'
            if condition is not None:
                sql_select_command = f'{sql_select_command} WHERE {condition}'
        return sql_select_command

    def fetch_data(self, table_name: str ,column_names: Optional[List[str]]=None, condition: Optional[str]=None) -> list:
        if not self.table_exists(table_name):
            raise TableDoesNotExistError

        data = self.c.execute(self.generate_sql_select_command(table_name, column_names, condition)).fetchall()
        return data

if __name__ == "__main__":
    pass



