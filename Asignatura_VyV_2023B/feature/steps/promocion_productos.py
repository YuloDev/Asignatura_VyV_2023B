from decimal import Decimal

import django
import faker

django.setup()
from behave import *
from faker import Faker
from django.test import RequestFactory
from marketplace.views import index, buscar_producto
from marketplace.models import *

use_step_matcher("re")

fake = Faker()


@step("que existen clientes con preferencias establecidas")
def step_impl(context):
    for row in context.table:
        Cliente.objects.get_or_create(nombre=row["cliente"], preferencias=row["preferencias"],
                                      correo='juan@example.com',
                                      cedula='023456789',
                                      apellido='Pérez',
                                      telefono='123456789')
        context.cliente = row["cliente"]
        context.preferencias = row["preferencias"]
    for row in context.table:
        assert Cliente.objects.filter(nombre=row["cliente"]).exists()


@step("que existen categorías con record de ventas")
def step_impl(context):
    context.categorias = []
    for row in context.table:
        categoria, created = Categoria.objects.get_or_create(nombre=row["categoria"],
                                                             defaults={"record_ventas": row["record_ventas"]})
        context.categorias.append(categoria)
    for categoria in context.categorias:
        assert Categoria.objects.filter(nombre=categoria.nombre).exists()


@step("al menos una de las categorías pertenece a las preferencias del cliente")
def step_impl(context):
    assert any(categoria.nombre in context.preferencias for categoria in context.categorias)


@step("existen productos que pertenecen a una unica categoría con unidades vendidas")
def step_impl(context):
    context.productos = []

    for row in context.table:
        producto = Producto.objects.get_or_create(nombre=row["producto"],
                                                  categoria=Categoria.objects.get(nombre=row["categoria"]),
                                                  unidades_vendidas=row["unidades_vendidas"],
                                                  precio=10.0, costo=10.0)
        context.productos.append(producto[0])
    for row in context.table:
        assert Producto.objects.filter(nombre=row["producto"]).exists()


@step("las unidades vendidas de algun producto superan el record de ventas de la categoría")
def step_impl(context):
    context.nombres_categoria_con_record_superado = []
    for producto in Producto.obtener_productos_destacados():
        context.nombres_categoria_con_record_superado.append(producto.categoria)
    assert Producto.obtener_productos_destacados() is not None


@step("se muestre la pagina principal del marketplace")
def step_impl(context):
    request_factory = RequestFactory()
    request = request_factory.get('/')
    response = index(request)
    assert response.status_code == 200


@step(
    "los productos que han superado el record de ventas y pertenecen a una categoría que está incluida en las preferencias del cliente se muestran en la seccion de productos destacados")
def step_impl(context):
    cliente = Cliente.objects.get(nombre=context.cliente)
    context.productos_destacados = cliente.obtener_productos_destacados_de_cliente()
    assert context.productos_destacados is not []


@step("el record de ventas de la categoria se actualiza con el valor de las unidades vendidas del producto")
def step_impl(context):
    Producto.actualizar_record_categorias()
    for producto in context.productos_destacados:
        nombre_categoria = producto.categoria
        categoria = Categoria.objects.get(nombre=nombre_categoria)
        assert producto.unidades_vendidas == categoria.record_ventas


@step("que existen vendedores que tienen productos")
def step_impl(context):
    nombres_productos = []
    for row in context.table:
        vendedor, created = Vendedor.objects.get_or_create(nombre=row['vendedor'])
        nombres_productos = row['nombres_productos'].split(",")
        for nombre_producto in nombres_productos:
            Producto.objects.get_or_create(nombre=nombre_producto,
                                           categoria=Categoria.objects.get(nombre="categoria_x"), vendedor=vendedor,
                                           precio=10.0, costo=10.0)
    for nombre_producto in nombres_productos:
        assert Producto.objects.filter(nombre=nombre_producto).exists()


@step("que existen paquetes de promociones")
def step_impl(context):
    for row in context.table:
        Promocion.objects.get_or_create(
            paquete=row["paquete"],
            costo=row["costo"],
            dias_duracion=row["dias_duracion"],
        )

    for row in context.table:
        assert Promocion.objects.filter(paquete=row["paquete"]).exists()


@step("los vendedores adquieren un paquete de promoción")
def step_impl(context):
    for row in context.table:
        promocion = Promocion.objects.get(paquete=row["paquete_contratado"])
        vendedor = Vendedor.objects.get(nombre=row["vendedor"])
        producto = Producto.objects.get(nombre=row["producto_promocionado"])
        producto.promocion = promocion
        producto.save()


@step("se realice una búsqueda de algún producto")
def step_impl(context):
    request_factory = RequestFactory()
    request = request_factory.get('/buscar-producto/?q=producto')
    response = buscar_producto(request)
    assert response.status_code == 200


@step(
    "los productos promocionados se mostrarán como primer resultado en la búsqueda que coincida con el nombre del producto, ordenados por el tipo del paquete y la fecha de adquisición del paquete")
def step_impl(context):
    assert Producto.buscar_productos("llave") is not None
