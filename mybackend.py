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
        # reader = csv.reader(a_file)
        titles = ["StartStationName", "EndStationName", "UserType", "TripDurationinmin"]
        data_frame = pd.read_csv("BikeShare.csv", usecols=titles)
        data_as_array = data_frame.to_numpy()
        self.cur.execute(f"CREATE TABLE if not exists bike {tuple(titles)};")
        self.cur.executemany("INSERT INTO bike VALUES (?,?,?,?)", data_as_array)
        self.conn.commit()

    def execute_query(self, query):
        self.cur.execute(query)
        result = self.cur.fetchall()
        return result

    def select(self, n):
        return self.execute_query(f"Select EndStationName from bike limit 5")


my_backend = Database()
ans = my_backend.select(3)
for row in ans:
    print(row)
