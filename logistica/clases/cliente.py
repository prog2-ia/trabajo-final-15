"""
Clase clientes. utilizada como base para generar los pedidos
Puede utilizarse como origen o destino de un pedido
contiene los atributos de pais, ciudad, calle, numero, coordenadas geograficas


    Representa un cliente del sistema logistico

    ATRIBUTOS
    dni -> identificador del cliente
    direccion -> objeto de la clase Direccion
    pedidos_en_curso -> lista de pedidos activos
    pedidos_terminados -> lista de pedidos finalizados
    importe_facturado -> importe total facturado

    METODOS
    validar_dni -> comprueba si el dni es valido
    validar_direccion -> valida la direccion usando la clase Direccion
    __add__ -> anade pedidos a pedidos_en_curso
    __sub__ -> mueve pedidos a pedidos_terminados
    """
class Cliente:
    def __init__(self, dni, direccion):

        self._dni = dni
        self._direccion = direccion

        self._pedidos_en_curso = []
        self._pedidos_terminados = []

        self._importe_facturado = 0

    # ==========================================
    # GETTERS
    # ==========================================

    @property
    def dni(self):
        return self._dni

    @property
    def direccion(self):
        return self._direccion

    @property
    def pedidos_en_curso(self):
        return self._pedidos_en_curso

    @property
    def pedidos_terminados(self):
        return self._pedidos_terminados

    @property
    def importe_facturado(self):
        return self._importe_facturado

    # ==========================================
    # VALIDACIONES
    # ==========================================

    def validar_dni(self):
        """
        valida formato basico de dni
        8 numeros + 1 letra
        """

        if not isinstance(self._dni, str):
            return None

        if len(self._dni) != 9:
            return None

        numeros = self._dni[:8]
        letra = self._dni[8]

        if not numeros.isdigit():
            return None

        if not letra.isalpha():
            return None

        return True

    def validar_direccion(self):
        """
        valida direccion usando objeto Direccion
        """

        if self._direccion is None:
            return None

        return self._direccion.validar()

    # ==========================================
    # OPERADORES
    # ==========================================

    def __add__(self, pedido):
        """
        anade pedido a pedidos_en_curso
        """

        if pedido is None:
            return self

        self._pedidos_en_curso.append(pedido)
        return self

    def __sub__(self, pedido):
        """
        mueve pedido de en curso a terminado
        """

        if pedido is None:
            return self

        if pedido in self._pedidos_en_curso:
            self._pedidos_en_curso.remove(pedido)
            self._pedidos_terminados.append(pedido)

            # suma al importe si el pedido tiene km
            if hasattr(pedido, "km") and pedido.km is not None:
                self._importe_facturado += pedido.km

        return self

    # ==========================================
    # REPRESENTACION
    # ==========================================
    def __str__(self):

        # convertir listas de pedidos a texto
        pedidos_curso_str = [str(p) for p in self._pedidos_en_curso]
        pedidos_terminados_str = [str(p) for p in self._pedidos_terminados]

        return (
            f"Cliente {self._dni}\n"
            f"Direccion: {self._direccion}\n\n"
            f"Pedidos en curso:\n"
            f"{pedidos_curso_str}\n\n"
            f"Pedidos terminados:\n"
            f"{pedidos_terminados_str}\n\n"
            f"Importe facturado: {self._importe_facturado}"
        )

