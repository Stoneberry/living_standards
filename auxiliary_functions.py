import folium
from folium.plugins import MarkerCluster
from operator import itemgetter


START_COORDS = (56.6175962, 33.5179093)
START_ZOOM = 5


def set_color_by_freq(freq):
    if freq < 10:
        return 'green'
    elif freq < 100:
        return 'orange'
    return 'red'


def prepare_options(results):
    line = '<option value="{}">{}</option>'
    options = [line.format(*tuple(result)*2) for result in results]
    return options


def generate_place_popup(place, id_place):
    popup = """
    <table cellspacing="2" border="1" cellpadding="5" width="200" style="text-align:center;margin-bottom:10px;">
      <tr><td>Название</td><td>{}</td></tr>
      <tr><td>Регион</td><td>{}</td></tr>
      <tr><td>Город</td><td>{}</td></tr>
      <tr><td>Тип</td><td>{}</td></tr>
      <tr><td>Кол-во предметов</td><td>{}</td></tr>
    </table>
    <a href="{}" class="places" id="place_{}" target="_blank">Смотреть предметы</a>
    """
    values = itemgetter('pname', 'region', 'city', "ptype", 'freq')(place)
    link = "/places/{}".format(id_place)
    popup = popup.format(*values, link, id_place)
    return popup


def create_map(places, filename="map"):
    folium_map = folium.Map(location=START_COORDS, zoom_start=START_ZOOM)
    marker_cluster = MarkerCluster().add_to(folium_map)
    for id_place in places:
        place = places[id_place]
        coords = itemgetter('coord_lat', 'coord_lon')(place)
        html = generate_place_popup(place, id_place)
        folium.CircleMarker(
            location=coords, radius=9, tooltip=place['pname'],
            popup=html, color="gray",
            fill_color=set_color_by_freq(place['freq']),
            fill_opacity=0.9).add_to(marker_cluster)
    folium_map.save('templates/{}.html'.format(filename))


def create_simple_map(coords, pname, filename="map"):
    folium_map = folium.Map(location=START_COORDS, zoom_start=START_ZOOM)
    folium.Marker(coords, popup=pname, tooltip=pname).add_to(folium_map)
    folium_map.save('templates/{}.html'.format(filename))