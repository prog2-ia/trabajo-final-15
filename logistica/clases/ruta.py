from geopy.distance import geodesic


class Ruta:

    def __init__(self, id_ruta, distancia=0):

        self.id_ruta = id_ruta
        self.lista_pedidos = []
        self.distancia_total = distancia

    def agregar_pedido(self, pedido):

        self.lista_pedidos.append(pedido)

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