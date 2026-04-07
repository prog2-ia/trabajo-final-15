###==================================Librarys==================================###
import datetime
import math

###==================================Classes==================================###
"""
FIXME: Significant refactoring is required for proper graph functionality:
1. Decompose logic into Node and Edge entities.
2. Implement graph construction and traversal methods.
3. Add pathfinding methods (e.g., Dijkstra or A* algorithms).
"""


class Ruta:
    def __init__(self, inicio, fin, distancia, tipo_camino):
        self.inicio = inicio
        self.fin = fin
        self.distancia = distancia
        self.tipo_camino = tipo_camino

    def __repr__(self):
        return f"{self.inicio}-{self.fin} ({self.distancia}km, {self.tipo_camino})"


"""
FIXME: Refactor the Transport class into specific subclasses (e.g., Truck, Van).
1. Implement trade duty/tax calculations only after they are officially introduced.
2. Otherwise, focus on adding type-specific attributes, such as load capacity 
   (payload) for freight vehicles, to differentiate the subclasses.
"""


class Transporte:
    def __init__(self, nombre, costo_por_km, velocidad_km_dia, tipo_ruta_soportado):
        self.nombre = nombre
        self.costo_por_km = costo_por_km
        self.velocidad_km_dia = velocidad_km_dia
        self.tipo_ruta_soportado = tipo_ruta_soportado

    def __repr__(self):
        return f"{self.nombre}"


class Producto:  # Added new class
    """
    Класс для товаров. 
    Атрибут es_gravable (bool): True, если товар облагается налогом.
    """

    def __init__(self, nombre, taxable=False):
        self.nombre = nombre
        self.taxable = taxable

    def __repr__(self):
        status = "Taxable" if self.taxable else "Tax-Free"
        return f"{self.nombre} ({status})"


"""
FIXME: add the necessary methods to create a database and work with it
"""


class Pedido:
    TAX_RATE = 0.21  # New tax constant

    def __init__(self, producto, fecha, ruta, transporte):
        self.producto = producto
        self.fecha = fecha
        self.ruta = ruta
        self.transporte = transporte

    def calcular_costo(self):
        costo_base = self.ruta.distancia * self.transporte.costo_por_km
        if self.producto.taxable:  # New TAX_RATE feature
            return costo_base * (1 + self.TAX_RATE)
        return costo_base

    def calcular_tiempo_entrega(self):
        dias_entrega = math.ceil(self.ruta.distancia / self.transporte.velocidad_km_dia)
        fecha_estimada = self.fecha + datetime.timedelta(days=dias_entrega)
        return fecha_estimada

    def __repr__(self):
        return f"Pedido(Producto: {self.producto}, Fecha: {self.fecha}, Ruta: {self.ruta}, Transporte: {self.transporte.nombre})"


###==================================DataBase==================================###
destinos = [
    Ruta("Madrid", "Alicante", 420, "terrestre"),
    Ruta("Sevilla", "Huelva", 90, "terrestre")
]

vehiculos = [
    Transporte("Coche", 1.2, 600, "terrestre"),
    Transporte("Camion", 0.5, 400, "terrestre"),
    Transporte("Barco", 0.8, 200, "acuático"),
    Transporte("Avión", 3.5, 2000, "aéreo")
]

productos = [
    Producto("Queso", taxable=False),  # Updated database
    Producto("Leche", taxable=False),
    Producto("Smartphone", taxable=True),
    Producto("Vino", taxable=True)
]

pedidos = []

###==================================Main code==================================###

print("=" * 50)
print("Welcome to the Logistics Management System!")
print("Our service helps you calculate the best routes and costs for your delivery.")
print("Ready to start? Let's build your order step by step.")
print("=" * 50 + "\n")

while True:
    print("\n--- Starting a New Order ---")
    while True:
        print('Products available:', [p.nombre for p in productos])  # New cycle logic
        prod_input = input('Select product: ')
        prod_encontrado = None
        for p in productos:
            if p.nombre == prod_input:
                prod_encontrado = p
                break
        if prod_encontrado:
            break
        else:
            print('Error: Product not found.')

    while True:
        print('Elige una ruta:', destinos)
        inicio_input = input('inicio: ')
        fin_input = input('fin: ')
        ruta_encontrada = None
        for r in destinos:
            if r.fin == fin_input and r.inicio == inicio_input:
                ruta_encontrada = r
                break
        if ruta_encontrada:
            break
        else:
            print('error: ruta no existe')

    while True:
        nombres_vehiculos = [v.nombre for v in vehiculos]
        print('Elige un transporte:', nombres_vehiculos)
        trans = input()

        vehiculo_encontrado = None
        for v in vehiculos:
            if v.nombre == trans:
                vehiculo_encontrado = v
                break

        if vehiculo_encontrado:
            if vehiculo_encontrado.tipo_ruta_soportado == ruta_encontrada.tipo_camino:
                break
            else:
                print(f"error: {vehiculo_encontrado.nombre} no puede viajar por ruta {ruta_encontrada.tipo_camino}")
        else:
            print('error: transporte no válido')

    mi_pedido = Pedido(producto=prod_encontrado, fecha=datetime.date.today(), ruta=ruta_encontrada,
                       transporte=vehiculo_encontrado)
    pedidos.append(mi_pedido)

    print("\n" + "=" * 40)
    print("ALL CURRENT ORDERS IN SYSTEM:")
    print("=" * 40)

    for i in range(len(pedidos)):
        p = pedidos[i]
        print(f"Order #{i + 1}:")
        print(f"  - Product: {p.producto}")
        print(f"  - Route: {p.ruta}")
        print(f"  - Cost: ${p.calcular_costo():.2f}")
        print("-" * 20)
    repeat = input("\nWould you like to place another order? (y/n): ")
    if repeat != 'y':
        print("\nThank you for using our service! Have a great day.")
        break
