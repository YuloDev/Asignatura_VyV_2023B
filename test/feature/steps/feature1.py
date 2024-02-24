from behave import *
from test.modelos.modelo import *

use_step_matcher("re")

@step("que un vendedor tiene uno o varios pedidos")
def step_impl(context):
    pass

@step("el numero de pedidos totales y el tiempo estimado para cada etapa en dias es el siguiente")
def step_impl(context):
    pass

@step("accede al resumen del seguimiento interno en la etapa de precompra")
def step_impl(context):
    pass

@step(
    "puede visualizar gráficas que proporcionen información sobre el numero de pedidos totales, el numero de pedidos cancelados, el numero de pedidos a tiempo y el numero de pedidos atrasados cuando sobrepasan el tiempo estimado para la etapa de precompra")
def step_impl(context):
    pass