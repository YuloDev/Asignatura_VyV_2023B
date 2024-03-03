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

def seguimiento_entrega(request, vendedor_id):

    vendedor = Vendedor.objects.get(id=vendedor_id)
    todos_los_pedidos = vendedor.listar_pedidos()

    for pedido in todos_los_pedidos:
        pedido.actualizar_estado_pedido(anios=0, meses=0, semanas=0, dias=0)

    numero_pedidos_totales = vendedor.total_pedidos_vendedor()
    numero_pedidos_totales_a_tiempo = vendedor.contar_pedidos_por_estado(Pedido.A_TIEMPO)
    numero_pedidos_totales_atrasado = vendedor.contar_pedidos_por_estado(Pedido.ATRASADO)
    numero_pedidos_totales_cliente_no_encotrado = vendedor.contar_pedidos_por_estado(Pedido.ATRASADO)

    numero_pedidos_listo_para_entregar_totales = vendedor.contar_pedidos_por_etapa(Pedido.LISTO_PARA_ENTREGAR)
    numero_pedidos_listo_para_entregar_a_tiempo = vendedor.contar_pedidos_por_estado_en_etapa(
        Pedido.LISTO_PARA_ENTREGAR, Pedido.A_TIEMPO)
    numero_pedidos_listo_para_entregar_atrasado = vendedor.contar_pedidos_por_estado_en_etapa(
        Pedido.LISTO_PARA_ENTREGAR, Pedido.ATRASADO)

    numero_pedidos_repartidor_asignado_totales = vendedor.contar_pedidos_por_etapa(Pedido.REPARTIDOR_ASIGNADO)
    numero_pedidos_repartidor_asignadio_a_tiempo = vendedor.contar_pedidos_por_estado_en_etapa(
        Pedido.REPARTIDOR_ASIGNADO, Pedido.A_TIEMPO)
    numero_pedidos_repartidor_asignadio_atrasado = vendedor.contar_pedidos_por_estado_en_etapa(
        Pedido.REPARTIDOR_ASIGNADO, Pedido.ATRASADO)

    numero_pedidos_embarcado_totales = vendedor.contar_pedidos_por_etapa(Pedido.EMBARCADO)
    numero_pedidos_embarcado_a_tiempo = vendedor.contar_pedidos_por_estado_en_etapa(Pedido.EMBARCADO, Pedido.A_TIEMPO)
    numero_pedidos_embarcado_atrasado = vendedor.contar_pedidos_por_estado_en_etapa(Pedido.EMBARCADO, Pedido.ATRASADO)

    numero_pedidos_paquete_no_entregado_totales = vendedor.contar_pedidos_por_etapa(Pedido.PAQUETE_NO_ENTREGADO)
    numero_pedidos_paquete_no_entregado_a_tiempo = vendedor.contar_pedidos_por_estado_en_etapa(
        Pedido.PAQUETE_NO_ENTREGADO, Pedido.A_TIEMPO)
    numero_pedidos_paquete_no_entregado_atrasado = vendedor.contar_pedidos_por_estado_en_etapa(
        Pedido.PAQUETE_NO_ENTREGADO, Pedido.ATRASADO)
    numero_pedidos_paquete_no_entregado_cliente_no_encontrado = vendedor.contar_pedidos_por_estado_en_etapa(
        Pedido.PAQUETE_NO_ENTREGADO, Pedido.CLIENTE_NO_ENCONTRADO)

    numero_pedidos_paquete_entregado_totales = vendedor.contar_pedidos_por_etapa(Pedido.PAQUETE_ENTREGADO)
    numero_pedidos_paquete_entregado_a_tiempo = vendedor.contar_pedidos_por_estado_en_etapa(
        Pedido.PAQUETE_ENTREGADO, Pedido.A_TIEMPO)
    numero_pedidos_paquete_entregado_atrasado = vendedor.contar_pedidos_por_estado_en_etapa(
        Pedido.PAQUETE_ENTREGADO, Pedido.ATRASADO)

    context = {
        'numero_pedidos_totales': numero_pedidos_totales,
        'numero_pedidos_totales_a_tiempo': numero_pedidos_totales_a_tiempo,
        'numero_pedidos_totales_atrasado': numero_pedidos_totales_atrasado,
        'numero_pedidos_totales_cliente_no_encotrado' : numero_pedidos_totales_cliente_no_encotrado,
        'numero_pedidos_listo_para_entregar_a_tiempo' : numero_pedidos_listo_para_entregar_a_tiempo,
        'numero_pedidos_listo_para_entregar_atrasado': numero_pedidos_listo_para_entregar_atrasado,
        'numero_pedidos_listo_para_entregar_totales': numero_pedidos_listo_para_entregar_totales,
        'numero_pedidos_repartidor_asignado_totales': numero_pedidos_repartidor_asignado_totales,
        'numero_pedidos_repartidor_asignadio_a_tiempo': numero_pedidos_repartidor_asignadio_a_tiempo,
        'numero_pedidos_repartidor_asignadio_atrasado': numero_pedidos_repartidor_asignadio_atrasado,
        'numero_pedidos_embarcado_totales': numero_pedidos_embarcado_totales,
        'numero_pedidos_embarcado_a_tiempo': numero_pedidos_embarcado_a_tiempo,
        'numero_pedidos_embarcado_atrasado': numero_pedidos_embarcado_atrasado,
        'numero_pedidos_paquete_no_entregado_totales': numero_pedidos_paquete_no_entregado_totales,
        'numero_pedidos_paquete_no_entregado_a_tiempo': numero_pedidos_paquete_no_entregado_a_tiempo,
        'numero_pedidos_paquete_no_entregado_atrasado': numero_pedidos_paquete_no_entregado_atrasado,
        'numero_pedidos_paquete_no_entregado_cliente_no_encontrado': numero_pedidos_paquete_no_entregado_cliente_no_encontrado,
        'numero_pedidos_paquete_entregado_totales': numero_pedidos_paquete_entregado_totales,
        'numero_pedidos_paquete_entregado_a_tiempo': numero_pedidos_paquete_entregado_a_tiempo,
        'numero_pedidos_paquete_entregado_atrasado': numero_pedidos_paquete_entregado_atrasado
    }

    return render(request, 'seguimiento_entrega.html', context)

