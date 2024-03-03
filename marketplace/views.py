from django.http import HttpResponse
from django.shortcuts import render
from marketplace.models import Producto, Categoria


def index(request):
    return render(request, 'home.html',
                  context={"products": Producto.objects.all(), "categorias": Categoria.objects.all()})


def buscar_producto(request):
    query = request.GET.get('q', '')
    productos = Producto.objects.filter(nombre__icontains=query).order_by('-promocion')
    return render(request, 'home.html', {'productos': productos, 'query': query})
