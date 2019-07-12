"""This module contains the Database class which is used to handle SQLite databases."""

import sqlite3
import os
import re


class Database:
    """Database object that can handle SQLite databases to create tables, add/delete/edit rows in tables, and return requested data."""    
    
    def __init__(self, path=os.getcwd(), db_name=None):
        """Initializes a Database object with a specified (path and) name. Default path is the current working directory.

        :param path: path to existing directory in which the database will be / was created
        :param db_name: file name of the database to create / that was created
        :type path: string
        :type db_name: string
        """
        
        # checks whether specified path is valid
        if os.path.exists(path):
            self.path = path
        else:
            raise AttributeError('Specified path does not exist or is invalid.')
        
        # checks whether specified name for the database is valid
        if isinstance(db_name, str) and re.match('^\w+\.db$', db_name) is not None:
            self.db_name = db_name
        else:
            raise AttributeError('Specified database name is invalid.')
        
        # connects / creates a SQLite database at specified path with specified name
        if self.path[-1] != '/':
            self.conn = sqlite3.connect(f'{self.path}/{self.db_name}')
        else:
            self.conn = sqlite3.connect(f'{self.path}{self.db_name}')

        self.c = self.conn.cursor()
        self.table_names = [name[0] for name in self.c.execute("""SELECT name from sqlite_master where type='table'""").fetchall()]
        
    def create_table(self, table_name=None, headers=None):
        """Creates new table in existing database with specified headers.

        :param table_name: name of the table to be created
        :param headers: column headers for the table to be created (format: (column_name_1 TEXT, ...))
        :type table_name: string
        :type headers: string
        """
        # checks whether table already exists
        if table_name in self.table_names:
            return
        
        # checks whether table_name and headers have the correct format
        if isinstance(table_name, str) and re.match('^\((\s*\w+\s[A-Z]+,*)+\)$', headers) is not None:
            # creates a new table with specified table name and headers
            self.c.execute(f"""CREATE TABLE {table_name} {headers}""")
            # appends table name to list of table names
            self.table_names.append(table_name)
        else:
            raise AttributeError('The specified arguments are invalid. Try again.')

    def add_row(self, table_name=None, data=None):
        """Adds data row in specified table.

        :param table_name: specifies the table to insert the data
        :param data: specifies the data to be inserted
        :type table_name: string
        :type data: tuple
        """
        # checks whether specified table name exists
        if table_name not in self.table_names:
            raise AttributeError('Specified table does not exist.')
        
        # checks whether specified data has a valid format
        cursor = self.c.execute(f"""SELECT * FROM {table_name}""")
        table_headers = [description[0] for description in cursor.description]
        if isinstance(data, tuple) and len(data) == len(table_headers):
            # inserts data row into specified table
            self.c.execute(f"""INSERT INTO {table_name} VALUES {data}""")
            print('data successfully inserted')
        
        # saves changes
        self.conn.commit()

    def delete_row(self, table_name=None, condition=None):
        pass
    # method that deletes line in existing db and table

    # method that edits line in existing db and table

    # method that allows to select data from specified database and table with SQL code

    # method that closes the connection

if "__name__" == "__main__":
    pass



