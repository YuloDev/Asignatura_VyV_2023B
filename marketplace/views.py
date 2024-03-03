from django.shortcuts import render

from marketplace.models import *


# Create your views here.


def index(request):
    return render(request, 'plantilla_hija_ejemplo.html')


def seguimiento_interno(request):
    # Obtener todos los pedidos de la base de datos
    pedidos = Pedido.objects.all()

    # Iterar sobre cada pedido y llamar al método cambiar_estado
    for pedido in pedidos:
        pedido.cambiar_estado()

    # Total pedidos del vendedor 1
    total_pedidos_vendedor = Pedido.total_pedidos_vendedor(1)

    # Obtener los totales y conteos por etapa
    total_pedidos_precompra, precompra_atrasados, precompra_a_tiempo, precompra_cancelados = Pedido.sumar_y_contar_por_etapa(
        Pedido.PRECOMPRA, 1)
    total_pedidos_reserva, reserva_atrasados, reserva_a_tiempo, reserva_cancelados = Pedido.sumar_y_contar_por_etapa(
        Pedido.RESERVA, 1)
    total_pedidos_listo_para_entregar, listo_para_entregar_atrasados, listo_para_entregar_a_tiempo, listo_para_entregar_cancelados = Pedido.sumar_y_contar_por_etapa(
        Pedido.LISTO_PARA_ENTREGAR, 1)

    context = {
        'total_pedidos_vendedor': total_pedidos_vendedor,
        'total_pedidos_precompra': total_pedidos_precompra,
        'total_pedidos_reserva': total_pedidos_reserva,
        'total_pedidos_listo_para_entregar': total_pedidos_listo_para_entregar,
        'precompra_a_tiempo': precompra_a_tiempo,
        'precompra_atrasados': precompra_atrasados,
        'precompra_cancelados': precompra_cancelados,
        'reserva_a_tiempo': reserva_a_tiempo,
        'reserva_atrasados': reserva_atrasados,
        'reserva_cancelados': reserva_cancelados,
        'listo_para_entregar_a_tiempo': listo_para_entregar_a_tiempo,
        'listo_para_entregar_atrasados': listo_para_entregar_atrasados,
        'listo_para_entregar_cancelados': listo_para_entregar_cancelados
    }
    return render(request, 'seguimiento_interno.html', context)