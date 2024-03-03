from behave import *
from modelos.modelos import *

use_step_matcher("re")


@step(
    "que un vendedor realizó (?P<ventas_mes_actual>.+) ventas en el mes actual, diciembre, de productos cuyo costo y precio fueron (?P<costo_mes_actual>.+) y (?P<precio_mes_actual>.+), respectivamente, y (?P<ventas_mes_anterior>.+) ventas en el mes anterior de productos cuyo costo y precio fueron (?P<costo_mes_anterior>.+) y (?P<precio_mes_anterior>.+), respectivamente")
def step_impl(context, ventas_mes_actual, costo_mes_actual, precio_mes_actual, ventas_mes_anterior, costo_mes_anterior, precio_mes_anterior):
    context.vendedor = Vendedor("Nombre")
    context.producto_de_mes_actual = Producto("Nombre", float(precio_mes_actual), float(costo_mes_actual))
    context.producto_de_mes_anterior = Producto("Nombre", float(precio_mes_anterior), float(costo_mes_anterior))
    context.anio = 2023
    context.mes_actual = 12
    context.mes_anterior = 11

    for _ in range(int(ventas_mes_actual)):
        context.vendedor.vender([context.producto_de_mes_actual], context.anio, context.mes_actual, 1)
    for _ in range(int(ventas_mes_anterior)):
        context.vendedor.vender([context.producto_de_mes_anterior], context.anio, context.mes_anterior, 1)

    assert (context.vendedor.obtener_cantidad_de_ventas_por_fecha(context.anio, context.mes_actual) == int(ventas_mes_actual) and
            context.vendedor.obtener_cantidad_de_ventas_por_fecha(context.anio, context.mes_anterior) == int(ventas_mes_anterior))


@step("el vendedor estableció como meta de número de ventas para el mes actual el valor (?P<meta_ventas>.+)")
def step_impl(context, meta_ventas):
    context.vendedor.establecer_meta(
        Meta(TipoDeMetrica.NUMERO_DE_VENTAS, int(meta_ventas), context.anio, context.mes_actual))
    assert (context.vendedor.obtener_meta(TipoDeMetrica.NUMERO_DE_VENTAS, context.anio, context.mes_actual) == int(
        meta_ventas))


@step("se despliegue el Dashboard de Métricas")
def step_impl(context):
    context.dashboard = DashboardDeMetricas(context.vendedor)
    context.dashboard.generar_metricas(context.anio, context.mes_actual)
    assert (context.dashboard.se_realizaron_metricas() == True)


@step("se mostrarán (?P<ventas>.+) ventas")
def step_impl(context, ventas):
    assert (context.dashboard.obtener_metrica(TipoDeMetrica.NUMERO_DE_VENTAS) == int(ventas))


@step(
    "se indicará que las ventas del mes actual (?P<comparacion_por_meta>.+) a la meta de ventas del mes actual, con el porcentaje de avance (?P<porcentaje>.+)%")
def step_impl(context, comparacion_por_meta, porcentaje):
    assert (context.dashboard.obtener_comparacion_por_meta(TipoDeMetrica.NUMERO_DE_VENTAS) == TipoDeComparacion(
        comparacion_por_meta) and context.dashboard.obtener_porcentaje_de_avance(TipoDeMetrica.NUMERO_DE_VENTAS) == int(porcentaje))


@step(
    "se indicará que las ventas del mes actual (?P<comparacion_por_mes>.+) a las ventas del mes anterior")
def step_impl(context, comparacion_por_mes):
    print(context.dashboard.obtener_comparacion_por_mes_anterior(TipoDeMetrica.NUMERO_DE_VENTAS))
    print(TipoDeComparacion(comparacion_por_mes))
    assert (context.dashboard.obtener_comparacion_por_mes_anterior(TipoDeMetrica.NUMERO_DE_VENTAS) == TipoDeComparacion(
        comparacion_por_mes))


@step("se recomendará (?P<recomendacion>.+)")
def step_impl(context, recomendacion):
    assert (Recomendacion(recomendacion) in context.dashboard.obtener_recomendaciones())


@step("el vendedor estableció como meta de ingresos para el mes actual la cantidad de (?P<meta_ingresos>.+) dólares")
def step_impl(context, meta_ingresos):
    context.vendedor.establecer_meta(Meta(TipoDeMetrica.INGRESOS, float(meta_ingresos), context.anio, context.mes_actual))
    assert (context.vendedor.obtener_meta(TipoDeMetrica.INGRESOS, context.anio, context.mes_actual) == float(meta_ingresos))


@step("se mostrarán (?P<ingresos>.+) dólares de ingresos")
def step_impl(context, ingresos):
    assert (context.dashboard.obtener_metrica(TipoDeMetrica.INGRESOS) == float(ingresos))


@step(
    "se indicará que los ingresos del mes actual (?P<comparacion_por_meta>.+) a la meta de ingresos del mes actual, con el porcentaje de avance (?P<porcentaje>.+)%")
def step_impl(context, comparacion_por_meta, porcentaje):
    assert (context.dashboard.obtener_comparacion_por_meta(TipoDeMetrica.INGRESOS) == TipoDeComparacion(
        comparacion_por_meta) and context.dashboard.obtener_porcentaje_de_avance(TipoDeMetrica.INGRESOS) == int(porcentaje))


@step("se indicará que los ingresos del mes actual (?P<comparacion_por_mes>.+) a los ingresos del mes anterior")
def step_impl(context, comparacion_por_mes):
    assert (context.dashboard.obtener_comparacion_por_mes_anterior(TipoDeMetrica.INGRESOS) == TipoDeComparacion(
        comparacion_por_mes))


@step("el vendedor estableció como la meta de costos para el mes actual la cantidad de (?P<meta_costos>.+) dólares")
def step_impl(context, meta_costos):
    context.vendedor.establecer_meta(Meta(TipoDeMetrica.COSTOS, float(meta_costos), context.anio, context.mes_actual))
    assert (context.vendedor.obtener_meta(TipoDeMetrica.COSTOS, context.anio, context.mes_actual) == float(meta_costos))


@step("se mostrarán (?P<costos>.+) dólares de costos")
def step_impl(context, costos):
    assert (context.dashboard.obtener_metrica(TipoDeMetrica.COSTOS) == float(costos))


@step(
    "se indicará que los costos del mes actual (?P<comparacion_por_meta>.+) a la meta de costos del mes actual, con el porcentaje de avance (?P<porcentaje>.+)%")
def step_impl(context, comparacion_por_meta, porcentaje):
    assert (context.dashboard.obtener_comparacion_por_meta(TipoDeMetrica.COSTOS) == TipoDeComparacion(
        comparacion_por_meta) and context.dashboard.obtener_porcentaje_de_avance(TipoDeMetrica.COSTOS) == int(porcentaje))


@step("se indicará que los costos del mes actual (?P<comparacion_por_mes>.+) a los costos del mes anterior")
def step_impl(context, comparacion_por_mes):
    assert (context.dashboard.obtener_comparacion_por_mes_anterior(TipoDeMetrica.COSTOS) == TipoDeComparacion(
        comparacion_por_mes))


@step(
    "el vendedor estableció como meta de beneficio por venta para el mes actual la cantidad de (?P<meta_beneficio>.+) dólares")
def step_impl(context, meta_beneficio):
    context.vendedor.establecer_meta(Meta(TipoDeMetrica.BENEFICIO_POR_VENTA, float(meta_beneficio), context.anio, context.mes_actual))
    assert (context.vendedor.obtener_meta(TipoDeMetrica.BENEFICIO_POR_VENTA, context.anio, context.mes_actual) == float(meta_beneficio))


@step("se mostrarán (?P<beneficio>.+) dólares de beneficio por venta")
def step_impl(context, beneficio):
    assert (context.dashboard.obtener_metrica(TipoDeMetrica.BENEFICIO_POR_VENTA) == float(beneficio))


@step(
    "se indicará que los beneficio por venta del mes actual (?P<comparacion_por_meta>.+) a la meta de los beneficios por venta del mes actual, con el porcentaje de avance (?P<porcentaje>.+)%")
def step_impl(context, comparacion_por_meta, porcentaje):
    assert (context.dashboard.obtener_comparacion_por_meta(TipoDeMetrica.BENEFICIO_POR_VENTA) == TipoDeComparacion(
        comparacion_por_meta) and context.dashboard.obtener_porcentaje_de_avance(TipoDeMetrica.BENEFICIO_POR_VENTA) == int(porcentaje))


@step(
    "se indicará que los beneficio por venta del mes actual (?P<comparacion_por_mes>.+) a los beneficios por venta del mes anterior")
def step_impl(context, comparacion_por_mes):
    assert (context.dashboard.obtener_comparacion_por_mes_anterior(
        TipoDeMetrica.BENEFICIO_POR_VENTA) == TipoDeComparacion(comparacion_por_mes))
