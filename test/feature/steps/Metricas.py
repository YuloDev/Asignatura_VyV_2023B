from behave import *
from modelos.modelos import *

use_step_matcher("re")


@step("que un vendedor tiene (?P<cantidad>.+) ventas:")
def step_impl(context, cantidad):
    print("Primer step")
    context.vendedor = Vendedor("nombre")
    for row in context.table:
        print(row)
        fecha = row["fecha"].split("-")
        context.vendedor.vender([Producto(row["producto"], float(row["precio"]), float(row["costo"]))], int(fecha[0]), int(fecha[1]),
                                int(fecha[2]))
    assert (len(context.vendedor.obtener_ventas()) == int(cantidad)), f"Los valores no son iguales"


@step("el vendedor estableció (?P<meta_ventas>.+) ventas como la meta de número de ventas para diciembre")
def step_impl(context, meta_ventas):
    context.vendedor.establecer_meta(Meta(TipoDeMetrica.NUMERO_DE_VENTAS, int(meta_ventas), 2023, 12))
    assert (context.vendedor.obtener_meta(TipoDeMetrica.NUMERO_DE_VENTAS, 2023, 12) == int(meta_ventas))


@step("se despliegue el Dashboard de Métricas en diciembre")
def step_impl(context):
    context.dashboard = Dashboard(context.vendedor)
    context.dashborad.generar_metricas(2023, 12)
    assert (context.dashboard.se_realizaron_metricas() == True)


@step("se mostrarán (?P<ventas>.+) ventas")
def step_impl(context, ventas):
    assert (context.dashboard.obtener_ventas() == int(ventas))


@step(
    "se indicará, mediante porcentaje, que las ventas de diciembre (?P<comparacion_por_meta>.+) a la meta de ventas de diciembre")
def step_impl(context, comparacion_por_meta):
    assert (context.dashboard.obtener_comparacion_por_meta(TipoDeMetrica.NUMERO_DE_VENTAS) == TipoDeComparacion(
        comparacion_por_meta))


@step(
    "se indicará, mediante porcentaje, que las ventas de diciembre (?P<comparacion_por_mes>.+) a las ventas de noviembre")
def step_impl(context, comparacion_por_mes):
    assert (context.dashboard.obtener_comparacion_por_mes_anterior(TipoDeMetrica.NUMERO_DE_VENTAS) == TipoDeComparacion(
        comparacion_por_mes))


@step("se recomendará (?P<recomendacion>.+)")
def step_impl(context, recomendacion):
    assert (context.dashboard.obtener_recomendación(TipoDeMetrica.NUMERO_DE_VENTAS) == TipoDeRecomendacion(
        recomendacion))


@step("el vendedor estableció (?P<meta_ingresos>.+) dolares como la meta de ingresos para diciembre")
def step_impl(context, meta_ingresos):
    pass


@step("se mostrarán (?P<ingresos>.+) dolares de ingresos")
def step_impl(context, ingresos):
    pass


@step(
    "se indicará, mediante porcentaje, que los ingresos de diciembre (?P<comparacion_por_meta>.+) a la meta de ingresos de diciembre")
def step_impl(context, comparacion_por_meta):
    pass


@step(
    "se indicará, mediante porcentaje, que los ingresos de diciembre (?P<comparacion_por_mes>.+) a los ingresos de noviembre")
def step_impl(context, comparacion_por_mes):
    pass


@step("el vendedor estableció (?P<meta_costos>.+) dolares como la meta de costos para diciembre")
def step_impl(context, meta_costos):
    pass


@step("se mostrarán (?P<costos>.+) dolares de costos")
def step_impl(context, costos):
    pass


@step(
    "se indicará, mediante porcentaje, que los costos de diciembre (?P<comparacion_por_meta>.+) a la meta de costos de diciembre")
def step_impl(context, comparacion_por_meta):
    pass


@step(
    "se indicará, mediante porcentaje, que los costos de diciembre (?P<comparacion_por_mes>.+) a los costos de noviembre")
def step_impl(context, comparacion_por_mes):
    pass


@step("el vendedor estableció (?P<meta_beneficio>.+) dolares como la meta de beneficio por venta para diciembre")
def step_impl(context, meta_beneficio):
    pass


@step("se mostrarán (?P<beneficio>.+) dolares de beneficio por venta")
def step_impl(context, beneficio):
    pass


@step(
    "se indicará, mediante porcentaje, que los beneficio por venta de diciembre (?P<comparacion_por_meta>.+) a la meta de los beneficios por venta de diciembre")
def step_impl(context, comparacion_por_meta):
    pass


@step(
    "se indicará, mediante porcentaje, que los beneficio por venta de diciembre (?P<comparacion_por_mes>.+) a los beneficios por venta de noviembre")
def step_impl(context, comparacion_por_mes):
    pass
