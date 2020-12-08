import sqlite3
import pandas as pd
import numpy as np
import csv


class Database:
    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.cur = self.conn.cursor()
        self.read_database()
        self.station_names = self.get_station_names_list()

    def if_table_exist(self):
        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='bike';")
        result = self.cur.fetchall()
        if len(result) > 0:
            return True
        return False

    def read_database(self):
        if not self.if_table_exist():
            # load the csv file into a sql table
            titles = ["StartStationName", "EndStationName", "UserType", "TripDurationinmin"]
            data_frame = pd.read_csv("BikeShare.csv", usecols=titles)
            data_as_array = data_frame.to_numpy()
            self.cur.execute(f"CREATE TABLE if not exists bike {tuple(titles)};")
            self.cur.executemany("INSERT INTO bike VALUES (?,?,?,?)", data_as_array)
            self.conn.commit()

    # put each station name from database on list
    def get_station_names_list(self):
        self.cur.execute(f"SELECT DISTINCT StartStationName FROM bike")
        result = self.cur.fetchall()
        return result

    # select the wanted end station by SQL query
    def select_end_stations(self, duration, start_location, num_of_result):

        # determine the range of the duration using alpha and beta
        alpha = duration * 0.75 # upper bound
        beta = duration * 1.25 # lower bound
        # fix the range if it is too small
        if beta < duration + 5:
            beta = duration + 5
            alpha = duration - 5

        # SQL query
        self.cur.execute(f"SELECT SUM(CASE WHEN UserType='Subscriber' THEN 5 ELSE 1 END) AS Co, "
                         f"EndStationName, AVG(TripDurationinmin) AS Av "
                         f"FROM bike "
                         f"WHERE StartStationName = '{start_location}' "
                         f"GROUP BY EndStationName "
                         f"HAVING Av BETWEEN {alpha} AND {beta} "
                         f"ORDER BY Co DESC "
                         f"LIMIT {num_of_result}")

        result = self.cur.fetchall()
        # self.print_result(result)
        return result

    # check if input location is valid
    def valid_start_location(self, start_location_input_text):
        # use station_name list for check valid location
        for location in self.station_names:
            if location[0] == start_location_input_text:
                return True
        return False

    def print_result(self, result):
        for row in result:
            print(row)

# my_backend = Database()
# # res = my_backend.select_end_stations(30, "Lincoln Park", 5)
# # # my_backend.print_result(res)
# # names = ""
# # for row in res:
# #     names = names + "\n" + row[1]
# # print(names)

# my_backend.valid_start_location("Essex Light Rail")
