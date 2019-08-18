"""This module contains the Database class which is used to handle SQLite databases."""

import sqlite3
import os
import re


class Database:
    """Database object that can handle SQLite databases to create tables, add/delete/edit rows in tables, and return requested data."""    

    def __init__(self, path=os.getcwd(), db_name=None):
        """Initializes a Database object with a specified (path and) name. Default path is the current working directory.
        :param path: path to existing directory in which the database will be created
        :param db_name: file name of the database to be created
        :type path: string
        :type db_name: string
        """
        
        # checks whether specified path is valid
        if os.path.exists(path):
            self.path = path
        else:
            raise ValueError('Specified path does not exist or is invalid.')
        
        # checks whether specified name for the database is valid
        if isinstance(db_name, str) and re.match('^\w+\.db$', db_name) is not None:
            self.db_name = db_name
        else:
            raise ValueError('Specified database name is invalid.')
        
        # creates a SQLite database at specified path with specified name
        if self.path[-1] != '/':
            self.conn = sqlite3.connect(f'{self.path}/{self.db_name}')
        else:
            self.conn = sqlite3.connect(f'{self.path}{self.db_name}')

        # initiates cursor in database
        self.c = self.conn.cursor()
        
        # initiates list of tables in SQLite database connection
        self.table_names = [name[0] for name in self.c.execute("""SELECT name from sqlite_master where type='table'""").fetchall()]
        print(f'Database {db_name} successfully created')

    def create_table(self, table_name=None, column_names=None):
        """Creates new table in existing database with specified column_names.
        :param table_name: name of the table to be created
        :param column_names: list of tuples containing column name and data type --> [(column1, TEXT)]
        :type table_name: string
        :type column_names: list of tuples
        :return:
        """
        # checks whether table already exists
        if table_name in self.table_names:
            print(f'Table {table_name} already exists')
            return
        
        # checks whether table_name and column_names have the correct input format
        if not isinstance(table_name, str):
            print(f'The argument table_name must be specified as a string')
            exit(1)
        if not isinstance(column_names, list):
            print(f'The argument column_names must be specified as a list of tuples')
            exit(1)
        
        # checks whether column_names consists of tuples which contain only strings and creates the right string format for SQL statement
        column_names_sql = '('
        for i, header in enumerate(column_names):
            if not isinstance(header, tuple):
                print(f'The list elements of the argument column_names must be specified as tuples')        
                exit(1)
            if len(header) != 2 or not isinstance(header[0], str) or not isinstance(header[1], str):
                print(f'Specified header tuples must have a length of two and only contain strings')
                exit(1)
            column_name = header[0]
            data_type = header[1]
            if i != len(column_names) - 1:
                column_names_sql = column_names_sql + column_name + ' ' + data_type.upper() + ','
            else:
                column_names_sql = column_names_sql + column_name + ' ' + data_type.upper() + ')'

        # creates a new table with specified table name and column_names
        try:
            self.c.execute(f"""CREATE TABLE {table_name} {column_names_sql}""")
        except:
            raise ValueError(f'Specified data types are invalid')

        # appends table name to list of table names
        self.table_names.append(table_name)
        print(f'Table {table_name} successfully created')

    def does_table_exist(self, table_name=None):
        """Checks whether specified table exists in Database
        :param table_name: specifies the table to be checked
        :type table_name: string
        :return:
        """
        if table_name not in self.table_names:
            raise AttributeError('Specified table does not exist.')

    def add_rows(self, table_name=None, data=None):
        """Adds data row in specified table.
        :param table_name: specifies the table to insert the data
        :param data: specifies the data to be inserted
        :type table_name: string
        :type data: list of tuples
        :return:
        """
        # checks whether specified table exists
        self.does_table_exist(table_name)
        
        # fetch column_names from table
        cursor = self.c.execute(f"""SELECT * FROM {table_name}""")
        column_names_of_table = [description[0] for description in cursor.description]
        
        # checks wheter specified data has the right format
        if isinstance(data, list):
            # inserts data row into specified table
            for i, row in enumerate(data):
                if isinstance(row, tuple) and len(row) == len(column_names_of_table):
                    self.c.execute(f"""INSERT INTO {table_name} VALUES {row}""")
                    print(f'{row} added to {table_name}')
                else:
                    raise ValueError(f'Row {i+1} has invalid length.')
        
        # saves changes
        self.conn.commit()

    def delete_rows(self, table_name=None, condition=None):
        """Deletes specified row(s) in specified table.
        :param table_name: specifies the table to delete data from
        :param condition: specifies the condition that rows to be deleted must meet
        :type table_name: string
        :type condition: string
        As strings in SQL must be enclosed in single quotes ('), please enclose condition in double qutoes (").
        :return:
        """
        # checks whether specified table name exists
        self.does_table_exist(table_name)
        
        # checks whether conditions is not None
        if condition is None:
            print(f'Please specify a condition')
            exit(1)

        # tries to delete row(s) based on condition
        try:
            self.c.execute(f"""DELETE FROM {table_name} WHERE {condition}""")
            print(f'Row(s) successfully deleted where {condition}')
        except:
            raise ValueError('Specified condition is invalid. Try again.')

        # saves changes
        self.conn.commit()

    def update_rows(self, table_name=None, set_values=None, condition=None):
        """Updates row(s) in specified table based on condition.
        :param table_name: specifies the table to update data from 
        :param set_values: specifies the column(s) and new value(s) to be inserted
        :param condition: specifies the condition that rows to be updated must meet
        :type table_name: string
        :type set_values: string
        As strings in SQL must be enclosed in single quotes ('), please enclose set_values in double qutoes (").
        :type condition: string
        As strings in SQL must be enclosed in single quotes ('), please enclose condition in double qutoes (").
        :return:
        """
        # checks validation of arguments
        self.does_table_exist(table_name)
        if set_values is None or condition is None:
            print(f'Please specify set values and condition')
            exit(1)
        if not isinstance(set_values, str) or not isinstance(condition, str):
            print(f'Set values and condition must be specified as strings')
            exit(1)
        
        # updates rows
        try:
            self.c.execute(f"""UPDATE {table_name} SET {set_values} WHERE {condition}""")
            print(f'Table {table_name} successfully updated with {set_values} where {condition}')
        except:
            raise ValueError(f'Specified set values or condition are invalid. Please try again.')

        # saves changes
        self.conn.commit()

    def column_names_of_table(self, table_name=None):
        """Returns column_names from specified table.
        :param table_name: specifies the table to show column_names from
        :type table_name: string
        :return: list of column names
        """
        # checks whether specified table exists
        self.does_table_exist(table_name)

        # fetches and returns column_names
        cursor = self.c.execute(f"""SELECT * FROM {table_name}""")
        column_names = list(map(lambda x: x[0], cursor.description))
        return column_names
        
    def fetch_data(self, table_name=None, column_names=None, condition=None):
        """Selects data from specified table and columns based on condition.
        :param table_name: specifies the table to fetch data from
        :param column_names: specifies the columns to select data from
        :param condition: specifies the condition based on which data is selected
        :type table_name: string
        :type column_names: list of strings
        :type condition: string
        :return: list of data rows matching condition
        """
        # checks whether specified table exists
        self.does_table_exist(table_name)

        # checks whether columns exist if column_names is not None
        if column_names is not None:
            if not isinstance(column_names, list):
                print(f'Column names must be specified as list of strings')
                exit(1)
            for column_name in column_names:
                if column_name not in self.column_names_of_table(table_name):
                    print(f'{column_name} is an invalid column name for {table_name}')
                    exit(1)

        # checks whether condition has valid format if not None
        if condition is not None and not isinstance(condition, str):
            print(f'Condition must be specified as string')
            exit(1)

        # four possible combinations of column_names and condition being None or not None
        if column_names is None and condition is None:
            data = self.c.execute(f"""SELECT * FROM {table_name}""").fetchall()
            return data
        elif column_names is None and condition is not None:
            try:
                data = self.c.execute(f"""SELECT * FROM {table_name} WHERE {condition}""").fetchall()
                return data
            except:
                print(f'Invalid condition. Please try again.')
                exit(1)
        else:
            column_names_sql = ''
            for i, column_name in enumerate(column_names):
                if i != len(column_names) - 1:
                    column_names_sql = column_names_sql + column_name + ', '
                else:
                    column_names_sql = column_names_sql + column_name
            if column_names is not None and condition is None:
                data = self.c.execute(f"""SELECT {column_names_sql} FROM {table_name}""").fetchall()
                return data
            elif column_names is not None and condition is not None:
                data = self.c.execute(f"""SELECT {column_names_sql} FROM {table_name} WHERE {condition}""").fetchall()
                return data
            else:
                print(f'No data fetched')
                exit(1)


if __name__ == "__main__":
    pass



