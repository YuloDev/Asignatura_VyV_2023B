from django.shortcuts import render


# Create your views here.


def index(request):
    return render(request, 'plantilla_hija_ejemplo.html')

def seguimiento_entrega(request):
    return render(request, 'seguimiento_entrega.html')