# -*- coding: utf-8 -*-
from flask import Flask, render_template, jsonify, request

from models import db
from search_db import Search
from auxiliary_functions import *


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///living_standards.db'
db.app = app
db.init_app(app)
db.create_all()

search = Search()

ICON_COLORS = ["green", "red", "blue"]
START_COORDS = (56.6175962, 33.5179093)
START_ZOOM = 5

@app.route('/')
def index():
    places = search.get_all_places()
    create_map(places, filename="map")
    item_types = search.get_item_types()
    regions = search.get_regions()
    return render_template("index.html", item_types=item_types, regions=regions)


@app.route("/places/<int:id_place>")
def formula_view(id_place):
    data = search.search_items_by_place(id_place)
    values = search.get_place_map(id_place)
    create_simple_map(values[3:], values[2], filename="map_place")
    return render_template(
        "place.html", data=data,
        area_map=values[0], area_image=values[1],
        area_title=values[2])


@app.route("/api/places", methods=["GET", "POST"])
def api_search():
    places = search.search_places(request)
    create_map(places, filename="map_search")
    return jsonify(places)


@app.route('/map')
def map():
    return render_template('map.html')


@app.route('/map_search')
def map_search():
    return render_template('map_search.html')


@app.route('/map_place')
def map_place():
    return render_template('map_place.html')


if __name__ == '__main__':
    app.run(debug=True)