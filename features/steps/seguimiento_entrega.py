from behave import *

from marketplace.models import Pedido, Vendedor
from django.utils import timezone
import datetime

use_step_matcher("re")


@step("que un Vendedor tiene varios Pedidos")
def step_impl(context):
    vendedor, _ = Vendedor.objects.get_or_create(nombre="Luis Almache")  # Corregido
    context.vendedor = vendedor
    for row in context.table:
        Pedido.objects.create(
            estado_pedido=row['estado_pedido'],
            etapa_pedido=row['etapa_pedido'],
            fecha_creacion_pedido=datetime.datetime.strptime(row['fecha_creacion_pedido'], '%Y-%m-%d').date(),
            fecha_entrega_cliente_estimada=datetime.datetime.strptime(row['fecha_entrega_cliente'], '%Y-%m-%d').date(),
            vendedor=vendedor
        )

@step('el Vendedor visualice el resumen de los Pedidos en etapa "listo para entregar"')
def step_impl(context):
    context.resumen = context.vendedor.listar_pedidos_listo_para_entregar()
    print(context.resumen)

@step("se actulizarán los estados de los Pedidos según el tiempo actual")
def step_impl(context):
    for pedido in context.resumen:
        pedido.actualizar_estado_pedido()


@step("se mostrarán los siguientes datos")
def step_impl(context):
    # Asumiendo que context.resumen ya contiene todos los pedidos relevantes para el vendedor.
    # Calcular la cantidad de pedidos a tiempo y atrasados.
    pedidos_a_tiempo = int(context.vendedor.contar_pedidos_a_tiempo_listo_para_entregar())
    pedidos_atrasados = int(context.vendedor.contar_pedidos_atrasados_listo_para_entregar())

    # Crear un diccionario para mapear los estados de los pedidos a las variables calculadas
    estados_pedidos = {
        'a_tiempo': pedidos_a_tiempo,
        'atrasado': pedidos_atrasados,
    }

    # Iterar sobre cada fila de la tabla en el escenario
    for row in context.table:
        estado_pedido = row['estado_pedido']
        numero_pedidos_esperado = int(row['numero_pedidos'])  # Asegurar que el número es un entero

        # Realizar el assert para comparar el número de pedidos esperado vs. el obtenido
        assert estados_pedidos[
                   estado_pedido] == numero_pedidos_esperado, f"Se esperaban {numero_pedidos_esperado} pedidos '{estado_pedido}', pero se encontraron {estados_pedidos[estado_pedido]}."






