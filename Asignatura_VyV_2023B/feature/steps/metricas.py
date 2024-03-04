import django

django.setup()
from behave import *
from faker import Faker
from datetime import date
from marketplace.models import *

use_step_matcher("re")


@step(
    "que un vendedor realizó (?P<ventas_mes_actual>.+) ventas en el mes actual, diciembre, de productos cuyo costo y precio fueron (?P<costo_mes_actual>.+) y (?P<precio_mes_actual>.+), respectivamente, y (?P<ventas_mes_anterior>.+) ventas en el mes anterior de productos cuyo costo y precio fueron (?P<costo_mes_anterior>.+) y (?P<precio_mes_anterior>.+), respectivamente")
def step_impl(context, ventas_mes_actual, costo_mes_actual, precio_mes_actual, ventas_mes_anterior, costo_mes_anterior, precio_mes_anterior):
    faker = Faker()
    vendedor, _ = Vendedor.objects.get_or_create(
        nombre=faker.name()
    )
    context.vendedor = vendedor

    context.producto_de_mes_actual, _ = Producto.objects.get_or_create(nombre="Pepsi",
                                                                       precio=float(precio_mes_actual),
                                                                       costo=float(costo_mes_actual),
                                                                       vendedor=context.vendedor)
    context.producto_de_mes_anterior, _ = Producto.objects.get_or_create(nombre="Pepsi",
                                                                         precio=float(precio_mes_anterior),
                                                                         costo=float(costo_mes_anterior),
                                                                         vendedor=context.vendedor)
    context.anio = 2023
    context.mes_actual = 12
    context.mes_anterior = 11

    for _ in range(int(ventas_mes_actual)):
        context.pedido = context.vendedor.pedidos.create(
            fecha_listo_para_entregar=date(context.anio, context.mes_actual, 1))
        context.pedido.detalles.get_or_create(producto=context.producto_de_mes_actual, cantidad=1)
    for _ in range(int(ventas_mes_anterior)):
        context.pedido = context.vendedor.pedidos.create(
            fecha_listo_para_entregar=date(context.anio, context.mes_anterior, 1))
        context.pedido.detalles.get_or_create(producto=context.producto_de_mes_anterior,
                                              cantidad=1)

    assert (context.vendedor.obtener_cantidad_de_ventas_por_fecha(context.anio, context.mes_actual) == int(ventas_mes_actual) and
            context.vendedor.obtener_cantidad_de_ventas_por_fecha(context.anio, context.mes_anterior) == int(ventas_mes_anterior))


@step("el vendedor estableció como meta de número de ventas para el mes actual el valor (?P<meta_ventas>.+)")
def step_impl(context, meta_ventas):
    context.meta, _ = Meta.objects.get_or_create(tipo_de_metrica=TipoDeMetrica.NUMERO_DE_VENTAS, valor=meta_ventas, anio=context.anio, mes=context.mes_actual, vendedor=context.vendedor)
    context.vendedor.establecer_meta(context.meta)
    assert (context.vendedor.obtener_meta(TipoDeMetrica.NUMERO_DE_VENTAS, context.anio, context.mes_actual).obtener_valor() == float(
        meta_ventas))


@step("se genera el Reporte de métricas")
def step_impl(context):
    context.reporte = context.vendedor.generar_reporte(context.anio, context.mes_actual)
    assert (context.reporte is not None)


@step("se mostrarán (?P<ventas>.+) ventas")
def step_impl(context, ventas):
    assert (context.reporte.obtener_metrica(TipoDeMetrica.NUMERO_DE_VENTAS).obtener_valor() == float(ventas))


@step(
    "se indicará que las ventas del mes actual (?P<comparacion_por_meta>.+) a la meta de ventas del mes actual, con el porcentaje de avance (?P<porcentaje>.+)%")
def step_impl(context, comparacion_por_meta, porcentaje):
    assert (context.reporte.obtener_comparacion_por_meta(TipoDeMetrica.NUMERO_DE_VENTAS) == comparacion_por_meta
            and context.reporte.obtener_porcentaje_de_avance(TipoDeMetrica.NUMERO_DE_VENTAS) == int(porcentaje))


@step(
    "se indicará que las ventas del mes actual (?P<comparacion_por_mes>.+) a las ventas del mes anterior")
def step_impl(context, comparacion_por_mes):
    assert (context.reporte.obtener_comparacion_por_mes_anterior(TipoDeMetrica.NUMERO_DE_VENTAS) == comparacion_por_mes)


@step("se recomendará (?P<recomendacion>.+)")
def step_impl(context, recomendacion):
    assert (recomendacion in context.reporte.obtener_recomendaciones())


@step("el vendedor estableció como meta de ingresos para el mes actual la cantidad de (?P<meta_ingresos>.+) dólares")
def step_impl(context, meta_ingresos):
    context.meta, _ = Meta.objects.get_or_create(tipo_de_metrica=TipoDeMetrica.INGRESOS, valor=meta_ingresos,
                                                 anio=context.anio, mes=context.mes_actual, vendedor=context.vendedor)
    context.vendedor.establecer_meta(context.meta)
    assert (context.vendedor.obtener_meta(TipoDeMetrica.INGRESOS, context.anio, context.mes_actual).obtener_valor() == float(
        meta_ingresos))


@step("se mostrarán (?P<ingresos>.+) dólares de ingresos")
def step_impl(context, ingresos):
    assert (context.reporte.obtener_metrica(TipoDeMetrica.INGRESOS).obtener_valor() == float(ingresos))


@step(
    "se indicará que los ingresos del mes actual (?P<comparacion_por_meta>.+) a la meta de ingresos del mes actual, con el porcentaje de avance (?P<porcentaje>.+)%")
def step_impl(context, comparacion_por_meta, porcentaje):
    assert (context.reporte.obtener_comparacion_por_meta(TipoDeMetrica.INGRESOS) == comparacion_por_meta
            and context.reporte.obtener_porcentaje_de_avance(TipoDeMetrica.INGRESOS) == int(porcentaje))


@step("se indicará que los ingresos del mes actual (?P<comparacion_por_mes>.+) a los ingresos del mes anterior")
def step_impl(context, comparacion_por_mes):
    assert (context.reporte.obtener_comparacion_por_mes_anterior(TipoDeMetrica.INGRESOS) == comparacion_por_mes)


@step("el vendedor estableció como la meta de costos para el mes actual la cantidad de (?P<meta_costos>.+) dólares")
def step_impl(context, meta_costos):
    context.meta, _ = Meta.objects.get_or_create(tipo_de_metrica=TipoDeMetrica.COSTOS, valor=meta_costos,
                                                 anio=context.anio, mes=context.mes_actual, vendedor=context.vendedor)
    context.vendedor.establecer_meta(context.meta)
    assert (context.vendedor.obtener_meta(TipoDeMetrica.COSTOS, context.anio, context.mes_actual).obtener_valor() == float(
        meta_costos))


@step("se mostrarán (?P<costos>.+) dólares de costos")
def step_impl(context, costos):
    assert (context.reporte.obtener_metrica(TipoDeMetrica.COSTOS).obtener_valor() == float(costos))


@step(
    "se indicará que los costos del mes actual (?P<comparacion_por_meta>.+) a la meta de costos del mes actual, con el porcentaje de avance (?P<porcentaje>.+)%")
def step_impl(context, comparacion_por_meta, porcentaje):
    assert (context.reporte.obtener_comparacion_por_meta(TipoDeMetrica.COSTOS) == comparacion_por_meta
            and context.reporte.obtener_porcentaje_de_avance(TipoDeMetrica.COSTOS) == int(porcentaje))



@step("se indicará que los costos del mes actual (?P<comparacion_por_mes>.+) a los costos del mes anterior")
def step_impl(context, comparacion_por_mes):
    assert (context.reporte.obtener_comparacion_por_mes_anterior(TipoDeMetrica.COSTOS) == comparacion_por_mes)


@step(
    "el vendedor estableció como meta de beneficio por venta para el mes actual la cantidad de (?P<meta_beneficio>.+) dólares")
def step_impl(context, meta_beneficio):
    context.meta, _ = Meta.objects.get_or_create(tipo_de_metrica=TipoDeMetrica.BENEFICIO_POR_VENTA, valor=meta_beneficio,
                                                 anio=context.anio, mes=context.mes_actual, vendedor=context.vendedor)
    context.vendedor.establecer_meta(context.meta)
    assert (context.vendedor.obtener_meta(TipoDeMetrica.BENEFICIO_POR_VENTA, context.anio, context.mes_actual).obtener_valor() == float(meta_beneficio))


@step("se mostrarán (?P<beneficio>.+) dólares de beneficio por venta")
def step_impl(context, beneficio):
    assert (context.reporte.obtener_metrica(TipoDeMetrica.BENEFICIO_POR_VENTA).obtener_valor() == float(beneficio))


@step(
    "se indicará que los beneficio por venta del mes actual (?P<comparacion_por_meta>.+) a la meta de los beneficios por venta del mes actual, con el porcentaje de avance (?P<porcentaje>.+)%")
def step_impl(context, comparacion_por_meta, porcentaje):
    assert (context.reporte.obtener_comparacion_por_meta(TipoDeMetrica.BENEFICIO_POR_VENTA) == comparacion_por_meta
            and context.reporte.obtener_porcentaje_de_avance(TipoDeMetrica.BENEFICIO_POR_VENTA) == int(porcentaje))


@step(
    "se indicará que los beneficio por venta del mes actual (?P<comparacion_por_mes>.+) a los beneficios por venta del mes anterior")
def step_impl(context, comparacion_por_mes):
    assert (context.reporte.obtener_comparacion_por_mes_anterior(TipoDeMetrica.BENEFICIO_POR_VENTA) == comparacion_por_mes)
