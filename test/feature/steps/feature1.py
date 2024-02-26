from behave import *
from test.modelos.modelo import *
from datetime import datetime

use_step_matcher("re")

@step("que un vendedor tiene uno o varios pedidos")
def step_impl(context):
    # Crear un vendedor
    context.vendedor = Vendedor("Juan", [])  # Se le proporciona una lista vacía de pedidos al instanciar el vendedor

    # Iterar sobre las filas de la tabla
    for row in context.table:
        # Crear un objeto Pedido con los datos de la fila
        pedido = Pedido.from_row(row)

        # Agregar el pedido a la lista de pedidos del vendedor
        context.vendedor.agregar_pedido(pedido)

    print(f"El vendedor {context.vendedor.nombre_vendedor} tiene {context.vendedor.contar_pedidos()} pedidos.")

    # Verificar que el vendedor tenga al menos un pedido
    assert context.vendedor.contar_pedidos() > 0, "El vendedor no tiene ningún pedido"

    # Obtener el último pedido del vendedor
    ultimo_pedido = context.vendedor.lista_pedidos[-1]

    # Comparar el número de pedido del último pedido con la suma total de pedidos
    suma_total_pedidos = context.vendedor.contar_pedidos()
    assert ultimo_pedido.numero_pedido == str(suma_total_pedidos).zfill(2), "El número total de pedidos del vendedor no coincide"

@step("el numero de pedidos totales y el tiempo estimado para cada etapa en dias es el siguiente")
def step_impl(context):
    # Crear un diccionario para almacenar la información de cada etapa
    info_etapas = {}

    # Iterar sobre las Etapas
    for etapa in EtapaEncuentra:
        etapa_nombre = etapa.name.lower()  # Utilizar .name para obtener el nombre del Enum y pasarlo a minúsculas

        # Definir el tiempo etapa fijo para cada etapa de acuerdo a lo que definimos
        if etapa_nombre == "precompra":
            tiempo_etapa = 2
        elif etapa_nombre == "reserva":
            tiempo_etapa = 4
        elif etapa_nombre == "listo_para_entregar":
            tiempo_etapa = 2
        else:
            tiempo_etapa = 0  # Este de aquí es por si crearamos otras etapas pero como no creo entonces se le deja así nomas

        # Filtrar los pedidos por la etapa actual
        pedidos_etapa = [pedido for pedido in context.vendedor.lista_pedidos if pedido.etapa_pedido == etapa_nombre]

        # Obtener el número total de pedidos
        total_pedidos = len(pedidos_etapa)

        # Almacenar la información en el diccionario
        info_etapas[etapa_nombre] = {"total_pedidos": total_pedidos, "tiempo_etapa": tiempo_etapa}

        # Imprimir información para verificar
        print(f"Etapa: {etapa_nombre}, Total Pedidos: {total_pedidos}, Tiempo Estimado: {tiempo_etapa} días")

    # Verificar que el número total de pedidos y el tiempo estimado coinciden con la tabla proporcionada
    for row in context.table:
        etapa_nombre = row["etapa_pedido"].lower()  # Convertir a minúsculas

        total_pedidos = info_etapas[etapa_nombre]["total_pedidos"]
        tiempo_etapa = info_etapas[etapa_nombre]["tiempo_etapa"]

        # Verificar que los valores coincidan con la tabla proporcionada
        assert total_pedidos == int(
            row["total_pedidos"]), f"El número total de pedidos para la etapa {etapa_nombre} no coincide"
        assert tiempo_etapa == int(row["tiempo_etapa"]), f"El tiempo estimado para la etapa {etapa_nombre} no coincide"


@step("accede al resumen del seguimiento interno en la etapa de precompra")
def step_impl(context):
    pass


@step(
    "puede visualizar gráficas que proporcionen información sobre el numero de pedidos totales, el numero de pedidos cancelados, el numero de pedidos a tiempo y el numero de pedidos atrasados cuando sobrepasan el tiempo estimado para la etapa de precompra")
def step_impl(context):
    # Genera el resumen de precompra
    resumen_precompra = context.vendedor.generar_resumen_precompra()

    # Verifica el número de pedidos a tiempo, atrasados y cancelados en la etapa de precompra
    for row in context.table:
        # Obtiene el estado de pedido y el número esperado de la data table
        estado_pedido = row["estado_pedido"]
        numero_pedidos_esperados = int(row["numero_pedidos"])

        # Compara con assert los valores obtenidos del resumen con los valores esperados de la data table
        if estado_pedido == "a_tiempo":
            assert resumen_precompra.num_pedidos_a_tiempo == numero_pedidos_esperados, \
                f"El número de pedidos a tiempo no coincide para la etapa de precompra"
        elif estado_pedido == "atrasado":
            assert resumen_precompra.num_pedidos_atrasados == numero_pedidos_esperados, \
                f"El número de pedidos atrasados no coincide para la etapa de precompra"
        elif estado_pedido == "cancelado":
            assert resumen_precompra.num_pedido_cancelados == numero_pedidos_esperados, \
                f"El número de pedidos cancelados no coincide para la etapa de precompra"