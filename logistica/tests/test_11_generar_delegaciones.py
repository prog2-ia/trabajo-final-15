import time
from geopy.geocoders import Nominatim

# =========================
# CONFIGURACION
# =========================
geolocator = Nominatim(user_agent="delegaciones_app")

cache = {}

def obtener_coordenadas(direccion):
    if direccion in cache:
        return cache[direccion]

    try:
        location = geolocator.geocode(direccion)
        if location:
            coords = (location.latitude, location.longitude)
            cache[direccion] = coords
            time.sleep(1)
            return coords
    except:
        pass

    return None


# =========================
# DIRECCIONES REALES SEUR
# =========================
delegaciones_reales = {

    # ALICANTE
    "Alicante_1": "Calle Euro 9, Alicante, España",
    "Alicante_2": "Calle Churruca 23, Alicante, España",
    "San Vicente del Raspeig_1": "Calle Cotolengo 25, San Vicente del Raspeig, España",
    "Elche_1": "Avenida Libertad 11, Elche, España",

    # MADRID
    "Madrid_1": "Calle Gamonal 6, Madrid, España",
    "Madrid_2": "Calle Resina 39, Madrid, España",
    "Getafe_1": "Calle Carpinteros 7, Getafe, España",
    "Leganés_1": "Calle del Trigo 39, Leganés, España",
    "Alcorcón_1": "Calle Industrias 14, Alcorcón, España",
    "Fuenlabrada_1": "Calle Constitución 5, Fuenlabrada, España"
}


# =========================
# GENERAR DICCIONARIO
# =========================
delegaciones = {}

print("Geocodificando delegaciones reales...\n")

for clave, direccion in delegaciones_reales.items():

    print(direccion)

    coords = obtener_coordenadas(direccion)

    ciudad = direccion.split(",")[1].strip()

    calle_num = direccion.split(",")[0]
    partes = calle_num.split(" ")
    numero = partes[-1]
    calle = " ".join(partes[:-1])

    delegaciones[clave] = {
        "delegacion": clave,
        "pais": "España",
        "ciudad": ciudad,
        "calle": calle,
        "numero": int(numero),
        "coordenadas": coords
    }


# =========================
# GUARDAR FICHERO
# =========================
with open("../datos/obsoletos/dic_delegaciones.py", "w", encoding="utf-8") as f:
    f.write("# Delegaciones SEUR reales geolocalizadas\n")
    f.write("delegaciones = {\n")

    items = list(delegaciones.items())
    for i, (k, v) in enumerate(items):

        linea = f'    "{k}": {v}'
        if i < len(items) - 1:
            linea += ","
        linea += "\n"

        f.write(linea)

    f.write("}\n")


print("\nArchivo dic_delegaciones.py generado correctamente")