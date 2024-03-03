from behave import *
from faker import Faker
from marketplace.models import *
import datetime

use_step_matcher("re")

@step("que un Vendedor tiene los siguientes Pedidos registrados")
def step_impl(context):
    faker = Faker()
    vendedor, _ = Vendedor.objects.get_or_create(
        nombre=faker.name()
    )
    context.vendedor = vendedor
    for row in context.table:
        Pedido.objects.get_or_create(
            estado_pedido=row['estado_pedido'],
            etapa_pedido=row['etapa_pedido'],
            fecha_listo_para_entregar=datetime.datetime.strptime(row['fecha_listo_para_entregar'], '%Y-%m-%d').date(),
            vendedor=vendedor
        )
@step("ha pasado (?P<anios>.+) años (?P<meses>.+) meses (?P<semanas>.+) semanas (?P<dias>.+) dias, desde su fecha listo para entregar")
def step_impl(context, anios, meses, semanas, dias):
    context.anios = anios
    context.meses = meses
    context.semanas = semanas
    context.dias = dias


@step("el Vendedor visualice el resumen de los Pedidos en la etapa (?P<etapa>.+) una vez se han actualizado los estados de los Pedidos segun el tiempo que ha pasado")
def step_impl(context, etapa):
    context.etapa = etapa
    context.resumen = context.vendedor.listar_pedidos_por_etapa(etapa)
    print(context.resumen)
    for pedido in context.resumen:
         pedido.actualizar_estado_pedido(int(context.anios), int(context.meses), int(context.semanas), int(context.dias))

# @step("se actualizarán los estados de los Pedidos según el tiempo que ha pasado")
# def step_impl(context):
#     for pedido in context.resumen:
#         pedido.actualizar_estado_pedido(int(context.anios), int(context.meses), int(context.semanas), int(context.dias))


@step("se mostrara el estado (?P<estado_pedido>.+) con la siguiente cantidad de pedidos (?P<numero_pedidos>.+)")
def step_impl(context, estado_pedido, numero_pedidos):
    num_pedidos = int(context.vendedor.contar_pedidos_por_estado_en_etapa(context.etapa, estado_pedido))
    assert (num_pedidos == int(
        numero_pedidos)), f"Se esperaban {numero_pedidos} pedidos '{estado_pedido}', pero se encontraron {num_pedidos}."

@step("que un Vendedor tiene los siguientes Pedidos registrados en estado PNE")
def step_impl(context):
    faker = Faker()
    vendedor, _ = Vendedor.objects.get_or_create(
        nombre=faker.name()
    )
    context.vendedor = vendedor
    context.pedidos = []

    for row in context.table:
        pedido, creado = Pedido.objects.get_or_create(
            estado_pedido=row['estado_pedido'],
            etapa_pedido=row['etapa_pedido'],
            fecha_listo_para_entregar=datetime.datetime.strptime(row['fecha_listo_para_entregar'], '%Y-%m-%d').date(),
            vendedor=vendedor
        )
        # Agregar solo pedido creado no la tupla completa, método get_or_create de Django devuelve una tupla (objeto, creado) y objeto es la instancia del modelo, creado solo es booleano que indica si se creó una nueva instancia
        context.pedidos.append(pedido)

@step("los Pedidos estan registrados como cliente no encontrado")
def step_impl(context):
    for pedido in context.pedidos:
        pedido.marcar_cliente_no_encontrado()


@step("el Vendedor visualice el resumen de los Pedidos en la etapa PNE")
def step_impl(context):
    context.etapa = "PNE"
    context.resumen = context.vendedor.listar_pedidos_por_etapa(context.etapa)
    print(context.resumen)

