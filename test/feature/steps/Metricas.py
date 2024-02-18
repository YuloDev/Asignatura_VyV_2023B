from datetime import date
from behave import *
from modelos.modelos import *

use_step_matcher("re")


@step("que un vendedor tiene 4 productos vendidos en diciembre")
def step_impl(context):
    context.producto = Producto(10, 6)
    context.vendedor = Vendedor("nombre")
    context.vendedor.vender([context.producto], date(2024, 12, 1))
    context.vendedor.vender([context.producto], date(2024, 12, 1))
    context.vendedor.vender([context.producto], date(2024, 12, 1))
    context.vendedor.vender([context.producto], date(2024, 12, 1))
    assert (context.vendedor.numero_ventas == 4)


@step("el vendedor estableció las metas: número de ventas, ingresos, costos y beneficio por venta para diciembre")
def step_impl(context):
    context.vendedor.establecer_meta(Metrica(TipoDeMetrica.NUMERO_DE_VENTAS, 8, date(2024, 12, 1)))
    assert (context.vendedor.tiene_metas(12) == True)


@step("se despliegue el Dashboard de Métricas en diciembre")
def step_impl(context):
    context.dashboard = context.vendedor.obtener_dashboard(date(2024, 12, 1))
    assert (context.dashboard is not None)


@step("se mostrará el número de ventas, ingresos, costos, beneficio por venta de diciembre")
def step_impl(context):
    assert ((context.dashboard.obtener_numero_venta() == 4) and
            (context.dashboard.obtener_ingresos() == 40) and
            (context.dashboard.obtener_costos() == 24) and
            (context.dashboard.obtener_beneficio_por_venta() == 4))


@step("se mostrará la diferencia entre las metas y los valores reales de las métricas como porcentaje")
def step_impl(context):
    assert ((context.dashboard.obtener_diferecia_entre_meta_y_numero_venta() == 50) and
            (context.dashboard.obtener_diferecia_entre_meta_e_ingresos() == 66) and
            (context.dashboard.obtener_diferecia_entre_meta_y_costos() == 60) and
            (context.dashboard.obtener_diferecia_entre_meta_y_beneficio_por_venta() == 80))


@step(
    "se mostrará la diferencia entre las valores reales de las métricas de noviembre y los valores reales de las métricas de diciembre como porcentaje")
def step_impl(context):
    pass


@step(
    "si el valor real de las cuatro métricas son (?P<comparacion>.+) por al menos (?P<porcentaje>.+)% al valor de las metas se recomendará (?P<recomendacion>.+)")
def step_impl(context, comparacion, porcentaje, recomendacion):
    pass
