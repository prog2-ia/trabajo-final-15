# from programas.generar_rutas_despachos import (
#     recoger_pedidos as ejecutar
# )
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

from clases.vehiculo import Vehiculo

from persistencia.persistencia_rutas import (
    cargar_rutas,
    guardar_rutas
)

from persistencia.persistencia_pedidos import (
    cargar_pedidos,
    guardar_pedidos
)

from persistencia.persistencia_delegaciones import (
    cargar_delegaciones
)

from persistencia.persistencia_vehiculos import (
    cargar_vehiculos,
    guardar_vehiculos
)
def recoger_pedidos():

    delegaciones = cargar_delegaciones()

    rutas = cargar_rutas()

    pedidos = cargar_pedidos()

    cargar_vehiculos()


    # ======================================================
    # FILTRAR RUTAS ACTIVAS
    # ======================================================
    rutas_activas = {}

    for rid, r in rutas.items():

        if (
                r["tipo"].lower() == "recogida"
                and
                not r.get("finalizada", False)
        ):

            rutas_activas[rid] = r

    # ======================================================
    # VALIDACIÓN
    # ======================================================
    if not rutas_activas:

        print("\n❌ No existen rutas activas")

        return

    # ======================================================
    # MOSTRAR RUTAS ACTIVAS
    # ======================================================
    print("\n")
    print("=" * 180)
    print(" RUTAS ACTIVAS ")
    print("=" * 180)

    print(
        f"{'Ruta':<10}"
        f"{'Delegación':<25}"
        f"{'Vehículo':<20}"
        f"{'Pedidos'}"
    )

    print("-" * 180)

    for rid, r in rutas_activas.items():

        print(
            f"{rid:<10}"
            f"{r['delegacion']:<25}"
            f"{r.get('vehiculo', 'N/A'):<20}"
            f"{', '.join(r['lista_pedidos'])}"
        )

    # ======================================================
    # SELECCIÓN RUTA
    # ======================================================
    ruta = None

    ruta_id = None

    while ruta is None:

        ruta_id = input(
            "\nNúmero ruta: "
        ).strip()

        if ruta_id not in rutas_activas:

            print("❌ Ruta incorrecta")

            continue

        ruta = rutas_activas[ruta_id]

    # ======================================================
    # MOSTRAR PEDIDOS
    # ======================================================
    print("\n")
    print("=" * 80)
    print(" PEDIDOS DE LA RUTA ")
    print("=" * 80)

    for pid in ruta["lista_pedidos"]:

        estado = pedidos[pid]["estado"]

        print(
            f"Pedido {pid} | "
            f"Estado: {estado}"
        )

    # ======================================================
    # PEDIDOS RECOGIDOS
    # ======================================================
    pedidos_recogidos = None

    while pedidos_recogidos is None:

        entrada = input(
            "\nPedidos recogidos "
            "(coma separados o 'todos'): "
        ).strip().lower()

        # --------------------------------------------------
        # TODOS
        # --------------------------------------------------
        if entrada == "todos":

            pedidos_recogidos = list(
                ruta["lista_pedidos"]
            )

            break

        # --------------------------------------------------
        # VALIDAR LISTA
        # --------------------------------------------------
        lista = []

        error = False

        for x in entrada.split(","):

            pid = x.strip()

            if pid not in ruta["lista_pedidos"]:

                print(
                    f"❌ Pedido incorrecto: {pid}"
                )

                error = True

            else:

                lista.append(pid)

        if error:

            continue

        pedidos_recogidos = lista

    # ======================================================
    # CONFIRMACIÓN
    # ======================================================
    confirmar = input(
        "\n¿Confirmar recogida? (s/n): "
    ).strip().lower()

    if confirmar != "s":

        print("\n❌ Operación cancelada")

        return
    # ======================================================
    # ACTUALIZAR ESTADO PEDIDOS RECOGIDOS
    # ======================================================

    nombre_delegacion = ruta["delegacion"]

    numero_despacho = (
        nombre_delegacion
        .lower()
        .replace("despacho", "")
        .strip()
    )

    nuevo_estado = (
        f"en_despacho_{numero_despacho}"
    )

    for pid in pedidos_recogidos:

        pedidos[pid]["estado"] = nuevo_estado
    # ======================================================
    # ELIMINAR PEDIDOS DE LA RUTA
    # ======================================================
    pedidos_restantes = []

    for pid in ruta["lista_pedidos"]:

        if pid not in pedidos_recogidos:

            pedidos_restantes.append(pid)

    ruta["lista_pedidos"] = pedidos_restantes

    # ======================================================
    # SI QUEDAN PEDIDOS
    # ======================================================
    if pedidos_restantes:

        print("\n")
        print("=" * 80)
        print(" PEDIDOS PENDIENTES ")
        print("=" * 80)

        for pid in pedidos_restantes:

            print(f"Pedido {pid}")

        finalizar = input(
            "\n¿Marcar ruta como finalizada? (s/n): "
        ).strip().lower()

        if finalizar == "s":

            # ==============================================
            # MARCAR RUTA FINALIZADA
            # ==============================================
            ruta["finalizada"] = True

            # ==============================================
            # LIBERAR VEHÍCULO
            # ==============================================
            matricula = ruta["vehiculo"]

            for v in Vehiculo.vehiculos_registrados():

                if v.matricula == matricula:

                    v.disponible = True
                    break

            guardar_vehiculos(
                Vehiculo.vehiculos_registrados()
            )

            # ==============================================
            # DEVOLVER PEDIDOS A GENERADO
            # ==============================================
            for pid in pedidos_restantes:

                pedidos[pid]["estado"] = "generado"

    # ======================================================
    # SI NO QUEDAN PEDIDOS
    # ======================================================
    else:

        ruta["finalizada"] = True

        matricula = ruta["vehiculo"]

        for v in Vehiculo.vehiculos_registrados():

            if v.matricula == matricula:

                v.disponible = True
                break

        guardar_vehiculos(
            Vehiculo.vehiculos_registrados()
        )

    # ======================================================
    # GUARDAR
    # ======================================================
    guardar_rutas(rutas)

    guardar_pedidos(pedidos)

    print(
        "\n✔ Pedidos recogidos correctamente"
    )

def ejecutar():
    recoger_pedidos()
# ==========================================================
# MAIN
# ==========================================================
if __name__ == "__main__":

    ejecutar()
