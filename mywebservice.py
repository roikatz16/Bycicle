import json

from flask import Flask, redirect, url_for, request
from mybackend import Database


app = Flask(__name__)


@app.route('/', methods=['GET'])
def search_locations():
    my_database = Database()
    req = request.values
    try:
        duration = float(req["timeduration"])
        start_location = req["startlocation"]
        num_of_result = int(req["k"])
    except ValueError:
        return {}
    result = my_database.select_end_stations(duration, start_location, num_of_result)
    stations_names = []
    for row in result:
        stations_names.append(row[1])
    return json.dumps(stations_names)


if __name__ == '__main__':
    app.run(debug = True)
