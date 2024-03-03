from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse
from .models import Pedido


# Create your views here.


def index(request):
    return render(request, 'plantilla_hija_ejemplo.html')

def seguimiento_entrega(request, vendedor_id):

    pedidos_todos_los_pedidos = Pedido.objects.filter(vendedor_id=vendedor_id)
    for pedido in pedidos_todos_los_pedidos:
        pedido.actualizar_estado_pedido(anios=0, meses=0, semanas=0, dias=0)

    numero_pedidos_totales = pedidos_todos_los_pedidos.count()
    numero_pedidos_totales_a_tiempo = pedidos_todos_los_pedidos.filter(estado_pedido=Pedido.A_TIEMPO).count()
    numero_pedidos_totales_atrasado = pedidos_todos_los_pedidos.filter(estado_pedido=Pedido.ATRASADO).count()
    numero_pedidos_totales_cliente_no_encotrado = pedidos_todos_los_pedidos.filter(estado_pedido=Pedido.CLIENTE_NO_ENCONTRADO).count()

    numero_pedidos_listo_para_entregar_totales = pedidos_todos_los_pedidos.filter(etapa_pedido=Pedido.LISTO_PARA_ENTREGAR).count()
    numero_pedidos_listo_para_entregar_a_tiempo = pedidos_todos_los_pedidos.filter(estado_pedido=Pedido.A_TIEMPO, etapa_pedido=Pedido.LISTO_PARA_ENTREGAR).count()
    numero_pedidos_listo_para_entregar_atrasado = pedidos_todos_los_pedidos.filter(estado_pedido=Pedido.ATRASADO, etapa_pedido=Pedido.LISTO_PARA_ENTREGAR).count()

    numero_pedidos_repartidor_asignado_totales = pedidos_todos_los_pedidos.filter(etapa_pedido=Pedido.REPARTIDOR_ASIGNADO).count()
    numero_pedidos_repartidor_asignadio_a_tiempo = pedidos_todos_los_pedidos.filter(estado_pedido=Pedido.A_TIEMPO,
                                                                                   etapa_pedido=Pedido.REPARTIDOR_ASIGNADO).count()
    numero_pedidos_repartidor_asignadio_atrasado = pedidos_todos_los_pedidos.filter(estado_pedido=Pedido.ATRASADO,
                                                                                   etapa_pedido=Pedido.REPARTIDOR_ASIGNADO).count()
    numero_pedidos_embarcado_totales = pedidos_todos_los_pedidos.filter(
        etapa_pedido=Pedido.EMBARCADO).count()
    numero_pedidos_embarcado_a_tiempo = pedidos_todos_los_pedidos.filter(estado_pedido=Pedido.A_TIEMPO,
                                                                                    etapa_pedido=Pedido.EMBARCADO).count()
    numero_pedidos_embarcado_atrasado = pedidos_todos_los_pedidos.filter(estado_pedido=Pedido.ATRASADO,
                                                                                    etapa_pedido=Pedido.EMBARCADO).count()

    numero_pedidos_paquete_no_entregado_totales = pedidos_todos_los_pedidos.filter(
        etapa_pedido=Pedido.PAQUETE_NO_ENTREGADO).count()
    numero_pedidos_paquete_no_entregado_a_tiempo = pedidos_todos_los_pedidos.filter(estado_pedido=Pedido.A_TIEMPO,
                                                                         etapa_pedido=Pedido.PAQUETE_NO_ENTREGADO).count()
    numero_pedidos_paquete_no_entregado_atrasado = pedidos_todos_los_pedidos.filter(estado_pedido=Pedido.ATRASADO,
                                                                         etapa_pedido=Pedido.PAQUETE_NO_ENTREGADO).count()
    numero_pedidos_paquete_no_entregado_cliente_no_encontrado = pedidos_todos_los_pedidos.filter(estado_pedido=Pedido.CLIENTE_NO_ENCONTRADO,
                                                                                    etapa_pedido=Pedido.PAQUETE_NO_ENTREGADO).count()
    numero_pedidos_paquete_entregado_totales = pedidos_todos_los_pedidos.filter(
        etapa_pedido=Pedido.PAQUETE_ENTREGADO).count()
    numero_pedidos_paquete_entregado_a_tiempo = pedidos_todos_los_pedidos.filter(
        estado_pedido=Pedido.A_TIEMPO,
        etapa_pedido=Pedido.PAQUETE_ENTREGADO).count()
    numero_pedidos_paquete_entregado_atrasado = pedidos_todos_los_pedidos.filter(estado_pedido=Pedido.ATRASADO,
                                                                                    etapa_pedido=Pedido.PAQUETE_ENTREGADO).count()

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

