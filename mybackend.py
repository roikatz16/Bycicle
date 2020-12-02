import sqlite3
import pandas as pd
import csv


class Database:
    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.cur = self.conn.cursor()
        self.read_database()

    def read_database(self):
        # reader = csv.reader(a_file)
        titles = ['StartStationName', 'EndStationName', 'UserType', 'TripDurationinmin']
        dataset = pd.read_csv("BikeShare.csv", names=titles)
        print(dataset.head(), dataset.shape)
        self.cur.execute(f"CREATE TABLE if not exists bike {tuple(titles)};")
        self.cur.executemany(f"INSERT INTO bike VALUES (?,?,?,?)", dataset)
        print("test")

    def execute_query(self, query):
        self.cur.execute(query)
        result = self.cur.fetchall()
        return result

    def select_top_duration(self, n):
        return self.execute_query(f"Select TripDuration from bike DESC LIMIT {n}")


my_backend = Database()
# ans = my_backend.select_top_duration(3)
print("Roi")
