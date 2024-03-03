from django.http import HttpResponse
from django.shortcuts import render
from .models import Servicio, Pedido, Vendedor, Calificacion


# Create your views here.


def index(request):
    return render(request, 'plantilla_hija_ejemplo.html')


def feedback(request):
    causas = dict()
    porcentajes_calculados = list()
    calificaciones_recibidas = list()
    estrellas = [1, 2, 3, 4, 5]
    num_estrella_calculada = 0
    if request.method == 'POST':
        if request.POST.get('opcion') == 'Servicio':
            servicio = Servicio.objects.filter(vendedor_id=1).first()
            calificaciones_recibidas = Calificacion.objects.filter(id_servicio_id=servicio.id)
            porcentajes_calculados = servicio.obtener_porcentajes_de_calificaciones()
            causas_dict = servicio.obtener_causas_de_cada_estrella(calificaciones_recibidas)
            causas = list(causas_dict.values())
            print(causas)
            num_estrella_calculada = servicio.obtener_promedio_general_del_servicio()
            return render(request, 'feedback.html', {
                'causas': causas,
                'porcentajes_calculados': porcentajes_calculados,
                'num_estrella_calculada': num_estrella_calculada,
                'estrellas': estrellas,
                'nombre': request.POST.get('opcion')
            })
        else:

            return render(request, 'feedback.html', {
                'causas': causas,
                'porcentajes_calculados': porcentajes_calculados,
                'num_estrella_calculada': num_estrella_calculada,
                'estrellas': estrellas,
                'nombre': request.POST.get('nombre_producto')
            })
    else:
        # Si la solicitud no es POST, renderizar la plantilla de formulario vacía
        return render(request, 'feedback.html')
