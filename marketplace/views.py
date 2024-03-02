from django.shortcuts import render
from .models import MetaG3, MetricaG3, Pedido_ProductoG3
from datetime import datetime, timedelta
from django.db.models import Sum


# Create your views here.


def index(request):
    return render(request, 'plantilla_hija_ejemplo.html')


def metricas(request):
    # Obtener el vendedor actual (supongamos que está autenticado)
    vendedor_id = 1  # Esto debe ser el ID del vendedor actual
    # Obtener la fecha actual
    fecha_actual = datetime(2023,12,31)
    # Calcular el mes anterior
    mes_anterior = fecha_actual.month - 1 if fecha_actual.month > 1 else 12
    # Calcular el año del mes anterior
    anio_anterior = fecha_actual.year if fecha_actual.month > 1 else fecha_actual.year - 1

    # Calcular el costo total de los productos vendidos en el mes actual
    costo_mes_actual = Pedido_ProductoG3.objects.filter(pedido__fecha_listo_para_entregar__year=fecha_actual.year,
                                                        pedido__fecha_listo_para_entregar__month=fecha_actual.month,
                                                        pedido__vendedor_id=vendedor_id).aggregate(
        Sum('producto__costo'))['producto__costo__sum'] or 0

    # Calcular el costo total de los productos vendidos en el mes anterior
    costo_mes_anterior = Pedido_ProductoG3.objects.filter(pedido__fecha_listo_para_entregar__year=anio_anterior,
                                                          pedido__fecha_listo_para_entregar__month=mes_anterior,
                                                          pedido__vendedor_id=vendedor_id).aggregate(
        Sum('producto__costo'))['producto__costo__sum'] or 0

    # Obtener la meta de costo para el mes actual
    meta_costo = MetaG3.objects.filter(tipo_de_metrica='Costos', anio=fecha_actual.year, mes=fecha_actual.month,
                                       vendedor_id=vendedor_id).first()

    # Calcular la diferencia entre el costo del mes actual y el costo del mes anterior
    diferencia_costo_mes_anterior = costo_mes_actual - costo_mes_anterior

    # Si hay una meta de costo para el mes actual, calcular si se ha superado
    superado = None
    if meta_costo:
        superado = costo_mes_actual > meta_costo.valor

    # Guardar la métrica de costo en la base de datos
    metrica_costo = MetricaG3.objects.create(tipo_de_metrica='Costo', valor=costo_mes_actual, anio=fecha_actual.year,
                                             mes=fecha_actual.month, vendedor_id=vendedor_id)

    # Enviar los datos al HTML
    context = {
        'costo_mes_actual': costo_mes_actual,
        'costo_mes_anterior': costo_mes_anterior,
        'diferencia_costo_mes_anterior': diferencia_costo_mes_anterior,
        'superado': superado,
    }

    return render(request, 'metrica.html', context)
