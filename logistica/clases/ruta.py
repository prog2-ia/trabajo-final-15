class Ruta:
    """
    Representa una ruta logística formada por varios pedidos.
    """

    def __init__(self, distancia=0):
        """
        Constructor de la clase Ruta.

        Parámetros:
        distancia (float): distancia total estimada de la ruta.
        """

        self.lista_pedidos = []
        self.distancia_total = distancia

    def agregar_pedido(self, pedido):
        """
        Añade un pedido a la ruta.

        Parámetros:
        pedido (Pedido): objeto pedido que se añadirá a la ruta.
        """

        self.lista_pedidos.append(pedido)

    def calcular_distancia(self):
        """
        Devuelve la distancia total de la ruta.
        """

        return self.distancia_total

    def calcular_coste(self, precio_km=1.5):
        """
        Calcula el coste de la ruta.

        Parámetros:
        precio_km (float): coste por kilómetro.

        Devuelve:
        float
        """

        return self.distancia_total * precio_km

    def numero_pedidos(self):
        """
        Devuelve el número de pedidos de la ruta.
        """

        return len(self.lista_pedidos)

    def __lt__(self, other):
        """
        Permite comparar rutas por coste.
        """

        return self.calcular_coste() < other.calcular_coste()

    def __str__(self):
        """
        Representación en texto de la ruta.
        """

        return f"Ruta con {len(self.lista_pedidos)} pedidos y {self.distancia_total} km"