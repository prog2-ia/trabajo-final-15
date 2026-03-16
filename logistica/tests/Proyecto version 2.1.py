import datetime

class Ruta:
    def __init__(self, inicio, fin, distancia):
        self.inicio = inicio
        self.fin = fin
        self.distancia = distancia

    def __repr__(self):
        return f"{self.inicio}-{self.fin}({self.distancia}km)"

# New class
class Pedido:
    def __init__(self, producto, fecha, ruta, transporte):
        self.producto = producto
        self.fecha = fecha
        self.ruta = ruta
        self.transporte = transporte

    def __repr__(self):
        return f"Pedido(Producto: {self.producto}, Fecha: {self.fecha}, Ruta: {self.ruta}, Transporte: {self.transporte})"

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

mi_pedido = Pedido(producto=prod, fecha=datetime.date.today(), ruta=ruta_encontrada, transporte=trans)

print(mi_pedido)
