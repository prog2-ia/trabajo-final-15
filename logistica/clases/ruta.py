
# from geopy.distance import geodesic

class Ruta:
    """
    Representa una ruta logística formada por varios pedidos.
    """

    def __init__(self, id_ruta, distancia=0):
        """
        Constructor de la ruta.

        Parámetros
        ----------
        id_ruta : str
            Identificador de la ruta
        distancia : float
            Distancia total estimada de la ruta
        """

        self.id_ruta = id_ruta
        self.lista_pedidos = []
        self.distancia_total = distancia

    # --------------------------------------------------

    def agregar_pedido(self, pedido):
        """
        Añade un pedido a la ruta.
        """

        self.lista_pedidos.append(pedido)

    # --------------------------------------------------

    def eliminar_pedido(self, id_pedido):
        """
        Elimina un pedido de la ruta.
        """

        self.lista_pedidos = [
            p for p in self.lista_pedidos
            if p.id != id_pedido
        ]

    # --------------------------------------------------

    def numero_pedidos(self):
        """
        Devuelve el número total de pedidos.
        """

        return len(self.lista_pedidos)

    # --------------------------------------------------

    def peso_total(self):
        """
        Calcula el peso total de los pedidos.
        """

        return sum(p.peso for p in self.lista_pedidos)

    # --------------------------------------------------

    def volumen_total(self):
        """
        Calcula el volumen total de los pedidos.
        """

        return sum(p.volumen for p in self.lista_pedidos)

    # --------------------------------------------------

    def calcular_distancia(self):
        """
        Calcula distancia total de la ruta usando coordenadas reales.
        """

        if len(self.lista_pedidos) < 2:
            return 0

        distancia = 0

        for i in range(len(self.lista_pedidos) - 1):

            p1 = self.lista_pedidos[i]
            p2 = self.lista_pedidos[i + 1]

            coord1 = p1.coordenadas_destino()
            coord2 = p2.coordenadas_destino()

            distancia += geodesic(coord1, coord2).km

        # multiplicamos por 1.2 para aproximar carreteras reales
        distancia *= 1.2

        self.distancia_total = distancia

        return distancia
    # --------------------------------------------------

    def calcular_coste(self, precio_km=1.5):
        """
        Calcula el coste de la ruta.

        coste = distancia * precio_km
        """

        return self.distancia_total * precio_km

    # --------------------------------------------------

    def listar_pedidos(self):
        """
        Devuelve una lista de strings con los pedidos.
        """

        return [str(p) for p in self.lista_pedidos]

    # --------------------------------------------------

    def generar_albaran_ruta(self):
        """
        Genera un albarán de la ruta en formato texto.
        """

        texto = []
        texto.append(f"\n\n\nALBARÁN RUTA {self.id_ruta}")
        texto.append("-" * 30)

        for p in self.lista_pedidos:
            texto.append(str(p))

        texto.append("-" * 30)
        texto.append(f"Total pedidos: {self.numero_pedidos()}")
        texto.append(f"Peso total: {self.peso_total():.2f} kg")
        texto.append(f"Volumen total: {self.volumen_total():.2f} l")
        texto.append(f"Distancia: {self.distancia_total:.2f} km")
        texto.append(f"Coste estimado: {self.calcular_coste():.2f} €")

        return "\n".join(texto)

    def recorrido_ciudades(self):
        """
        Devuelve el recorrido de ciudades de la ruta.
        """

        if not self.lista_pedidos:
            return "Ruta vacía"

        ciudades = [p.origen for p in self.lista_pedidos]

        # añadimos el último destino
        ciudades.append(self.lista_pedidos[-1].destino)

        return " → ".join(ciudades)

    # --------------------------------------------------

    def __lt__(self, other):
        """
        Permite comparar rutas por coste.
        """

        return self.calcular_coste() < other.calcular_coste()

    # --------------------------------------------------

    def __len__(self):
        """
        Permite usar len(ruta).
        """

        return len(self.lista_pedidos)

    # --------------------------------------------------
    def __str__(self):

        return (
            f"Ruta {self.id_ruta} | "
            f"{len(self.lista_pedidos)} pedidos | "
            f"{self.distancia_total:} km | "
            f"{self.recorrido_ciudades()} | "
            f"{self.generar_albaran_ruta()}"
        )

    


