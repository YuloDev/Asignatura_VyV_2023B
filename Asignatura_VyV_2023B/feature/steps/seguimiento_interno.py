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
    # Calcular el número total de pedidos en cada etapa
    total_pedidos_precompra = Pedido.objects.filter(etapa_pedido="precompra").count()
    total_pedidos_reserva = Pedido.objects.filter(etapa_pedido="reserva").count()
    total_pedidos_listo_para_entregar = Pedido.objects.filter(etapa_pedido="listo_para_entregar").count()

    # Verificar si los resultados son los esperados
    assert total_pedidos_precompra == 2, "El número de pedidos en la etapa de precompra no es el esperado"
    assert total_pedidos_reserva == 2, "El número de pedidos en la etapa de reserva no es el esperado"
    assert total_pedidos_listo_para_entregar == 2, "El número de pedidos en la etapa de listo para entregar no es el esperado"


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
    # Filtrar pedidos en la etapa de precompra
    pedidos_precompra = Pedido.objects.filter(etapa_pedido="PC")

    # Contar pedidos a tiempo, atrasados y cancelados en la etapa de precompra
    p_a_tiempo = pedidos_precompra.filter(estado_pedido="AT").count()
    p_atrasados = pedidos_precompra.filter(estado_pedido="A").count()
    p_cancelados = pedidos_precompra.filter(estado_pedido="C").count()

    # Verificar si los resultados son los esperados
    assert p_a_tiempo == 1, "El número de pedidos a tiempo en la etapa de precompra no es el esperado"
    assert p_atrasados == 0, "El número de pedidos atrasados en la etapa de precompra no es el esperado"
    assert p_cancelados == 1, "El número de pedidos cancelados en la etapa de precompra no es el esperado"


@step(
    "puede visualizar gráficas que proporcionen información sobre el numero de pedidos totales, el numero de pedidos cancelados, el numero de pedidos a tiempo y el numero de pedidos atrasados cuando sobrepasan el tiempo estimado para la etapa de reserva")
def step_impl(context):
    # Filtrar pedidos en la etapa de precompra
    pedidos_reserva = Pedido.objects.filter(etapa_pedido="R")

    # Contar pedidos a tiempo, atrasados y cancelados en la etapa de precompra
    p_a_tiempo = pedidos_reserva.filter(estado_pedido="AT").count()
    p_atrasados = pedidos_reserva.filter(estado_pedido="A").count()
    p_cancelados = pedidos_reserva.filter(estado_pedido="C").count()

    # Verificar si los resultados son los esperados
    assert p_a_tiempo == 1, "El número de pedidos a tiempo en la etapa de reserva no es el esperado"
    assert p_atrasados == 1, "El número de pedidos atrasados en la etapa de reserva no es el esperado"
    assert p_cancelados == 0, "El número de pedidos cancelados en la etapa de reserva no es el esperado"


@step(
    "puede visualizar gráficas que proporcionen información sobre el numero de pedidos totales, el numero de pedidos cancelados, el numero de pedidos a tiempo y el numero de pedidos atrasados cuando sobrepasan el tiempo estimado para la etapa de listo_para_entregar")
def step_impl(context):
    # Filtrar pedidos en la etapa de precompra
    pedidos_listo_para_entregar = Pedido.objects.filter(etapa_pedido="LE")

    # Contar pedidos a tiempo, atrasados y cancelados en la etapa de precompra
    p_a_tiempo = pedidos_listo_para_entregar.filter(estado_pedido="AT").count()
    p_atrasados = pedidos_listo_para_entregar.filter(estado_pedido="A").count()
    p_cancelados = pedidos_listo_para_entregar.filter(estado_pedido="C").count()

    # Verificar si los resultados son los esperados
    assert p_a_tiempo == 0, "El número de pedidos a tiempo en la etapa de listo para entregar no es el esperado"
    assert p_atrasados == 1, "El número de pedidos atrasados en la etapa de listo para entregar no es el esperado"
    assert p_cancelados == 1, "El número de pedidos cancelados en la etapa de listo para entregar no es el esperado"
