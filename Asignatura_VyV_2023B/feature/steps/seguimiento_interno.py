import django

django.setup()
from behave import *
from django.test import RequestFactory
from marketplace.views import seguimiento_interno
from marketplace.models import *

use_step_matcher("re")


@step("que un vendedor tiene uno o varios pedidos")
def step_impl(context):
    # Crear vendedor
    context.vendedor = Vendedor.objects.get_or_create(nombre="Rafa")

    # Iteramos sobre las filas de la tabla para obtener los datos de los pedidos
    for row in context.table:
        # Utilizamos get_or_create para obtener o crear un pedido con los datos proporcionados
        if row["etapa_pedido"] == "precompra":
            Pedido.objects.get_or_create(
                etapa_pedido=row["etapa_pedido"],
                pedido_activo=row["pedido_activo"],
                estado_pedido=row["estado_pedido"],
                fecha_creacion_pedido=row["fecha_creacion_pedido"],
                fecha_etapa_precompra=row["fecha_etapa_precompra"]
            )

        if row["etapa_pedido"] == "reserva":
            Pedido.objects.get_or_create(
                etapa_pedido=row["etapa_pedido"],
                pedido_activo=row["pedido_activo"],
                estado_pedido=row["estado_pedido"],
                fecha_creacion_pedido=row["fecha_creacion_pedido"],
                fecha_etapa_precompra=row["fecha_etapa_precompra"],
                fecha_etapa_reserva=row["fecha_etapa_reserva"]
            )

        if row["etapa_pedido"] == "listo_para_entregar":
            Pedido.objects.get_or_create(
                etapa_pedido=row["etapa_pedido"],
                pedido_activo=row["pedido_activo"],
                estado_pedido=row["estado_pedido"],
                fecha_creacion_pedido=row["fecha_creacion_pedido"],
                fecha_etapa_precompra=row["fecha_etapa_precompra"],
                fecha_etapa_reserva=row["fecha_etapa_reserva"],
                fecha_listo_para_entregar=row["fecha_etapa_listo_para_entregar"]
            )

    # Verificamos si el vendedor tiene algún pedido
    assert Pedido.objects.filter(vendedor__vendedorID=1).count() > 0, "El vendedor no tiene ningún pedido"


@step("el numero de pedidos totales y el tiempo estimado para cada etapa en dias es el siguiente")
def step_impl(context):
    # # Crear una instancia de la clase Etapa
    # context.etapa = Etapa()
    #
    # # Agregar pedidos a cada una de las etapas
    # for pedido in context.vendedor.lista_pedidos:
    #     context.etapa.agregar_pedido(pedido, pedido.etapa_pedido)
    #
    # # Calcular la información de las etapas utilizando el método en el modelo
    # info_etapas = context.etapa.calcular_info_etapas()
    #
    # # Iterar sobre las filas de la tabla de BDD
    # for row in context.table:
    #     # Obtener el nombre de la etapa de la fila y convertirlo a minúsculas
    #     etapa_nombre = row["etapa_pedido"].lower()
    #
    #     # Obtener el número total de pedidos y el tiempo estimado para la etapa actual
    #     total_pedidos = info_etapas[etapa_nombre]["total_pedidos"]
    #     tiempo_etapa = info_etapas[etapa_nombre]["tiempo_etapa"]
    #
    #     # Comparar con los valores proporcionados en la tabla de BDD
    #     assert total_pedidos == int(
    #         row["total_pedidos"]), f"El número total de pedidos para la etapa {etapa_nombre} no coincide"
    #     assert tiempo_etapa == int(row["tiempo_etapa"]), f"El tiempo estimado para la etapa {etapa_nombre} no coincide"

    pass


@step("accede al resumen del seguimiento interno en la etapa de precompra")
def step_impl(context):
    request_factory = RequestFactory()
    request = request_factory.get('/seguimientoInterno/')
    response = seguimiento_interno(request)
    assert response.status_code == 200


@step("accede al resumen del seguimiento interno en la etapa de reserva")
def step_impl(context):
    request_factory = RequestFactory()
    request = request_factory.get('/seguimientoInterno/')
    response = seguimiento_interno(request)
    assert response.status_code == 200


@step("accede al resumen del seguimiento interno en la etapa de listo_para_entregar")
def step_impl(context):
    request_factory = RequestFactory()
    request = request_factory.get('/seguimientoInterno/')
    response = seguimiento_interno(request)
    assert response.status_code == 200


@step(
    "puede visualizar gráficas que proporcionen información sobre el numero de pedidos totales, el numero de pedidos cancelados, el numero de pedidos a tiempo y el numero de pedidos atrasados cuando sobrepasan el tiempo estimado para la etapa de precompra")
def step_impl(context):
    # # Validar los datos con la tabla de características
    # for row in context.table:
    #     estado_pedido = row["estado_pedido"]
    #     numero_pedidos_esperados = int(row["numero_pedidos"])
    #
    #     if estado_pedido == "a_tiempo":
    #         assert context.resumen_PreCompra.num_pedidos_a_tiempo == numero_pedidos_esperados, f"El número de pedidos a tiempo no coincide"
    #     elif estado_pedido == "atrasado":
    #         assert context.resumen_PreCompra.num_pedidos_atrasados == numero_pedidos_esperados, f"El número de pedidos atrasados no coincide"
    #     elif estado_pedido == "cancelado":
    #         assert context.resumen_PreCompra.num_pedido_cancelados == numero_pedidos_esperados, f"El número de pedidos cancelados no coincide"
    #     else:
    #         raise ValueError(f"Estado de pedido no reconocido: {estado_pedido}")
    pass


@step(
    "puede visualizar gráficas que proporcionen información sobre el numero de pedidos totales, el numero de pedidos cancelados, el numero de pedidos a tiempo y el numero de pedidos atrasados cuando sobrepasan el tiempo estimado para la etapa de reserva")
def step_impl(context):
    # # Validar los datos con la tabla de características
    # for row in context.table:
    #     estado_pedido = row["estado_pedido"]
    #     numero_pedidos_esperados = int(row["numero_pedidos"])
    #
    #     if estado_pedido == "a_tiempo":
    #         assert context.resumen_PreCompra.num_pedidos_a_tiempo == numero_pedidos_esperados, f"El número de pedidos a tiempo no coincide"
    #     elif estado_pedido == "atrasado":
    #         assert context.resumen_PreCompra.num_pedidos_atrasados == numero_pedidos_esperados, f"El número de pedidos atrasados no coincide"
    #     elif estado_pedido == "cancelado":
    #         assert context.resumen_PreCompra.num_pedido_cancelados == numero_pedidos_esperados, f"El número de pedidos cancelados no coincide"
    #     else:
    #         raise ValueError(f"Estado de pedido no reconocido: {estado_pedido}")
    pass


@step(
    "puede visualizar gráficas que proporcionen información sobre el numero de pedidos totales, el numero de pedidos cancelados, el numero de pedidos a tiempo y el numero de pedidos atrasados cuando sobrepasan el tiempo estimado para la etapa de listo_para_entregar")
def step_impl(context):
    pass
