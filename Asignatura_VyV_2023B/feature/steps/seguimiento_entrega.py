from behave import *

use_step_matcher("re")


@step("que un Vendedor tiene los siguientes Pedidos")
def step_impl(context):
    pass


@step("el Vendedor visualice el resumen de los Pedidos en una etapa (?P<etapa>.+)")
def step_impl(context, etapa):
    pass


@step("se actualizarán los estados de los Pedidos según el tiempo actual de la zona")
def step_impl(context):
    pass


@step("se mostrarán el siguiente estado (?P<estado_pedido>.+) con la siguiente cantidad de pedidos (?P<numero_pedidos>.+)")
def step_impl(context, estado_pedido, numero_pedidos):
    pass
