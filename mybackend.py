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

    def select_end_stations(self, duration, start_location, num_of_result):
        #

        # if the wanted duration time is
        alpha = duration * 0.75
        beta = duration * 1.25
        if beta < duration + 5:
            beta = duration + 5
            alpha = duration - 5

        self.cur.execute(f"SELECT SUM(CASE WHEN UserType='Subscriber' THEN 5 ELSE 1 END) AS Co, "
                         f"EndStationName, AVG(TripDurationinmin) AS Av "
                         f"FROM bike "
                         f"WHERE StartStationName = '{start_location}' "
                         f"GROUP BY EndStationName "
                         f"HAVING Av BETWEEN {alpha} AND {beta} "
                         f"ORDER BY Co DESC "
                         f"LIMIT {num_of_result}")

        result = self.cur.fetchall()
        self.print_result(result)

    def print_result(self, result):
        for row in result:
            print(row)


# my_backend = Database()
# my_backend.select_end_stations(30, "Lincoln Park", 5)
print(sqlite3.sqlite_version)