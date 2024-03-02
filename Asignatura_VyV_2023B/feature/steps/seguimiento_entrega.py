from behave import *
from pytest_bdd import scenario, given, when, then
import datetime
import os
# from datetime import datetime
import django

django.setup()

import django

from marketplace.models import *

use_step_matcher("re")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Asignatura_VyV_2023B.settings')

@given("que un Vendedor tiene los siguientes Pedidos")
def step_impl():
    pass



@when("el Vendedor visualice el resumen de los Pedidos en una etapa (?P<etapa>.+)")
def step_impl():
    pass


@then("se actualizarán los estados de los Pedidos según el tiempo actual de la zona")
def step_impl():
    pass


@then("se mostrarán el siguiente estado (?P<estado_pedido>.+) con la siguiente cantidad de pedidos (?P<numero_pedidos>.+)")
def step_impl():
    pass