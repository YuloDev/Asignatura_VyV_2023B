from behave import *
from modelos.modelos import *

use_step_matcher("re")


@step("que un vendedor realizó (?P<ventas_de_diciembre>.+) ventas en diciembre y (?P<ventas_de_dnoviembre>.+) ventas en noviembre")
def step_impl(context, ventas_de_diciembre, ventas_de_noviembre):
    context.vendedor = Vendedor("nombre")
    for row in context.table:
        fecha = row["fecha"].split("-")
        lista_de_productos = [Producto(row["producto"], float(row["precio"]), float(row["costo"])) for _ in
                              range(int(row["cantidad"]))]
        context.vendedor.vender(lista_de_productos, int(fecha[0]), int(fecha[1]), int(fecha[2]))
    assert (len(context.vendedor.obtener_ventas()) == (int(ventas_de_diciembre)+int(ventas_de_noviembre)))


@step("el vendedor estableció como meta de número de ventas para diciembre el valor (?P<meta_ventas>.+)")
def step_impl(context, meta_ventas):
    context.vendedor.establecer_meta(Meta(TipoDeMetrica.NUMERO_DE_VENTAS, int(meta_ventas), 2023, 12))
    assert (context.vendedor.obtener_meta(TipoDeMetrica.NUMERO_DE_VENTAS, 2023, 12) == int(meta_ventas))


@step("se despliegue el Dashboard de Métricas en diciembre")
def step_impl(context):
    context.dashboard = Dashboard(context.vendedor)
    context.dashboard.generar_metricas(2023, 12)
    assert (context.dashboard.se_realizaron_metricas() == True)


@step("se mostrarán (?P<ventas>.+) ventas en diciembre")
def step_impl(context, ventas):
    assert (context.dashboard.obtener_metrica(TipoDeMetrica.NUMERO_DE_VENTAS) == int(ventas))


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
    assert (Recomendacion(recomendacion) in context.dashboard.obtener_recomendaciones())


@step("el vendedor estableció como meta de ingresos para diciembre la cantidad de (?P<meta_ingresos>.+) dólares")
def step_impl(context, meta_ingresos):
    context.vendedor.establecer_meta(Meta(TipoDeMetrica.INGRESOS, float(meta_ingresos), 2023, 12))
    assert (context.vendedor.obtener_meta(TipoDeMetrica.INGRESOS, 2023, 12) == float(meta_ingresos))


@step("se mostrarán (?P<ingresos>.+) dólares de ingresos en diciembre")
def step_impl(context, ingresos):
    assert (context.dashboard.obtener_metrica(TipoDeMetrica.INGRESOS) == float(ingresos))


@step(
    "se indicará, mediante porcentaje, que los ingresos de diciembre (?P<comparacion_por_meta>.+) a la meta de ingresos de diciembre")
def step_impl(context, comparacion_por_meta):
    assert (context.dashboard.obtener_comparacion_por_meta(TipoDeMetrica.INGRESOS) == TipoDeComparacion(
        comparacion_por_meta))


@step(
    "se indicará, mediante porcentaje, que los ingresos de diciembre (?P<comparacion_por_mes>.+) a los ingresos de noviembre")
def step_impl(context, comparacion_por_mes):
    assert (context.dashboard.obtener_comparacion_por_mes_anterior(TipoDeMetrica.INGRESOS) == TipoDeComparacion(
        comparacion_por_mes))


@step("el vendedor estableció como la meta de costos para diciembre la cantidad de (?P<meta_costos>.+) dólares")
def step_impl(context, meta_costos):
    context.vendedor.establecer_meta(Meta(TipoDeMetrica.COSTOS, float(meta_costos), 2023, 12))
    assert (context.vendedor.obtener_meta(TipoDeMetrica.COSTOS, 2023, 12) == float(meta_costos))


@step("se mostrarán (?P<costos>.+) dólares de costos en diciembre")
def step_impl(context, costos):
    assert (context.dashboard.obtener_metrica(TipoDeMetrica.COSTOS) == float(costos))


@step(
    "se indicará, mediante porcentaje, que los costos de diciembre (?P<comparacion_por_meta>.+) a la meta de costos de diciembre")
def step_impl(context, comparacion_por_meta):
    assert (context.dashboard.obtener_comparacion_por_meta(TipoDeMetrica.COSTOS) == TipoDeComparacion(
        comparacion_por_meta))


@step(
    "se indicará, mediante porcentaje, que los costos de diciembre (?P<comparacion_por_mes>.+) a los costos de noviembre")
def step_impl(context, comparacion_por_mes):
    assert (context.dashboard.obtener_comparacion_por_mes_anterior(TipoDeMetrica.COSTOS) == TipoDeComparacion(
        comparacion_por_mes))


@step("el vendedor estableció como meta de beneficio por venta para diciembre la cantidad de (?P<meta_beneficio>.+) dólares")
def step_impl(context, meta_beneficio):
    context.vendedor.establecer_meta(Meta(TipoDeMetrica.BENEFICIO_POR_VENTA, float(meta_beneficio), 2023, 12))
    assert (context.vendedor.obtener_meta(TipoDeMetrica.BENEFICIO_POR_VENTA, 2023, 12) == float(meta_beneficio))


@step("se mostrarán (?P<beneficio>.+) dólares de beneficio por venta en diciembre")
def step_impl(context, beneficio):
    assert (context.dashboard.obtener_metrica(TipoDeMetrica.BENEFICIO_POR_VENTA) == float(beneficio))


@step(
    "se indicará, mediante porcentaje, que los beneficio por venta de diciembre (?P<comparacion_por_meta>.+) a la meta de los beneficios por venta de diciembre")
def step_impl(context, comparacion_por_meta):
    assert (context.dashboard.obtener_comparacion_por_meta(TipoDeMetrica.BENEFICIO_POR_VENTA) == TipoDeComparacion(
        comparacion_por_meta))


@step(
    "se indicará, mediante porcentaje, que los beneficio por venta de diciembre (?P<comparacion_por_mes>.+) a los beneficios por venta de noviembre")
def step_impl(context, comparacion_por_mes):
    assert (context.dashboard.obtener_comparacion_por_mes_anterior(
        TipoDeMetrica.BENEFICIO_POR_VENTA) == TipoDeComparacion(comparacion_por_mes))
