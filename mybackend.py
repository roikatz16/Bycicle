import sqlite3
import pandas as pd
import numpy as np
import csv


class Database:
    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.cur = self.conn.cursor()
        self.read_database()

    def read_database(self):
        # load the csv file into a sql table
        titles = ["StartStationName", "EndStationName", "UserType", "TripDurationinmin"]
        data_frame = pd.read_csv("BikeShare.csv", usecols=titles)
        data_as_array = data_frame.to_numpy()
        self.cur.execute(f"CREATE TABLE if not exists bike {tuple(titles)};")
        self.cur.executemany("INSERT INTO bike VALUES (?,?,?,?)", data_as_array)
        self.conn.commit()

    def execute_query(self, duration, start_location):
        alpha = duration*0.75
        beta = duration*1.25
        if beta < duration + 5:
            beta = duration + 5
            alpha = duration - 5

        # self.cur.execute(f"SELECT COUNT(EndStationName) AS C, EndStationName, AVG(TripDurationinmin) AS A "
        #                  f"FROM bike "
        #                  f"WHERE StartStationName = '{start_location}' "
        #                  f"GROUP BY EndStationName "
        #                  f"HAVING A BETWEEN {alpha} AND {beta} "
        #                  f"ORDER BY C DESC")

        self.cur.execute(f"SELECT COUNT(EndStationName) AS C1, EndStationName, AVG(TripDurationinmin) AS A "
                         f"FROM bike "
                         f"WHERE StartStationName = '{start_location}' "
                         f"GROUP BY EndStationName "
                         f"HAVING A BETWEEN {alpha} AND {beta} "
                         f"ORDER BY C DESC")


        result = self.cur.fetchall()
        self.print_result(result)


    def print_result(self, result):
        for row in result:
            print(row)


my_backend = Database()
my_backend.execute_query(30, "Lincoln Park")


