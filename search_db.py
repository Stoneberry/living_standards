# -*- coding: utf-8 -*-
from models import Item_types as IT, Items, Prices, Places
from sqlalchemy import func
from auxiliary_functions import prepare_options

DEFAULT_CAT = "предмет роскоши"
DEFAULT_ITYPE = "предмет"


class Search:

    @staticmethod
    def item_result_to_dict(result):
        result = [
            {
                "id": item.items.id_item,
                "name": item.items.iname,
                "itype": item.items.item_types.itype,
                "price_cur": item.price_cur,
                "scope": item.price_cur,
                "mname_hist": item.measures.mnane_hist,
                "mname_old": item.measures.mnane_old,
                "place": {
                    "id_place": item.places.id_place,
                    "name": item.places.pname,
                    "region": item.places.region,
                    "ptype": item.places.ptype,
                    "city": item.places.city,
                    "coord": {
                        "lat": item.places.coord_lat,
                        "lon": item.places.coord_lon,
                    }
                },
                "source": {
                    "name": item.sources.sname,
                    "page": item.page,
                    "year": item.year,
                    "month":  item.month,
                },
             }
            for item in result
        ]
        return result

    @staticmethod
    def gather_place_descr(item):
        place_descr = {
            "name": item.places.pname,
            "ptype": item.places.ptype,
            "city": item.places.city,
            "region": item.places.region,
            "coord": {
                "lat": item.places.coord_lat,
                "lon": item.places.coord_lon,
            }
         }
        return place_descr

    @staticmethod
    def gather_source_descr(item):
        source_descr = {
            "name": item.sources.sname,
            "page": item.page,
            "year": item.year,
            "month": item.month,
         }
        return source_descr

    @staticmethod
    def places_result_to_dict(results):
        places = {}
        for item in results:
            keys = list(item.keys())[1:] + ["freq"]
            places[item[0]] = dict(zip(keys, item[1:]))
        return places

    def get_all_prices(self):
        result = Prices.query.all()
        return self.item_result_to_dict(result)

    def get_all_places(self):
        result = Prices.query.join(Places, Prices.id_place==Places.id_place)\
            .with_entities(
            Prices.id_place, Places.pname,
            Places.ptype, Places.city,
            Places.coord_lat, Places.coord_lon,
            Places.region, func.count())\
            .group_by(Prices.id_place).all()
        return self.places_result_to_dict(result)

    def search_items_by_place(self, id_place):
        result = Prices.query.filter(
            Prices.id_place == id_place
        ).all()
        return self.item_result_to_dict(result)

    @staticmethod
    def get_item_types():
        result = IT.query.\
            with_entities(IT.itype).\
            distinct(IT.itype).all()
        return prepare_options(result)

    @staticmethod
    def get_regions():
        result = Places.query.\
            with_entities(Places.region).\
            distinct(Places.region).all()
        return prepare_options(result)

    @staticmethod
    def prepare_regions_types(regs, itypes):
        result = Prices.query \
            .join(Places, Prices.id_place == Places.id_place) \
            .join(Items, Prices.id_item == Items.id_item) \
            .join(IT, Items.id_itype == IT.id_itype) \
            .filter(Places.region.in_(regs)) \
            .filter(IT.itype.in_(itypes)) \
            .with_entities(
                Prices.id_place, Places.pname,
                Places.ptype, Places.city,
                Places.coord_lat, Places.coord_lon,
                Places.region, func.count()) \
            .group_by(Prices.id_place).all()
        return result

    @staticmethod
    def prepare_regions(regs):
        result = Prices.query \
            .join(Places, Prices.id_place == Places.id_place) \
            .filter(Places.region.in_(regs)) \
            .with_entities(
                Prices.id_place, Places.pname,
                Places.ptype, Places.city,
                Places.coord_lat, Places.coord_lon,
                Places.region, func.count()) \
            .group_by(Prices.id_place).all()
        return result

    @staticmethod
    def prepare_types(itypes):
        result = Prices.query \
            .join(Places, Prices.id_place == Places.id_place) \
            .join(Items, Prices.id_item == Items.id_item) \
            .join(IT, Items.id_itype == IT.id_itype) \
            .filter(IT.itype.in_(itypes)) \
            .with_entities(
                Prices.id_place, Places.pname,
                Places.ptype, Places.city,
                Places.coord_lat, Places.coord_lon,
                Places.region, func.count()) \
            .group_by(Prices.id_place).all()
        return result

    def search_places(self, request):
        form_values = request.args.to_dict(flat=False)
        if form_values:
            regs = form_values.get('region')
            itypes = form_values.get('item_type')
            if regs and itypes:
                result = self.prepare_regions_types(regs, itypes)
            elif regs:
                result = self.prepare_regions(regs)
            elif itypes:
                result = self.prepare_types(itypes)
            return self.places_result_to_dict(result)
        return self.get_all_places()

    @staticmethod
    def get_place_map(id_place):
        result = Places.query.filter(
            Places.id_place == id_place
        ).with_entities(
            Places.description, Places.area_image,
            Places.pname, Places.coord_lat, Places.coord_lon
        ).first()

        iframe = '''
            <iframe 
                class ="embed-responsive-item" src="{}" 
                name="etomesto-map" width="100%" 
                height="90%" frameborder="0" 
                vspace="0" hspace="0" 
                marginwidth="0"  marginheight="0" 
                scrolling="no">
            </iframe>'''.format(result[0])

        area_image, pname, coord_lat, coord_lon = result[1:]
        return iframe, area_image, pname, coord_lat, coord_lon
