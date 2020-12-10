import json

from flask import Flask, redirect, url_for, request
from mybackend import Database


app = Flask(__name__)
my_database = Database()


@app.route('/', methods=['GET'])
def search_locations():
    # get values from the request
    req = request.values
    try:
        # casting values
        duration = float(req["timeduration"])
        start_location = req["startlocation"]
        num_of_result = int(req["k"])
    except ValueError:
        # return an empty JSON for incorrect input
        return {}
    result = my_database.select_end_stations(duration, start_location, num_of_result)
    stations_names = []
    # put only stations names on list
    for row in result:
        stations_names.append(row[1])
    return json.dumps(stations_names)


if __name__ == '__main__':
    app.run(debug = True)
