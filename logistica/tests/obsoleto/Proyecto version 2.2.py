import datetime
import math

class Ruta:
    def __init__(self, inicio, fin, distancia):
        self.inicio = inicio
        self.fin = fin
        self.distancia = distancia

    def __repr__(self):
        return f"{self.inicio}-{self.fin}({self.distancia}km)"

class Pedido:
    def __init__(self, producto, fecha, ruta, transporte):
        self.producto = producto
        self.fecha = fecha
        self.ruta = ruta
        self.transporte = transporte

    #cost calculator
    def calcular_costo(self):
        matricula_val = float(self.transporte['matricula'].replace('$', ''))
        costo = (matricula_val * self.ruta.distancia) / 100
        return costo

    # fecha final de pedido calculator
    def calcular_tiempo_entrega(self):
        dias_entrega = math.ceil(self.ruta.distancia / 100)
        fecha_estimada = self.fecha + datetime.timedelta(days=dias_entrega)
        return fecha_estimada

    def __repr__(self):
        return f"Pedido(Producto: {self.producto}, Fecha: {self.fecha}, Ruta: {self.ruta}, Transporte: {self.transporte['tipo']})"

destinos = [
    Ruta("Madrid", "Alicante", 420),
    Ruta("Sevilla", "Huelva", 90,)
]

vehiculo = {'matricula': '100$','tipo': 'coche'}
productos = ['queso','leche']

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
    print('Elige un transporte:', vehiculo['tipo'])
    trans = input()
    
    if trans == vehiculo['tipo']:
        error_3 = 1
    else:
        print('error')

mi_pedido = Pedido(producto=prod, fecha=datetime.date.today(), ruta=ruta_encontrada, transporte=vehiculo)

# info output
print(f"\n--- Detalles del Pedido ---")
print(mi_pedido)
print(f"Costo estimado: {mi_pedido.calcular_costo()}$")
print(f"Fecha de entrega (estimada): {mi_pedido.calcular_tiempo_entrega()}")
