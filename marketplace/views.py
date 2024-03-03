from django.shortcuts import render, get_object_or_404
from .models import *


# Create your views here.


def index(request):
    return render(request, 'plantilla_hija_ejemplo.html')


def metricas(request, vendedor_id):
    
    anio = 2023
    mes = 12

    vendedor = get_object_or_404(Vendedor, pk=vendedor_id)

    reporte = vendedor.generar_reporte(anio, mes)

    recomendaciones = reporte.obtener_recomendaciones()

    numero_ventas = reporte.obtener_metrica(TipoDeMetrica.NUMERO_DE_VENTAS).valor
    ingresos = reporte.obtener_metrica(TipoDeMetrica.INGRESOS).valor
    costos = reporte.obtener_metrica(TipoDeMetrica.COSTOS).valor
    beneficio_venta = reporte.obtener_metrica(TipoDeMetrica.BENEFICIO_POR_VENTA).valor

    nv_porcentaje = reporte.obtener_porcentaje_de_avance(TipoDeMetrica.NUMERO_DE_VENTAS)
    is_porcentaje = reporte.obtener_porcentaje_de_avance(TipoDeMetrica.INGRESOS)
    cs_porcentaje = reporte.obtener_porcentaje_de_avance(TipoDeMetrica.COSTOS)
    bv_porcentaje = reporte.obtener_porcentaje_de_avance(TipoDeMetrica.BENEFICIO_POR_VENTA)

    nv_comparacion_meta = reporte.obtener_comparacion_por_meta(TipoDeMetrica.NUMERO_DE_VENTAS)
    is_comparacion_meta = reporte.obtener_comparacion_por_meta(TipoDeMetrica.INGRESOS)
    cs_comparacion_meta = reporte.obtener_comparacion_por_meta(TipoDeMetrica.COSTOS)
    bv_comparacion_meta = reporte.obtener_comparacion_por_meta(TipoDeMetrica.BENEFICIO_POR_VENTA)

    nv_comparacion_mes_anterior = reporte.obtener_comparacion_por_mes_anterior(TipoDeMetrica.NUMERO_DE_VENTAS)
    is_comparacion_mes_anterior = reporte.obtener_comparacion_por_mes_anterior(TipoDeMetrica.INGRESOS)
    cs_comparacion_mes_anterior = reporte.obtener_comparacion_por_mes_anterior(TipoDeMetrica.COSTOS)
    bv_comparacion_mes_anterior = reporte.obtener_comparacion_por_mes_anterior(TipoDeMetrica.BENEFICIO_POR_VENTA)

    nv_valor_mes_anterior = reporte.obtener_metrica_mes_anterior(TipoDeMetrica.NUMERO_DE_VENTAS).valor
    is_valor_mes_anterior = reporte.obtener_metrica_mes_anterior(TipoDeMetrica.INGRESOS).valor
    cs_valor_mes_anterior = reporte.obtener_metrica_mes_anterior(TipoDeMetrica.COSTOS).valor
    bv_valor_mes_anterior = reporte.obtener_metrica_mes_anterior(TipoDeMetrica.BENEFICIO_POR_VENTA).valor

    context = {
        'recomendaciones': recomendaciones,
        'numero_ventas': numero_ventas,
        'ingresos': ingresos,
        'costos': costos,
        'beneficio_venta': beneficio_venta,
        'nv_porcentaje': nv_porcentaje,
        'is_porcentaje': is_porcentaje,
        'cs_porcentaje': cs_porcentaje,
        'bv_porcentaje': bv_porcentaje,
        'nv_comparacion_meta': nv_comparacion_meta,
        'is_comparacion_meta': is_comparacion_meta,
        'cs_comparacion_meta': cs_comparacion_meta,
        'bv_comparacion_meta': bv_comparacion_meta,
        'nv_comparacion_mes_anterior': nv_comparacion_mes_anterior,
        'is_comparacion_mes_anterior': is_comparacion_mes_anterior,
        'cs_comparacion_mes_anterior': cs_comparacion_mes_anterior,
        'bv_comparacion_mes_anterior': bv_comparacion_mes_anterior,
        'nv_valor_mes_anterior': nv_valor_mes_anterior,
        'is_valor_mes_anterior': is_valor_mes_anterior,
        'cs_valor_mes_anterior': cs_valor_mes_anterior,
        'bv_valor_mes_anterior': bv_valor_mes_anterior
    }

    return render(request, 'metrica.html', context)
