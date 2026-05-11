"""
==========================================================
MÓDULO: mantenimiento_vehiculos.py
==========================================================

Mantenimiento completo de vehículos.

FUNCIONALIDADES:
✔ Altas
✔ Modificaciones
✔ Bajas
✔ Listados

CARACTERÍSTICAS:
✔ Validación de matrículas únicas
✔ Validación según tipo de delegación
✔ Persistencia en fichero texto
✔ Gestión automática de mochilas

REGLAS:
✔ Central  → Camión
✔ Base     → Furgoneta
✔ Despacho → Furgoneta / Motocicleta / Mochila
"""

# ==========================================================
# IMPORTS
# ==========================================================
import os
import sys

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '..'
        )
    )
)

from clases.delegacion import (
    DelegacionCentral,
    DelegacionBase,
    DelegacionDespacho
)

from clases.vehiculo import (
    Vehiculo,
    VehiculoCamion,
    VehiculoFurgoneta,
    VehiculoMotocicleta,
    VehiculoMochila
)

from persistencia.persistencia_delegaciones import (
    cargar_delegaciones
)
from persistencia.persistencia_vehiculos import (
    guardar_vehiculos,
    cargar_vehiculos
)

from utiles.utils import (
    generar_matricula,
    validar_matricula_esp
)

# ==========================================================
# BUSCAR VEHÍCULO
# ==========================================================
def buscar_vehiculo(matricula, vehiculos):

    matricula = matricula.upper()

    for v in vehiculos:

        if v.matricula == matricula:
            return v

    return None


# ==========================================================
# BUSCAR DELEGACIÓN
# ==========================================================
def buscar_delegacion(nombre, delegaciones):

    for d in delegaciones:

        if d.nombre.lower() == nombre.lower():
            return d

    return None


# ==========================================================
# IMPRIMIR JERARQUÍA
# ==========================================================
def imprimir_jerarquia(delegaciones):

    ANCHO_NOMBRE = 35

    def imprimir_linea(prefijo, delegacion):

        nombre = f"{prefijo}{delegacion.nombre}"

        print(
            f"{nombre:<{ANCHO_NOMBRE}}"
            f"│ {delegacion.provincia}"
        )

    centrales = [

        d for d in delegaciones

        if isinstance(
            d,
            DelegacionCentral
        )
    ]

    for central in centrales:

        imprimir_linea(
            "",
            central
        )

        bases = [

            d for d in delegaciones

            if isinstance(
                d,
                DelegacionBase
            )

            and d.delegacion_superior == central
        ]

        for b in bases:

            imprimir_linea(
                "   ├── ",
                b
            )

            despachos = [

                d for d in delegaciones

                if isinstance(
                    d,
                    DelegacionDespacho
                )

                and d.delegacion_superior == b
            ]

            for dep in despachos:

                imprimir_linea(
                    "   │     ├── ",
                    dep
                )



# ==========================================================
# PEDIR MOCHILA
# ==========================================================
def pedir_mochila(
        delegacion,
        vehiculos
):

    # ======================================================
    # BUSCAR SIGUIENTE CORRELATIVO
    # ======================================================
    numeros = []

    prefijo = (
        f"{delegacion.nombre}-"
    )

    for v in vehiculos:

        if v.tipo != "mochila":
            continue

        if not v.matricula.startswith(
                prefijo
        ):
            continue

        partes = v.matricula.split("-")

        if len(partes) < 2:
            continue

        numero = partes[-1]

        if numero.isdigit():

            numeros.append(
                int(numero)
            )

    siguiente = (
            max(numeros, default=0)
            + 1
    )

    # ======================================================
    # PEDIR NÚMERO
    # ======================================================
    while True:

        entrada = input(
            f"\nNúmero mochila "
            f"[{siguiente}]: "
        ).strip()

        # --------------------------------------------------
        # USAR SUGERIDO
        # --------------------------------------------------
        if not entrada:

            numero = str(siguiente)

        else:

            numero = entrada

        # --------------------------------------------------
        # VALIDAR NUMÉRICO
        # --------------------------------------------------
        if not numero.isdigit():

            print(
                "\n❌ Número inválido"
            )

            continue

        # --------------------------------------------------
        # GENERAR MATRÍCULA
        # --------------------------------------------------
        matricula = (
            f"{delegacion.nombre}"
            f"-{numero}"
        )

        # --------------------------------------------------
        # VALIDAR UNICIDAD
        # --------------------------------------------------
        existe = buscar_vehiculo(
            matricula,
            vehiculos
        )

        if existe:

            print(
                "\n❌ Mochila existente"
            )

            continue

        return matricula
# ==========================================================
# PEDIR DELEGACIÓN
# ==========================================================
def pedir_delegacion(delegaciones):

    imprimir_jerarquia(delegaciones)

    while True:

        nombre = input(
            "\nDelegación: "
        )

        d = buscar_delegacion(
            nombre,
            delegaciones
        )

        if d:
            return d

        print(
            "\n❌ Delegación no encontrada"
        )


# ==========================================================
# PEDIR MATRÍCULA
# ==========================================================
def pedir_matricula(vehiculos):

    while True:

        matricula = input(
            "\nMatrícula: "
        ).upper()

        if not validar_matricula_esp(
                matricula
        ):

            print(
                "\n❌ Matrícula inválida"
            )

            continue

        if buscar_vehiculo(
                matricula,
                vehiculos
        ):

            print(
                "\n❌ Matrícula existente"
            )

            continue

        return matricula


# ==========================================================
# PEDIR MOCHILA
# ==========================================================
def pedir_mochila(
        delegacion,
        vehiculos
):

    while True:

        numero = input(
            "\nNúmero mochila: "
        )

        if not numero.isdigit():

            print(
                "\n❌ Número inválido"
            )

            continue

        matricula = (
            f"{delegacion.nombre}"
            f"-{numero}"
        )

        existe = buscar_vehiculo(
            matricula,
            vehiculos
        )

        if existe:

            print(
                "\n❌ Mochila existente"
            )

            continue

        return matricula


# ==========================================================
# ALTAS
# ==========================================================
def alta_vehiculo(
        vehiculos,
        delegaciones
):

    print("\n" + "=" * 60)
    print("ALTA DE VEHÍCULO")
    print("=" * 60)

    # ======================================================
    # PEDIR DELEGACIÓN
    # ======================================================
    delegacion = pedir_delegacion(
        delegaciones
    )

    # ======================================================
    # CENTRAL → CAMIÓN
    # ======================================================
    if isinstance(
            delegacion,
            DelegacionCentral
    ):

        print(
            "\nTipo vehículo: CAMIÓN"
        )

        matricula = pedir_matricula(
            vehiculos
        )

        v = VehiculoCamion(
            matricula,
            True,
            delegacion,
            20000,
            40000
        )


    # ======================================================
    # BASE → FURGONETA
    # ======================================================
    elif isinstance(
            delegacion,
            DelegacionBase
    ):

        print(
            "\nTipo vehículo: FURGONETA"
        )

        matricula = pedir_matricula(
            vehiculos
        )

        v = VehiculoFurgoneta(
            matricula,
            True,
            delegacion,
            3500,
            10000
        )


    # ======================================================
    # DESPACHO
    # ======================================================
    else:

        print("\n1. Furgoneta")
        print("2. Motocicleta")
        print("3. Mochila")

        opcion = input(
            "\nTipo vehículo: "
        )

        # --------------------------------------------------
        # FURGONETA
        # --------------------------------------------------
        if opcion == "1":

            matricula = pedir_matricula(
                vehiculos
            )

            v = VehiculoFurgoneta(
                matricula,
                True,
                delegacion,
                1000,
                4000
            )


        # --------------------------------------------------
        # MOTOCICLETA
        # --------------------------------------------------
        elif opcion == "2":

            matricula = pedir_matricula(
                vehiculos
            )

            v = VehiculoMotocicleta(
                matricula,
                True,
                delegacion,
                30,
                30
            )


        # --------------------------------------------------
        # MOCHILA
        # --------------------------------------------------
        elif opcion == "3":

            matricula = pedir_mochila(
                delegacion,
                vehiculos
            )

            vehiculo = VehiculoMochila(
                matricula,
                True,
                delegacion,
                30,
                30
            )


        else:

            print(
                "\n❌ Opción inválida"
            )

            return

    # ======================================================
    # GUARDAR
    # ======================================================
    vehiculos.append(v)

    guardar_vehiculos(vehiculos)

    print("\n✔ Vehículo creado")


# ==========================================================
# MODIFICACIONES
# ==========================================================
def modificar_vehiculo(vehiculos):

    print("\n" + "=" * 60)
    print("MODIFICACIÓN DE VEHÍCULO")
    print("=" * 60)

    matricula = input(
        "\nMatrícula: "
    ).upper()

    v = buscar_vehiculo(
        matricula,
        vehiculos
    )

    if not v:

        print(
            "\n❌ Vehículo no encontrado"
        )

        return

    # ======================================================
    # MOSTRAR DATOS
    # ======================================================
    print("\nDATOS ACTUALES\n")

    print(f"Tipo       : {v.tipo}")
    print(f"Matrícula  : {v.matricula}")
    print(f"Disponible : {v.disponible}")
    print(f"Delegación : {v.delegacion.nombre}")

    # ======================================================
    # DISPONIBILIDAD
    # ======================================================
    disponible = input(
        f"\nDisponible "
        f"[{v.disponible}] "
        f"(s/n): "
    ).lower()

    if disponible == "s":

        v._disponible = True

    elif disponible == "n":

        v._disponible = False

    guardar_vehiculos(vehiculos)

    print("\n✔ Vehículo modificado")


# ==========================================================
# BAJAS
# ==========================================================
def baja_vehiculo(vehiculos):

    print("\n" + "=" * 60)
    print("BAJA DE VEHÍCULO")
    print("=" * 60)

    matricula = input(
        "\nMatrícula: "
    ).upper()

    v = buscar_vehiculo(
        matricula,
        vehiculos
    )

    if not v:

        print(
            "\n❌ Vehículo no encontrado"
        )

        return

    # ======================================================
    # MOSTRAR DATOS
    # ======================================================
    print("\nVEHÍCULO\n")

    print(f"Tipo       : {v.tipo}")
    print(f"Matrícula  : {v.matricula}")
    print(f"Disponible : {v.disponible}")
    print(f"Delegación : {v.delegacion.nombre}")

    confirmar = input(
        "\n¿Confirmar baja? (s/n): "
    ).lower()

    if confirmar != "s":

        print(
            "\n✔ Operación cancelada"
        )

        return

    vehiculos.remove(v)

    guardar_vehiculos(vehiculos)

    print("\n✔ Vehículo eliminado")


# ==========================================================
# LISTADO
# ==========================================================
def listado_vehiculos(
        vehiculos,
        delegaciones
):

    print("\n" + "=" * 60)
    print("LISTADO DE VEHÍCULOS")
    print("=" * 60)

    print("\n1. Todos")
    print("2. Por delegación")

    opcion = input(
        "\nSeleccione opción: "
    )

    resultado = vehiculos

    # ======================================================
    # FILTRAR POR DELEGACIÓN
    # ======================================================
    if opcion == "2":

        delegacion = pedir_delegacion(
            delegaciones
        )

        resultado = [

            v for v in vehiculos

            if v.delegacion == delegacion
        ]

    # ======================================================
    # MOSTRAR
    # ======================================================
    print("\n" + "=" * 140)
    print("LISTADO DE VEHÍCULOS")
    print("=" * 140)

    # ======================================================
    # CABECERA
    # ======================================================
    print(
        f"{'TIPO':<15}"
        f"{'MATRICULA':<20}"
        f"{'DISPONIBLE':<12}"
        f"{'CARGA MAX':<15}"
        f"{'CUBICAJE':<15}"
        f"{'DELEGACION'}"
    )

    print("-" * 140)

    # ======================================================
    # DATOS
    # ======================================================
    for v in vehiculos:
        print(
            f"{v.tipo:<15}"
            f"{v.matricula:<20}"
            f"{str(v.disponible):<12}"
            f"{str(v.carga_maxima):<15}"
            f"{str(v.cubicaje):<15}"
            f"{v.delegacion.nombre}"
        )


    print("\n")




# ==========================================================
# MENÚ PRINCIPAL
# ==========================================================
def ejecutar():

    delegaciones = cargar_delegaciones()

    vehiculos = cargar_vehiculos()

    while True:

        print("\n" + "=" * 60)
        print("MANTENIMIENTO DE VEHÍCULOS")
        print("=" * 60)

        print("\n1. Alta")
        print("2. Modificación")
        print("3. Baja")
        print("4. Listado")
        print("5. Salir")

        opcion = input(
            "\nSeleccione opción: "
        )

        # ==================================================
        # ALTAS
        # ==================================================
        if opcion == "1":

            alta_vehiculo(
                vehiculos,
                delegaciones
            )

        # ==================================================
        # MODIFICACIONES
        # ==================================================
        elif opcion == "2":

            modificar_vehiculo(
                vehiculos
            )

        # ==================================================
        # BAJAS
        # ==================================================
        elif opcion == "3":

            baja_vehiculo(
                vehiculos
            )

        # ==================================================
        # LISTADOS
        # ==================================================
        elif opcion == "4":

            listado_vehiculos(
                vehiculos,
                delegaciones
            )

        # ==================================================
        # SALIR
        # ==================================================
        elif opcion == "5":

            break

        else:

            print(
                "\n❌ Opción inválida"
            )


# ==========================================================
# MAIN
# ==========================================================
if __name__ == "__main__":

    ejecutar()