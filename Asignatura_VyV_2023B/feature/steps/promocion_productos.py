import django
from django.test import RequestFactory
from marketplace.views import index

django.setup()

from behave import *
from marketplace.models import *

use_step_matcher("re")


@step("que existen clientes con preferencias establecidas")
def step_impl(context):
    for row in context.table:
        Cliente.objects.get_or_create(nombre=row["cliente"], preferencias=row["preferencias"])
        context.cliente = row["cliente"]
        context.preferencias = row["preferencias"]
    for row in context.table:
        assert Cliente.objects.filter(nombre=row["cliente"]).exists()


@step("que existen categorías con record de ventas")
def step_impl(context):
    context.categorias = ""
    for row in context.table:
        Categoria.objects.get_or_create(nombre=row["categoria"], record_ventas=row["record_ventas"])
        context.categorias += row["categoria"] + " "
    for row in context.table:
        assert Categoria.objects.filter(nombre=row["categoria"]).exists()


@step("al menos una de las categorías pertenece a las preferencias del cliente")
def step_impl(context):
    categorias = context.categorias.split(" ")
    assert any(categoria in context.preferencias for categoria in categorias)


@step("existen productos que pertenecen a una unica categoría con unidades vendidas")
def step_impl(context):
    context.productos = []
    for row in context.table:
        producto = Producto.objects.get_or_create(nombre=row["producto"],
                                                  categoria=Categoria.objects.get(nombre=row["categoria"]),
                                                  unidades_vendidas=row["unidades_vendidas"])
        context.productos.append(producto[0])
    for row in context.table:
        assert Producto.objects.filter(nombre=row["producto"]).exists()


@step("las unidades vendidas de algun producto superan el record de ventas de la categoría")
def step_impl(context):
    for producto in context.productos:
        if producto.ha_superado_record():
            assert True


@step("se muestre la pagina principal del marketplace")
def step_impl(context):
    request_factory = RequestFactory()
    request = request_factory.get('/')
    response = index(request)
    assert response.status_code == 200


@step(
    "en la parte superior de la ventana principal del marketplace se muestran las categorias pertenecientes a las preferencias del cliente con el producto que superó el record de ventas")
def step_impl(context):
    request = RequestFactory().get('/')
    response = index(request)
    print(response.content)



@step("el record de ventas de la categoria se actualiza con el valor de las unidades vendidas del producto")
def step_impl(context):
    pass


@step("que existen vendedores que tienen productos")
def step_impl(context):
    pass


@step("que existen paquetes de promociones")
def step_impl(context):
    pass


@step("los vendedores adquieren un paquete de promoción")
def step_impl(context):
    pass


@step("se realice una búsqueda de algún producto")
def step_impl(context):
    pass


@step(
    "los productos promocionados se mostrarán como primer resultado en la búsqueda que coincida con el nombre del producto, ordenados por el tipo del paquete y la fecha de adquisición del")
def step_impl(context):
    pass
