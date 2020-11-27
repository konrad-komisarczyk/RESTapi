from flask import (Flask, render_template, request, jsonify)
import json
import math
import itertools

app = Flask(__name__)



# Adding/deleting/editing(moving) points on the map
# Adding/editing data related to the points (like in your original forms)
# Storing data about the pickup and delivery orders on the server (you may use just an in-memory storage for demo purposes)
# Presenting overall data from the server on the map
# Presenting detailed information of the order selected on the map
# Matching addresses to locations and vice versa with geocoding and reverse geocoding services

def distance(lat1, lon1, lat2, lon2):
    r = 6371000
    fi1 = lat1 * math.pi / 180
    fi2 = lat2 * math.pi / 180
    delta_fi = (lat2 - lat1) * math.pi / 180
    delta_sigma = (lon1 - lon2) * math.pi / 180
    a = math.sin(delta_fi / 2) ** 2 + math.cos(fi1) * math.cos(fi2) * math.sin(delta_sigma / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return r * c

class setOfPackages:
    storehouse_lat = 52.217993
    storehouse_lon = 20.961914

    def __init__(self):
        self.lat = []
        self.lon = []
        self.weight = []

    def totalWeight(self):
        return sum(self.weight)

    def routeLength(self):
        total = 0
        if len(self.lat) == 0:
            return 0
        total += distance(self.storehouse_lat, self.storehouse_lon, self.lat[0], self.lon[0])
        total += distance(self.storehouse_lat, self.storehouse_lon, self.lat[-1], self.lon[-1])
        for i in range(0, len(self.lat) - 1):
            total += distance(self.lat[i], self.lon[i], self.lat[i + 1], self.lon[i + 1])
        return total

    def optimizeOrder(self):
        lat_permuts = list(itertools.permutations(self.lat))
        lon_permuts = list(itertools.permutations(self.lon))
        weight_permuts = list(itertools.permutations(self.weight))

        optimalForNow = 0
        optimalDistance = self.routeLength()
        for i in range(1, len(lat_permuts)):
            self.lat = lat_permuts[i]
            self.lon = lon_permuts[i]
            dist = self.routeLength()
            if dist < optimalDistance:
                optimalDistance = dist
                optimalForNow = i

        self.lat = lat_permuts[optimalForNow]
        self.lon = lon_permuts[optimalForNow]
        self.weight = weight_permuts[optimalForNow]

    def addPackage(self, lat, lon):
        self.lat.append(lat)
        self.lon.append(lon)
        self.optimizeOrder()


def dividePackages(packages, vehicles):
    for vehicle_id in vehicles.keys():
        while

@app.route('/form')
def form():
    return render_template("form.html")

@app.route('/form_vehicles')
def form_vehicles():
    return render_template("form_vehicles.html")


@app.route('/')
def index():
    try:
        with open('packages.json', 'r') as f:
            entries = json.loads(f.read())
            return render_template("index.html", orders=entries)
    except:
        return "error"


@app.route('/packages/<id>', methods=['DELETE', 'PUT', 'GET'])
def menu(id):
    try:
        if request.method == 'DELETE':
            with open('packages.json', 'r') as f:
                entries = json.loads(f.read())
                if id and (id in entries.keys()):
                    with open('packages.json', 'w') as f2:
                        response = entries[id]
                        entries.pop(id)
                        json.dump(entries, f2)
                    return response
                else:
                    return "error"

        if request.method == 'PUT':
            with open('packages.json', 'r') as f:
                entries = json.loads(f.read())
                if id and (id in entries.keys()):
                    with open('packages.json', 'w') as f2:
                        new_entry = {
                            id: request.form
                        }
                        entries.pop(id)
                        entries.update(new_entry)
                        json.dump(entries, f2)
                    return new_entry
                else:
                    return "error"

        if request.method == 'GET':
            with open('packages.json', 'r') as f:
                entries = json.loads(f.read())
                if id in entries.keys():
                    return entries[id]
                else:
                    return "error"
    except:
        return "error"


@app.route('/packages/', methods=['POST', 'GET'])
def user():
    try:
        if request.method == 'POST':
            with open('packages.json', 'r') as f:
                entries = json.loads(f.read())
                with open('packages.json', 'w') as f2:
                    if len(entries) == 0:
                        new_id = 1
                    else:
                        new_id = max([int(s) for s in entries.keys()]) + 1
                    new_entry = {
                        new_id: request.form
                    }
                    entries.update(new_entry)
                    json.dump(entries, f2)
            return request.form

        if request.method == 'GET':
            with open('packages.json', 'r') as f:
                entries = json.loads(f.read())
                return entries

    except:
        return "error"



@app.route('/vehicles/<id>', methods=['DELETE', 'PUT', 'GET'])
def menu_vehicles(id):
    try:
        if request.method == 'DELETE':
            with open('vehicles.json', 'r') as f:
                entries = json.loads(f.read())
                if id and (id in entries.keys()):
                    with open('vehicles.json', 'w') as f2:
                        response = entries[id]
                        entries.pop(id)
                        json.dump(entries, f2)
                    return response
                else:
                    return "error"

        if request.method == 'PUT':
            with open('vehicles.json', 'r') as f:
                entries = json.loads(f.read())
                if id and (id in entries.keys()):
                    with open('vehicles.json', 'w') as f2:
                        new_entry = {
                            id: request.form
                        }
                        entries.pop(id)
                        entries.update(new_entry)
                        json.dump(entries, f2)
                    return new_entry
                else:
                    return "error"

        if request.method == 'GET':
            with open('vehicles.json', 'r') as f:
                entries = json.loads(f.read())
                if id in entries.keys():
                    return entries[id]
                else:
                    return "error"
    except:
        return "error"


@app.route('/vehicles/', methods=['POST', 'GET'])
def user_vehicles():
    try:
        if request.method == 'POST':
            with open('vehicles.json', 'r') as f:
                entries = json.loads(f.read())
                with open('vehicles.json', 'w') as f2:
                    if len(entries) == 0:
                        new_id = 1
                    else:
                        new_id = max([int(s) for s in entries.keys()]) + 1
                    new_entry = {
                        new_id: request.form
                    }
                    entries.update(new_entry)
                    json.dump(entries, f2)
            return request.form

        if request.method == 'GET':
            with open('vehicles.json', 'r') as f:
                entries = json.loads(f.read())
                return entries

    except:
        return "error"


if __name__ == '__main__':
    app.run()
