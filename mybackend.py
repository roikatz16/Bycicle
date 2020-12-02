import sqlite3
import csv

conn = sqlite3.connect('database.db')
cur = conn.cursor()

with open("BikeShare.csv") as a_file:
    reader = csv.reader(a_file)
    titles = tuple(next(reader))
    num_of_columns = len(titles)
    question_marks = "(" + "?, "*(num_of_columns-1) + "?)"
    cur.execute(f"CREATE TABLE if not exists bike {titles};")
    cur.executemany(f"INSERT INTO bike VALUES {question_marks}", reader)
    # cur.execute("SELECT * FROM data")
    # print(cur.fetchall())


def execute_query(query):
    cur.execute(query)
    result = cur.fetchall()
    return result


def select_top_duration(n):
    return execute_query(f"Select TripDuration from bike DESC LIMIT {n}")


ans = select_top_duration(3)
print(ans)
