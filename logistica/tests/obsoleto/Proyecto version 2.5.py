import datetime
import math


class Ruta:
    # Nuevo parametro tipo_camino
    def __init__(self, inicio, fin, distancia, tipo_camino):
        self.inicio = inicio
        self.fin = fin
        self.distancia = distancia
        self.tipo_camino = tipo_camino

    def __repr__(self):
        return f"{self.inicio}-{self.fin} ({self.distancia}km, {self.tipo_camino})"


# Nuevo classe
class Transporte:
    def __init__(self, nombre, costo_por_km, velocidad_km_dia, tipo_ruta_soportado):
        self.nombre = nombre
        self.costo_por_km = costo_por_km
        self.velocidad_km_dia = velocidad_km_dia
        self.tipo_ruta_soportado = tipo_ruta_soportado

    def __repr__(self):
        return f"{self.nombre}"


class Pedido:
    def __init__(self, producto, fecha, ruta, transporte):
        self.producto = producto
        self.fecha = fecha
        self.ruta = ruta
        self.transporte = transporte

    # Updated cost calculator (distancia * costo_por_km)
    def calcular_costo(self):
        costo = self.ruta.distancia * self.transporte.costo_por_km
        return costo

    # Updated fecha final de pedido calculator (distancia / velocidad_km_dia)
    def calcular_tiempo_entrega(self):
        dias_entrega = math.ceil(self.ruta.distancia / self.transporte.velocidad_km_dia)
        fecha_estimada = self.fecha + datetime.timedelta(days=dias_entrega)
        return fecha_estimada

    def __repr__(self):
        return f"Pedido(Producto: {self.producto}, Fecha: {self.fecha}, Ruta: {self.ruta}, Transporte: {self.transporte.nombre})"


# Updated data with path_tipe (terrestre)
destinos = [
    Ruta("Madrid", "Alicante", 420, "terrestre"),
    Ruta("Sevilla", "Huelva", 90, "terrestre")
]

# Nuevos datos de transporte
vehiculos = [
    Transporte("Coche", 1.2, 600, "terrestre"),
    Transporte("Camion", 0.5, 400, "terrestre"),
    Transporte("Barco", 0.8, 200, "acuático"),
    Transporte("Avión", 3.5, 2000, "aéreo")
]

productos = ['queso', 'leche']

error_1 = 0
error_2 = 0
error_3 = 0

while error_1 == 0:
    print('Elige un producto:', productos)
    prod = input()
    if prod in productos:
        error_1 = 1
    else:
        print('error')

while error_2 == 0:
    print('Elige una ruta:', destinos)
    inicio_input = input('inicio: ')
    fin_input = input('fin: ')
    ruta_encontrada = None
    for r in destinos:
        if r.fin == fin_input and r.inicio == inicio_input:
            ruta_encontrada = r
            break
    if ruta_encontrada:
        error_2 = 1
    else:
        print('error: ruta no existe')

while error_3 == 0:
    nombres_vehiculos = [v.nombre for v in vehiculos]
    print('Elige un transporte:', nombres_vehiculos)
    trans = input()

    vehiculo_encontrado = None
    for v in vehiculos:
        if v.nombre == trans:
            vehiculo_encontrado = v
            break

    if vehiculo_encontrado:
        # Check for path tipe
        if vehiculo_encontrado.tipo_ruta_soportado == ruta_encontrada.tipo_camino:
            error_3 = 1
        else:
            print(f"error: {vehiculo_encontrado.nombre} no puede viajar por ruta {ruta_encontrada.tipo_camino}")
    else:
        print('error: transporte no válido')

# Added tipe of transport (vehiculo_encontrado)
mi_pedido = Pedido(producto=prod, fecha=datetime.date.today(), ruta=ruta_encontrada, transporte=vehiculo_encontrado)

# info output
print(f"\n--- Detalles del Pedido ---")
print(mi_pedido)
print(f"Costo estimado: {mi_pedido.calcular_costo()}$")
print(f"Fecha de entrega (estimada): {mi_pedido.calcular_tiempo_entrega()}")
