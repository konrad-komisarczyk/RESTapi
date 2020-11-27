import copy

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
    a = math.sin(delta_fi / 2)**2 + math.cos(fi1) * math.cos(fi2) * math.sin(delta_sigma / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return r * c


class Package:
    def __init__(self, lat, lon, weight, id):
        self.lat = lat
        self.lon = lon
        self.weight = weight
        self.id = id
        self.loaded = False

    def markLoaded(self):
        self.loaded = True

    def __str__(self):
        return "lat: " + self.lat + ", lon: " + self.lon + ", weight: " + self.weight + ", id: " + self.id \
               + ", loaded: " + self.loaded


storehouse_lat = 52.217993
storehouse_lon = 20.961914

class SetOfPackages:
    def __init__(self):
        self.packages = []

    def totalWeight(self):
        total = 0
        for package in self.packages:
            total += package.weight
        return total

    def routeLength(self):
        total = 0
        if len(self.packages) == 0:
            return 0
        total += distance(storehouse_lat, storehouse_lon, self.packages[0].lat, self.packages[0].lon)
        total += distance(storehouse_lat, storehouse_lon, self.packages[-1].lat, self.packages[-1].lon)
        for i in range(0, len(self.packages) - 1):
            total += distance(self.packages[i].lat, self.packages[i].lon,
                              self.packages[i + 1].lat, self.packages[i + 1].lon)
        return total


    def optimizeOrder(self):
        permuts = list(itertools.permutations(self.packages))
        optimalForNow = 0
        optimalDistance = self.routeLength()
        for i in range(1, len(permuts)):
            self.packages = permuts[i]
            dist = self.routeLength()
            if dist < optimalDistance:
                optimalDistance = dist
                optimalForNow = int(i)
        print("permuts :")
        print(type(permuts[optimalForNow]))
        self.packages = list(permuts[optimalForNow])


    def addPackage(self, package):
        print("addPackage1")
        print(package.lat)
        print(len(self.packages))
        print(type(self.packages))
        print(self.packages)
        self.packages.append(package)
        #self.packages[len(self.packages)] = package
        print("addPackage2")
        self.optimizeOrder()
        print("addPackage3")


class Vehicle:
    def __init__(self, capacity, maxRoute, id):
        self.capacity = capacity
        self.maxRoute = maxRoute
        self.id = id
        self.setOfPackages = SetOfPackages()

    def possibleToLoad(self, package):
        print("poss1")
        newSetOfPackages = copy.deepcopy(self.setOfPackages)
        print("poss2")
        newSetOfPackages.addPackage(package)
        print("poss3")
        return newSetOfPackages.totalWeight() < self.capacity and newSetOfPackages.routeLength() < self.maxRoute

    def load(self, package):
        if self.possibleToLoad(package):
            self.setOfPackages.addPackage(package)
        else:
            raise Exception("Not possible to load!")

    def getRoute(self):
        route = []
        if len(self.setOfPackages.packages) == 0:
            return route
        route.append({"lat": storehouse_lat, "lon": storehouse_lon})
        for package in self.setOfPackages.packages:
            route.append({"lat": package.lat, "lon": package.lon})
        route.append({"lat": storehouse_lat, "lon": storehouse_lon})
        return route



def assignRoutes(packages, vehicles):
    print("asingRoutes")
    for package in packages:
        print("package" + package.id)
        for vehicle in vehicles:
            print("veh" + vehicle.id)
            print(package.loaded)
            print(vehicle.possibleToLoad(package))
            if not package.loaded and vehicle.possibleToLoad(package):
                print("loading")
                package.markLoaded()
                vehicle.load(package)
    print("asign2")


def parseLatLonString(latlon):
    lat = float(latlon.split("(")[-1].split(")")[0].split(",")[0])
    lon = float(latlon.split("(")[-1].split(")")[0].split(",")[1])
    return lat, lon


def dailyDeparture():
    try:
        with open('packages.json', 'r') as packages_database:
            with open('vehicles.json', 'r') as vehicles_database:
                packages_db = json.loads(packages_database.read())
                vehicles_db = json.loads(vehicles_database.read())
                packages_to_depart = []
                available_vehicles = []
                for id in packages_db.keys():
                    status = packages_db[id]["status"]
                    weight = float(packages_db[id]["weight"])
                    if status == "sent":
                        latlon = packages_db[id]["pickup-map"]
                        lat, lon = parseLatLonString(latlon)
                        packages_to_depart.append(Package(lat, lon, weight, id))
                    elif status == "in_storehouse":
                        latlon = packages_db[id]["delivery-map"]
                        lat, lon = parseLatLonString(latlon)
                        packages_to_depart.append(Package(lat, lon, weight, id))

                for id in vehicles_db.keys():
                    capacity = float(vehicles_db[id]["capacity"])
                    available_vehicles.append(Vehicle(capacity, 200000, id))

                assignRoutes(packages_to_depart, available_vehicles)

                for package in packages_to_depart:
                    if package.loaded:
                        status_current = packages_db[package.id]["status"]
                        if status_current == "sent":
                            packages_db[package.id]["status"] = "in_storehouse"
                        elif status_current == "in_storehouse":
                            packages_db[package.id]["status"] = "delivered"

                for vehicle in available_vehicles:
                    vehicles_db[vehicle.id]["route"] = vehicle.getRoute()
                    vehicles_db[vehicle.id]["weight"] = vehicle.setOfPackages.totalWeight()
                    vehicles_db[vehicle.id]["route-length"] = round(vehicle.setOfPackages.routeLength() / 1000, 1)

        with open('packages.json', 'w') as packages_database_w:
            json.dump(packages_db, packages_database_w)

        with open('vehicles.json', 'w') as vehicles_database_w:
            json.dump(vehicles_db, vehicles_database_w)

        return packages_db

    except:
        return "error"

@app.route('/departure/', methods=['GET'])
def departure_endpoint():
    if request.method == 'GET':
        return dailyDeparture()


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
            with open('vehicles.json', 'r') as f2:
                orders = json.loads(f.read())
                vehicles = json.loads(f2.read())
                return render_template("index.html", orders=orders, vehicles=vehicles)
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


@app.route('/package_info/<id>', methods=['GET'])
def package_info(id):
    try:
        if request.method == 'GET':
            with open('packages.json', 'r') as f:
                entries = json.loads(f.read())
                if id in entries.keys():
                    return render_template("package_info.html", package=entries[id])
                else:
                    return "error"
    except:
        return "error loading database"

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
                    entry_data = request.form.copy()
                    entry_data["status"] = "sent"
                    new_entry = {
                        new_id: entry_data
                    }
                    entries.update(new_entry)
                    json.dump(entries, f2)
            return entry_data

        if request.method == 'GET':
            with open('packages.json', 'r') as f:
                entries = json.loads(f.read())
                return entries

    except:
        return "error"

@app.route('/vehicle_route_preview/<id>', methods=['GET'])
def vehicle_route_preview(id):
    try:
        with open('vehicles.json', 'r') as vehicles_database:
            vehicles = json.loads(vehicles_database.read())
            return render_template("vehicle_route_preview.html", vehicle=vehicles[id])

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
                    vehicle_data = request.form.copy()
                    vehicle_data["route"] = []
                    vehicle_data["route-length"] = 0
                    vehicle_data["weight"] = 0
                    new_entry = {
                        new_id: vehicle_data
                    }
                    entries.update(new_entry)
                    json.dump(entries, f2)
            return vehicle_data

        if request.method == 'GET':
            with open('vehicles.json', 'r') as f:
                entries = json.loads(f.read())
                return entries

    except:
        return "error"


if __name__ == '__main__':
    app.run()
