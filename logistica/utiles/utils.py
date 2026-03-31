
from math import radians, sin, cos, sqrt, atan2
import random

# from datos.dic_ciudades import CIUDADES   # importar diccionario de ciudades
# from datos.ciudades_alicante import CIUDADES_ALICANTE



def distancia_km(coord1, coord2):

    lat1, lon1 = coord1
    lat2, lon2 = coord2

    R = 6371  # radio de la Tierra en km

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c

def encontrar_raiz(proyecto="logistica"):

    import os

    ruta = os.path.abspath(os.path.dirname(__file__))

    while True:
        if os.path.basename(ruta) == proyecto:
            return ruta

        nueva = os.path.dirname(ruta)

        if nueva == ruta:
            return None

        ruta = nueva

def limpiar_texto(txt):
        return str(txt).replace("'", "").replace('"', "")

def validar_dni_real(dni):

    if len(dni) != 9:
        return False

    numero = dni[:8]
    letra = dni[-1].upper()

    if not numero.isdigit():
        return False

    letras = "TRWAGMYFPDXBNJZSQVHLCKE"

    return letra == letras[int(numero) % 23]

def generar_dni_real():

    numero = random.randint(10000000, 99999999)
    letras = "TRWAGMYFPDXBNJZSQVHLCKE"
    letra = letras[numero % 23]

    return f"{numero}{letra}"

def validar_matricula_esp(matricula):

    if not matricula:
        return False

    matricula = matricula.upper().replace(" ", "")

    if len(matricula) != 7:
        return False

    numeros = matricula[:4]
    letras = matricula[4:]

    if not numeros.isdigit():
        return False

    letras_validas = "BCDFGHJKLMNPRSTVWXYZ"

    for l in letras:
        if l not in letras_validas:
            return False

    return True



def generar_matricula():

    """
    Genera matricula española valida
    Ejemplo: 1234 ABC
    """

    numeros = random.randint(1000, 9999)

    letras_validas = "BCDFGHJKLMNPRSTVWXYZ"

    letras = "".join(random.choice(letras_validas) for _ in range(3))

    return f"{numeros} {letras}"

def validar_unicidad(valor, conjunto):

    if valor in conjunto:
        return False

    conjunto.add(valor)
    return True
