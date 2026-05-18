# mantenimiento_vehiculos.py

"""
============================================================
MANTENIMIENTO DE VEHÍCULOS
============================================================

FUNCIONALIDADES:
✔ Alta
✔ Baja
✔ Modificación
✔ Listado
✔ Compatibilidad con mypy
✔ Validación de matrículas
✔ Validación de delegaciones
✔ Gestión de mochilas
"""

# ============================================================
# IMPORTS
# ============================================================
from typing import List, Optional

from clases.delegacion import (
    Delegacion,
    DelegacionBase,
    DelegacionCentral,
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
    cargar_vehiculos,
    guardar_vehiculos
)

from utiles.utils import (
    validar_matricula_esp
)


# ============================================================
# BUSCAR VEHÍCULO
# ============================================================
def buscar_vehiculo(
        matricula: str,
        vehiculos: List[Vehiculo]
) -> Optional[Vehiculo]:

    for vehiculo in vehiculos:

        if (
                vehiculo.matricula.upper()
                == matricula.upper()
        ):
            return vehiculo

    return None


# ============================================================
# BUSCAR DELEGACIÓN
# ============================================================
def buscar_delegacion(
        nombre: str,
        delegaciones: List[Delegacion]
) -> Optional[Delegacion]:

    for delegacion in delegaciones:

        if (
                delegacion.nombre.upper()
                == nombre.upper()
        ):
            return delegacion

    return None


# ============================================================
# IMPRIMIR JERARQUÍA
# ============================================================
def imprimir_jerarquia(
        delegaciones: List[Delegacion]
) -> None:

    print()
    print("=" * 90)

    print(
        f"{'TIPO':15}"
        f"{'NOMBRE':25}"
        f"{'POBLACIÓN':20}"
        f"{'PROVINCIA':20}"
    )

    print("-" * 90)

    for delegacion in delegaciones:

        print(
            f"{delegacion.tipo.upper():15}"
            f"{delegacion.nombre:25}"
            f"{delegacion.poblacion:20}"
            f"{delegacion.provincia:20}"
        )


# ============================================================
# SIGUIENTE NÚMERO MOCHILA
# ============================================================
def siguiente_numero_mochila(
        delegacion,
        vehiculos: List[Vehiculo]
) -> int:

    numeros: List[int] = []

    prefijo = (
        delegacion.nombre.upper()
        + "-"
    )

    for vehiculo in vehiculos:

        if (
                isinstance(
                    vehiculo,
                    VehiculoMochila
                )
                and vehiculo.matricula.startswith(
                    prefijo
                )
        ):

            try:

                numero = int(
                    vehiculo.matricula.split(
                        "-"
                    )[-1]
                )

                numeros.append(numero)

            except ValueError:
                pass

    if not numeros:
        return 1

    return max(numeros) + 1


# ============================================================
# PEDIR MATRÍCULA
# ============================================================
def pedir_matricula() -> str:

    while True:

        matricula = input(
            "Matrícula: "
        ).upper().strip()

        if validar_matricula_esp(
                matricula
        ):

            return matricula

        print(
            "❌ Matrícula inválida"
        )


# ============================================================
# ALTA VEHÍCULO
# ============================================================
def alta_vehiculo() -> None:

    vehiculos = cargar_vehiculos()

    delegaciones = cargar_delegaciones()

    print()
    print("=== ALTA VEHÍCULO ===")

    imprimir_jerarquia(
        delegaciones
    )

    nombre_delegacion = input(
        "\nDelegación: "
    ).strip()

    delegacion = buscar_delegacion(
        nombre_delegacion,
        delegaciones
    )

    if not delegacion:

        print(
            "❌ Delegación no encontrada"
        )

        return

    vehiculo: Vehiculo

    # ========================================================
    # CENTRAL -> CAMIÓN
    # ========================================================
    if isinstance(
            delegacion,
            DelegacionCentral
    ):

        matricula = pedir_matricula()

        vehiculo = VehiculoCamion(
            matricula,
            True,
            delegacion,
            20000,
            40
        )

    # ========================================================
    # BASE -> FURGONETA
    # ========================================================
    elif isinstance(
            delegacion,
            DelegacionBase
    ):

        matricula = pedir_matricula()

        vehiculo = VehiculoFurgoneta(
            matricula,
            True,
            delegacion,
            3500,
            10
        )

    # ========================================================
    # DESPACHO
    # ========================================================
    elif isinstance(
            delegacion,
            DelegacionDespacho
    ):

        print()
        print("1. Furgoneta")
        print("2. Motocicleta")
        print("3. Mochila")

        opcion = input(
            "Tipo: "
        ).strip()

        # ====================================================
        # FURGONETA
        # ====================================================
        if opcion == "1":

            matricula = pedir_matricula()

            vehiculo = VehiculoFurgoneta(
                matricula,
                True,
                delegacion,
                1000,
                4
            )

        # ====================================================
        # MOTOCICLETA
        # ====================================================
        elif opcion == "2":

            matricula = pedir_matricula()

            vehiculo = VehiculoMotocicleta(
                matricula,
                True,
                delegacion,
                30,
                0.03
            )

        # ====================================================
        # MOCHILA
        # ====================================================
        elif opcion == "3":

            sugerido = siguiente_numero_mochila(
                delegacion,
                vehiculos
            )

            numero = input(
                f"Número mochila [{sugerido}]: "
            ).strip()

            if numero == "":
                numero = str(sugerido)

            matricula = (
                f"{delegacion.nombre.upper()}-{numero}"
            )

            vehiculo = VehiculoMochila(
                matricula,
                True,
                delegacion,
                30,
                0.03
            )

        else:

            print(
                "❌ Opción inválida"
            )

            return

    else:

        print(
            "❌ Tipo delegación inválido"
        )

        return

    vehiculos.append(
        vehiculo
    )

    guardar_vehiculos(
        vehiculos
    )

    print()
    print(
        "✔ Vehículo creado"
    )


# ============================================================
# BAJA VEHÍCULO
# ============================================================
def baja_vehiculo() -> None:

    vehiculos = cargar_vehiculos()

    matricula = input(
        "Matrícula: "
    ).strip()

    vehiculo = buscar_vehiculo(
        matricula,
        vehiculos
    )

    if not vehiculo:

        print(
            "❌ Vehículo no encontrado"
        )

        return

    vehiculos.remove(
        vehiculo
    )

    guardar_vehiculos(
        vehiculos
    )

    print(
        "✔ Vehículo eliminado"
    )


# ============================================================
# MODIFICAR VEHÍCULO
# ============================================================
def modificar_vehiculo() -> None:

    vehiculos = cargar_vehiculos()

    matricula = input(
        "Matrícula: "
    ).strip()

    vehiculo = buscar_vehiculo(
        matricula,
        vehiculos
    )

    if not vehiculo:

        print(
            "❌ Vehículo no encontrado"
        )

        return

    print()

    print(
        f"Disponibilidad actual: {vehiculo.disponible}"
    )

    nuevo_estado = input(
        "Disponible (s/n): "
    ).lower().strip()

    vehiculo.set_disponible(
        nuevo_estado == "s"
    )

    guardar_vehiculos(
        vehiculos
    )

    print(
        "✔ Vehículo modificado"
    )


# ============================================================
# LISTAR VEHÍCULOS
# ============================================================
def listar_vehiculos() -> None:

    vehiculos = cargar_vehiculos()

    print()
    print("=" * 120)

    print(
        f"{'TIPO':15}"
        f"{'MATRÍCULA':20}"
        f"{'DISPONIBLE':15}"
        f"{'DELEGACIÓN':25}"
        f"{'CARGA':15}"
        f"{'CUBICAJE':15}"
    )

    print("-" * 120)

    for vehiculo in vehiculos:

        print(
            f"{vehiculo.tipo.upper():15}"
            f"{vehiculo.matricula:20}"
            f"{str(vehiculo.disponible):15}"
            f"{vehiculo.delegacion.nombre:25}"
            f"{vehiculo.carga_maxima:<15}"
            f"{vehiculo.cubicaje:<15}"
        )


# ============================================================
# MENÚ PRINCIPAL
# ============================================================
def ejecutar() -> None:

    while True:

        print()
        print("=" * 40)

        print(
            "MANTENIMIENTO VEHÍCULOS"
        )

        print("=" * 40)

        print("1. Alta")
        print("2. Baja")
        print("3. Modificar")
        print("4. Listar")
        print("0. Salir")

        opcion = input(
            "\nOpción: "
        ).strip()

        if opcion == "1":

            alta_vehiculo()

        elif opcion == "2":

            baja_vehiculo()

        elif opcion == "3":

            modificar_vehiculo()

        elif opcion == "4":

            listar_vehiculos()

        elif opcion == "0":

            break

        else:

            print(
                "❌ Opción inválida"
            )