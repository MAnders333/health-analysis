from typing import Type
from database import Database
import matplotlib.pyplot as plt 
import numpy as np


def show_complete_db(database_class: Type[Database]) -> None:
    for table in database_class.table_names:
        print(f'Table {table}')
        data = database_class.fetch_data(table_name=table)
        data = np.array(data)
        x_values = np.array([])
        y_values = np.array([])
        for row in data:
            np.append(x_values, row[0])
            np.append(y_values, row[1])
        plt.plot(x_values, y_values)
        plt.show()




# def show_complete_db(database_class: Type[Database]) -> None:
#     seperator = '-'*100
#     for table in database_class.table_names:
#         print(seperator)
#         print(f'Table {table}')
#         print(seperator)
#         data = database_class.fetch_data(table_name=table)
#         for row in data:
#             print(row)
