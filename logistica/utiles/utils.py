
from math import radians, sin, cos, sqrt, atan2
from datos.ciudades import CIUDADES   # importar diccionario de ciudades
from datos.ciudades_alicante import CIUDADES_ALICANTE



def distancia_km(coord1, coord2):

    lat1, lon1 = coord1
    lat2, lon2 = coord2

    R = 6371  # radio de la Tierra en km

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c