import random
import time
from geopy.geocoders import Nominatim

# =========================
# CONFIGURACION GEOPY
# =========================
geolocator = Nominatim(user_agent="clientes_app")

# =========================
# CACHE
# =========================
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
# DNI
# =========================
def generar_dni():
    numero = random.randint(10000000, 99999999)
    letras = "TRWAGMYFPDXBNJZSQVHLCKE"
    return f"{numero}{letras[numero % 23]}"


# =========================
# NOMBRES (20)
# =========================
nombres = [
    "Antonio", "José", "Manuel", "Francisco", "David",
    "Juan", "Javier", "Daniel", "Carlos", "Miguel",
    "Alejandro", "Rafael", "Luis", "Fernando", "Pablo",
    "Sergio", "Álvaro", "Adrián", "Iván", "Rubén"
]

# =========================
# APELLIDOS (40)
# =========================
apellidos = [
    "García", "Fernández", "González", "Rodríguez", "López",
    "Martínez", "Sánchez", "Pérez", "Gómez", "Ruiz",
    "Díaz", "Hernández", "Moreno", "Muñoz", "Álvarez",
    "Romero", "Alonso", "Gutiérrez", "Navarro", "Torres",
    "Domínguez", "Vázquez", "Ramos", "Gil", "Ramírez",
    "Serrano", "Blanco", "Suárez", "Molina", "Morales",
    "Ortega", "Delgado", "Castro", "Ortiz", "Rubio",
    "Marín", "Sanz", "Iglesias", "Núñez", "Medina"
]

# =========================
# CIUDADES Y CALLES
# =========================
ciudades = {

    # -------- ALICANTE --------
    "Alicante": [
        "Calle San Vicente", "Avenida Maisonnave", "Calle Mayor",
        "Calle Castaños", "Avenida Alfonso X", "Calle Pintor Aparicio",
        "Avenida Aguilera", "Calle Gerona", "Calle Italia", "Calle Francia"
    ],

    "Elche": [
        "Calle Reina Victoria", "Avenida Libertad", "Calle Jorge Juan",
        "Calle Obispo Winibal", "Calle Antonio Machado", "Calle Blas Valero",
        "Calle José María Buck", "Calle Doctor Caro", "Calle Alfonso XII", "Calle Filet de Fora"
    ],

    "Torrevieja": [
        "Calle Ramón Gallud", "Calle Caballero de Rodas", "Calle del Mar",
        "Calle Apolo", "Calle Pedro Lorca", "Calle Bazán",
        "Calle Zoa", "Calle La Loma", "Calle San Pascual", "Calle Patricio Pérez"
    ],

    "Orihuela": [
        "Calle Mayor", "Calle San Pascual", "Calle Hospital",
        "Calle Ramón y Cajal", "Calle Soleres", "Calle Aragón",
        "Calle Duque de Tamames", "Calle Santa Justa", "Calle San Juan", "Calle Obispo Rocamora"
    ],

    "Benidorm": [
        "Avenida Mediterráneo", "Calle Gerona", "Calle Ibiza",
        "Avenida Europa", "Calle Lepanto", "Calle Murcia",
        "Calle Esperanto", "Calle Londres", "Calle Berlín", "Calle París"
    ],

    "Alcoy": [
        "Calle San Nicolás", "Calle País Valencià", "Calle Oliver",
        "Calle Entenza", "Calle Alzamora", "Calle Santa Rosa",
        "Calle Alicante", "Calle Isabel la Católica", "Calle El Camí", "Calle Sabadell"
    ],

    "Elda": [
        "Calle Nueva", "Calle Jardines", "Calle Dahellos",
        "Calle Ortega y Gasset", "Calle Antonino Vera", "Calle Padre Manjón",
        "Calle Colón", "Calle Reyes Católicos", "Calle San Roque", "Calle La Cruz"
    ],

    "San Vicente del Raspeig": [
        "Calle Alicante", "Calle Ancha de Castelar", "Calle Mayor",
        "Calle San Pascual", "Calle La Huerta", "Calle Río Turia",
        "Calle Cervantes", "Calle Doctor Fleming", "Calle Lillo Juan", "Calle Poeta Miguel Hernández"
    ],

    "Villena": [
        "Calle Mayor", "Calle Corredera", "Calle Nueva",
        "Calle San Sebastián", "Calle San Francisco", "Calle Joaquín María López",
        "Calle Rambla", "Calle Navarro Santafé", "Calle La Virgen", "Calle El Hilo"
    ],

    "Denia": [
        "Calle Marqués de Campo", "Calle La Mar", "Calle Diana",
        "Calle Campos", "Calle Colón", "Calle Sandunga",
        "Calle Magallanes", "Calle Loreto", "Calle Pare Pere", "Calle Calderón"
    ],

    # -------- MADRID --------
    "Madrid": [
        "Gran Vía", "Calle Alcalá", "Paseo Castellana",
        "Calle Serrano", "Calle Goya", "Calle Atocha",
        "Calle Velázquez", "Calle Princesa", "Calle Mayor", "Calle Fuencarral"
    ],

    "Móstoles": [
        "Calle Simón Hernández", "Avenida Portugal", "Calle Baleares",
        "Calle Canarias", "Calle Barcelona", "Calle Zaragoza",
        "Calle Toledo", "Calle Burgos", "Calle Sevilla", "Calle Madrid"
    ],

    "Alcalá de Henares": [
        "Calle Mayor", "Calle Libreros", "Calle Santiago",
        "Calle Cervantes", "Calle Tinte", "Calle Empecinado",
        "Calle Teniente Ruiz", "Calle Colegios", "Calle Victoria", "Calle Imagen"
    ],

    "Fuenlabrada": [
        "Calle Leganés", "Calle Móstoles", "Calle Humanes",
        "Calle Málaga", "Calle Francia", "Calle Grecia",
        "Calle Italia", "Calle Alemania", "Calle Portugal", "Calle Holanda"
    ],

    "Leganés": [
        "Calle Juan Muñoz", "Calle Madrid", "Calle Getafe",
        "Calle Alcorcón", "Calle Fuenlabrada", "Calle Toledo",
        "Calle Barcelona", "Calle Sevilla", "Calle Zaragoza", "Calle Valencia"
    ],

    "Getafe": [
        "Calle Madrid", "Calle Toledo", "Calle Leganés",
        "Calle Fuenlabrada", "Calle Alcalá", "Calle Valencia",
        "Calle Barcelona", "Calle Zaragoza", "Calle Sevilla", "Calle Granada"
    ],

    "Alcorcón": [
        "Calle Mayor", "Calle Porto Cristo", "Calle Polvoranca",
        "Calle Oslo", "Calle Estocolmo", "Calle Viena",
        "Calle Berlín", "Calle París", "Calle Roma", "Calle Lisboa"
    ],

    "Parla": [
        "Calle Real", "Calle Pinto", "Calle Leganés",
        "Calle Getafe", "Calle Toledo", "Calle Madrid",
        "Calle Valencia", "Calle Barcelona", "Calle Sevilla", "Calle Zaragoza"
    ],

    "Torrejón de Ardoz": [
        "Calle Enmedio", "Calle Madrid", "Calle Pesquera",
        "Calle Londres", "Calle París", "Calle Roma",
        "Calle Lisboa", "Calle Berlín", "Calle Viena", "Calle Oslo"
    ],

    "Alcobendas": [
        "Calle Marquesa Viuda Aldama", "Calle Constitución", "Calle Libertad",
        "Calle Mayor", "Calle Real", "Calle Madrid",
        "Calle Valencia", "Calle Barcelona", "Calle Sevilla", "Calle Zaragoza"
    ]
}


# =========================
# GENERAR DIRECCIONES
# =========================
def generar_direcciones_unicas(n=20):
    direcciones = set()

    ciudades_lista = list(ciudades.keys())

    while len(direcciones) < n:
        ciudad = random.choice(ciudades_lista)
        calle = random.choice(ciudades[ciudad])
        numero = random.randint(1, 50)

        direccion = f"{calle} {numero}, {ciudad}, España"
        direcciones.add(direccion)

    return list(direcciones)


# =========================
# GENERAR CLIENTES
# =========================
def generar_clientes(n=100):

    clientes = {}

    direcciones = generar_direcciones_unicas(20)
    coords_direcciones = {}

    print("Geocodificando...\n")

    for direccion in direcciones:
        print(direccion)

        coords = obtener_coordenadas(direccion)

        if not coords:
            ciudad = direccion.split(",")[1]
            coords = obtener_coordenadas(f"{ciudad}, España")

        coords_direcciones[direccion] = coords

    print("\nGenerando clientes...\n")

    for i in range(n):

        direccion = random.choice(direcciones)

        calle_num, ciudad, _ = direccion.split(",")

        partes = calle_num.strip().split(" ")
        numero = partes[-1]
        calle = " ".join(partes[:-1])

        cliente = {
            "dni": generar_dni(),
            "nombre": random.choice(nombres),
            "apellidos": f"{random.choice(apellidos)} {random.choice(apellidos)}",
            "pais": "España",
            "ciudad": ciudad.strip(),
            "calle": calle,
            "numero": int(numero),
            "coordenadas": coords_direcciones[direccion]
        }

        clientes[f"cliente_{i+1}"] = cliente

    return clientes


# =========================
# EJECUCION
# =========================
clientes = generar_clientes(100)

for k, v in list(clientes.items())[:]:
    print(k, v)