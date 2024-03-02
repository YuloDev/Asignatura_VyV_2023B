from django.shortcuts import render


# Create your views here.


def index(request):
    return render(request, 'plantilla_hija_ejemplo.html')


def feedback(request):
    causas = ["Mal estado"]
    porcentajes_calculados = ["70", "0", "5", "100", "15"]
    estrellas = [1, 2, 3, 4, 5]
    return render(request, 'feedback.html', {'causas': causas,
                                             'porcentajes_calculados': porcentajes_calculados, 'num_estrella_calculada': 5,
                                             'estrellas': estrellas, 'nombre_producto': "Producto 1"})
