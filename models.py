# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey

db = SQLAlchemy()


# class Categories(db.Model):
#     __tablename__ = 'categories'
#     id_category = db.Column(db.Integer, primary_key=True)
#     category = db.Column(db.Text)
#     description = db.Column(db.Text)


class Item_types(db.Model):
    __tablename__ = 'item_types'
    id_itype = db.Column(db.Integer, primary_key=True)
    itype = db.Column(db.Text)
    description = db.Column(db.Text)


# class Source_types(db.Model):
#     __tablename__ = 'source_types'
#     id_stype = db.Column(db.Integer, primary_key=True)
#     stype = db.Column(db.Text)
#     description = db.Column(db.Text)


class Places(db.Model):
    __tablename__ = 'places'

    id_place = db.Column(db.Integer, primary_key=True)
    pname = db.Column(db.Text)
    other_name = db.Column(db.Text)
    ptype = db.Column(db.Text)
    # amenity = db.Column(db.Text)
    # building = db.Column(db.Text)
    region = db.Column(db.Text)
    city = db.Column(db.Text)
    coord_lat = db.Column(db.Float)
    coord_lon = db.Column(db.Float)
    description = db.Column(db.Text)
    area_image = db.Column(db.Text)


class Items(db.Model):
    __tablename__ = 'items'

    id_item = db.Column(db.Integer, primary_key=True)
    iname = db.Column(db.Text)
    description = db.Column(db.Text)

    # id_category = db.Column(db.Integer, ForeignKey("categories.id_category"))
    id_itype = db.Column(db.Integer, ForeignKey("item_types.id_itype"))

    # relationships
    # categories = db.relationship("Categories", uselist=False, primaryjoin="Categories.id_category==Items.id_category")
    item_types = db.relationship("Item_types", uselist=False, primaryjoin="Item_types.id_itype==Items.id_itype")


class Sources(db.Model):
    __tablename__ = 'sources'

    id_source = db.Column(db.Integer, primary_key=True)
    sname = db.Column(db.Text)
    description = db.Column(db.Text)
    year = db.Column(db.Text)

    # id_stype = db.Column(db.Integer, ForeignKey("source_types.id_stype"))

    # relationships
    # source_types = db.relationship("Source_types", uselist=False, primaryjoin="Source_types.id_stype==Sources.id_stype")


class Measures(db.Model):
    __tablename__ = 'measures'
    id_measure = db.Column(db.Integer, primary_key=True)
    mnane_old = db.Column(db.Text)
    mnane_hist = db.Column(db.Text)


class Prices(db.Model):
    __tablename__ = 'c_price'

    id_cprice = db.Column(db.Integer, primary_key=True)

    price_cur = db.Column(db.Integer)
    price_old = db.Column(db.Integer)
    scope = db.Column(db.Float)
    year = db.Column(db.Integer)
    month = db.Column(db.Integer)
    page = db.Column(db.Text)
    # measure_cur = db.Column(db.Text)
    # measure_old = db.Column(db.Text)
    # nominal = db.Column(db.Text)
    description = db.Column(db.Text)

    id_item = db.Column(db.Integer, ForeignKey("items.id_item"))
    id_place = db.Column(db.Integer, ForeignKey("places.id_place"))
    id_source = db.Column(db.Integer, ForeignKey("sources.id_source"))
    id_measure = db.Column(db.Integer, ForeignKey("measures.id_measure"))

    # relationships
    items = db.relationship("Items", uselist=False, primaryjoin="Items.id_item==Prices.id_item")
    sources = db.relationship("Sources", uselist=False, primaryjoin="Sources.id_source==Prices.id_source")
    places = db.relationship("Places", uselist=False, primaryjoin="Places.id_place==Prices.id_place")
    measures = db.relationship("Measures", uselist=False, primaryjoin="Measures.id_measure==Prices.id_measure")

