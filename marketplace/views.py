from django.http import HttpResponse
from django.shortcuts import render
from marketplace.models import Producto


# from marketplace.models import Producto


# Create your views here.


def index(request):
    return render(request, 'index.html', context={"productos_destacados": []})


def buscar_producto(request):
    query = request.GET.get('q', '')
    productos = Producto.objects.filter(nombre__icontains=query).order_by('-promocion')
    return render(request, 'plantilla_hija_ejemplo.html', {'productos': productos, 'query': query})
