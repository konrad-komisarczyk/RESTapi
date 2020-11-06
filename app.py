from flask import (Flask, render_template, request, jsonify)
import json

app = Flask(__name__)


# Adding/deleting/editing(moving) points on the map
# Adding/editing data related to the points (like in your original forms)
# Storing data about the pickup and delivery orders on the server (you may use just an in-memory storage for demo purposes)
# Presenting overall data from the server on the map
# Presenting detailed information of the order selected on the map
# Matching addresses to locations and vice versa with geocoding and reverse geocoding services

@app.route('/form')
def form():
    return render_template("form.html")


@app.route('/index')
def index():
    try:
        with open('db.json', 'r') as f:
            entries = json.loads(f.read())
            return render_template("index.html", orders=entries)
    except:
        return "error"


@app.route('/<id>', methods=['DELETE', 'PUT', 'GET'])
def menu(id):
    try:
        if request.method == 'DELETE':
            with open('db.json', 'r') as f:
                entries = json.loads(f.read())
                if id and (id in entries.keys()):
                    with open('db.json', 'w') as f2:
                        response = entries[id]
                        entries.pop(id)
                        json.dump(entries, f2)
                    return response
                else:
                    return "error"

        if request.method == 'PUT':
            with open('db.json', 'r') as f:
                entries = json.loads(f.read())
                if id and (id in entries.keys()):
                    with open('db.json', 'w') as f2:
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
            with open('db.json', 'r') as f:
                entries = json.loads(f.read())
                if id in entries.keys():
                    return entries[id]
                else:
                    return "error"
    except:
        return "error"


@app.route('/', methods=['POST', 'GET'])
def user():
    try:
        if request.method == 'POST':
            with open('db.json', 'r') as f:
                entries = json.loads(f.read())
                with open('db.json', 'w') as f2:
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
            with open('db.json', 'r') as f:
                entries = json.loads(f.read())
                return entries

    except:
        return "error"


if __name__ == '__main__':
    app.run()
