from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse
from .models import Pedido


# Create your views here.


def index(request):
    return render(request, 'plantilla_hija_ejemplo.html')

def seguimiento_entrega(request):
    pedidos_listos_para_entregar = Pedido.objects.filter(etapa_pedido=Pedido.LISTO_PARA_ENTREGAR)
    cantidad_pedidos = pedidos_listos_para_entregar.count()

    # De los pedidos listos, contar cuántos están a tiempo y cuántos están atrasados
    pedidos_a_tiempo = pedidos_listos_para_entregar.filter(estado_pedido=Pedido.A_TIEMPO).count()
    pedidos_atrasados = pedidos_listos_para_entregar.filter(estado_pedido=Pedido.ATRASADO).count()

    context = {
        'pedidos_a_tiempo': pedidos_a_tiempo,
        'pedidos_atrasados': pedidos_atrasados,
        'cantidad_pedidos': cantidad_pedidos,
    }

    return render(request, 'dashboard_listo_para_entregar.html', context)
    return render(request, 'seguimiento_entrega.html')

