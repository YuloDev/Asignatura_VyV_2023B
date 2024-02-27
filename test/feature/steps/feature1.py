from behave import *
from test.modelos.modelo import *
from datetime import datetime

use_step_matcher("re")

@step("que un vendedor tiene uno o varios pedidos")
def step_impl(context):
    # Crear un vendedor
    context.vendedor = Vendedor("Juan", [])  # Se le proporciona una lista vacía de pedidos al instanciar el vendedor

    # Almacenar información de la tabla en el contexto
    context.informacion_pedidos = []
    for row in context.table:
        pedido = Pedido.from_row(row)
        context.informacion_pedidos.append({"pedido": pedido, "etapa": row["etapa_pedido"].lower()})

        # Agregar el pedido a la lista de pedidos del vendedor
        context.vendedor.agregar_pedido(pedido, row["etapa_pedido"].lower())

    print(f"El vendedor {context.vendedor.nombre_vendedor} tiene {context.vendedor.contar_pedidos()} pedidos.")

    # Verificar que el vendedor tenga al menos un pedido
    assert context.vendedor.contar_pedidos() > 0, "El vendedor no tiene ningún pedido"

    # Obtener el último pedido del vendedor
    ultimo_pedido = context.vendedor.lista_pedidos[-1]

    # Comparar el número de pedido del último pedido con la suma total de pedidos
    suma_total_pedidos = context.vendedor.contar_pedidos()
    assert ultimo_pedido.numero_pedido == str(suma_total_pedidos).zfill(
        2), "El número total de pedidos del vendedor no coincide"


@step("el numero de pedidos totales y el tiempo estimado para cada etapa en dias es el siguiente")
def step_impl(context):
    # Crear una instancia del Modelo (o Etapa, dependiendo de tu diseño)
    context.modelo = TiempoEtapa()

    # Calcular la información de las etapas utilizando el método en el modelo
    info_etapas = context.modelo.calcular_info_etapas(context.vendedor.lista_pedidos)

    # Iterar sobre las filas de la tabla de BDD
    for row in context.table:
        # Obtener el nombre de la etapa de la fila y convertirlo a minúsculas
        etapa_nombre = row["etapa_pedido"].lower()

        # Obtener el número total de pedidos y el tiempo estimado para la etapa actual
        total_pedidos = info_etapas[etapa_nombre]["total_pedidos"]
        tiempo_etapa = info_etapas[etapa_nombre]["tiempo_etapa"]

        # Comparar con los valores proporcionados en la tabla de BDD
        assert total_pedidos == int(
            row["total_pedidos"]), f"El número total de pedidos para la etapa {etapa_nombre} no coincide"
        assert tiempo_etapa == int(row["tiempo_etapa"]), f"El tiempo estimado para la etapa {etapa_nombre} no coincide"


@step("accede al resumen del seguimiento interno en la etapa de precompra")
def step_impl(context):
    # Llamamos al método para obtener el resumen del vendedor
    context.resumen_PreCompra = context.vendedor.obtener_resumen_etapa("PreCompra")
    assert (context.resumen_PreCompra is not None), "El resumen no se ha generado"



@step("accede al resumen del seguimiento interno en la etapa de reserva")
def step_impl(context):
    # Llamamos al método para obtener el resumen del vendedor
    context.resumen_PreCompra = context.vendedor.obtener_resumen_etapa("Reserva")
    assert (context.resumen_PreCompra is not None), "El resumen no se ha generado"


@step("accede al resumen del seguimiento interno en la etapa de listo_para_entregar")
def step_impl(context):
    # Llamamos al método para obtener el resumen del vendedor
    context.resumen_PreCompra = context.vendedor.obtener_resumen_etapa("listo_para_entregar")
    assert (context.resumen_PreCompra is not None), "El resumen no se ha generado"


@step(
    "puede visualizar gráficas que proporcionen información sobre el numero de pedidos totales, el numero de pedidos cancelados, el numero de pedidos a tiempo y el numero de pedidos atrasados cuando sobrepasan el tiempo estimado para la etapa de precompra")
def step_impl(context):
    # Validar los datos con la tabla de características
    for row in context.table:
        estado_pedido = row["estado_pedido"]
        numero_pedidos_esperados = int(row["numero_pedidos"])

        if estado_pedido == "a_tiempo":
            assert context.resumen_PreCompra.num_pedidos_a_tiempo == numero_pedidos_esperados, f"El número de pedidos a tiempo no coincide"
        elif estado_pedido == "atrasado":
            assert context.resumen_PreCompra.num_pedidos_atrasados == numero_pedidos_esperados, f"El número de pedidos atrasados no coincide"
        elif estado_pedido == "cancelado":
            assert context.resumen_PreCompra.num_pedido_cancelados == numero_pedidos_esperados, f"El número de pedidos cancelados no coincide"
        else:
            raise ValueError(f"Estado de pedido no reconocido: {estado_pedido}")

@step(
    "puede visualizar gráficas que proporcionen información sobre el numero de pedidos totales, el numero de pedidos cancelados, el numero de pedidos a tiempo y el numero de pedidos atrasados cuando sobrepasan el tiempo estimado para la etapa de reserva")
def step_impl(context):
    # Validar los datos con la tabla de características
    for row in context.table:
        estado_pedido = row["estado_pedido"]
        numero_pedidos_esperados = int(row["numero_pedidos"])

        if estado_pedido == "a_tiempo":
            assert context.resumen_PreCompra.num_pedidos_a_tiempo == numero_pedidos_esperados, f"El número de pedidos a tiempo no coincide"
        elif estado_pedido == "atrasado":
            assert context.resumen_PreCompra.num_pedidos_atrasados == numero_pedidos_esperados, f"El número de pedidos atrasados no coincide"
        elif estado_pedido == "cancelado":
            assert context.resumen_PreCompra.num_pedido_cancelados == numero_pedidos_esperados, f"El número de pedidos cancelados no coincide"
        else:
            raise ValueError(f"Estado de pedido no reconocido: {estado_pedido}")


@step(
    "puede visualizar gráficas que proporcionen información sobre el numero de pedidos totales, el numero de pedidos cancelados, el numero de pedidos a tiempo y el numero de pedidos atrasados cuando sobrepasan el tiempo estimado para la etapa de listo_para_entregar")
def step_impl(context):
    # Validar los datos con la tabla de características
    for row in context.table:
        estado_pedido = row["estado_pedido"]
        numero_pedidos_esperados = int(row["numero_pedidos"])

        if estado_pedido == "a_tiempo":
            assert context.resumen_PreCompra.num_pedidos_a_tiempo == numero_pedidos_esperados, f"El número de pedidos a tiempo no coincide"
        elif estado_pedido == "atrasado":
            assert context.resumen_PreCompra.num_pedidos_atrasados == numero_pedidos_esperados, f"El número de pedidos atrasados no coincide"
        elif estado_pedido == "cancelado":
            assert context.resumen_PreCompra.num_pedido_cancelados == numero_pedidos_esperados, f"El número de pedidos cancelados no coincide"
        else:
            raise ValueError(f"Estado de pedido no reconocido: {estado_pedido}")
