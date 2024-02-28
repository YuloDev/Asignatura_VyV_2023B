import datetime
import os
# from datetime import datetime
import django

django.setup()

import django
from behave import *
from marketplace.models import *

use_step_matcher("re")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Asignatura_VyV_2023B.settings')


# @step("que existen productos que pertenecen a una categoria con un record de ventas")
# def step_impl(context):
#     context.producto = Producto(nombre="Martillo", unidades_vendidas=12)
#     context.producto = Producto(nombre="Destornillador", unidades_vendidas=1)
#     context.categoria = Categoria("Herramientas", record=100)
#     context.categoria.agregar_producto(context.producto)
#
#     # Verificar que el producto pertenezca a la categoría
#     assert context.producto in context.categoria.obtener_productos()
#
#
# @step("las unidades vendidas del producto superen el récord de ventas de su categoría")
# def step_impl(context):
#     context.producto = Producto(nombre="Martillo", unidades_vendidas=120)
#     context.categoria = Categoria("Herramientas", record=100)
#     context.producto.asignar_categoria(categoria=context.categoria)
#     assert context.producto.unidades_vendidas_ha_superado_record() == True
#
#
# @step("el producto se asigna como recomendado dentro de su categoria durante una semana")
# def step_impl(context):
#     # Crear un producto y una instancia de Recomendacion
#     context.producto = Producto(nombre="Martillo", unidades_vendidas=120)
#     context.categoria = Categoria("Herramientas", record=100)
#     context.producto.asignar_categoria(categoria=context.categoria)
#     context.recomendacion = Recomendacion()
#
#     # Asignar el producto como recomendado con duración 7
#     context.recomendacion.asignar_recomendado(context.producto, duracion=7)
#
#     # Obtener la lista de productos recomendados
#     recomendados = context.recomendacion.obtener_recomendados()
#
#     # Verificar que el producto está recomendado y que la duración es 7
#     assert context.producto in recomendados.keys()
#     assert recomendados[context.producto] == 7


# @step("que existe un vendedor y su producto")
# def step_impl(context):
#     context.vendedor = Vendedor(nombre="Rafael", apellido="Piedra")
#     context.producto = Producto(nombre="Herramienta")
#
#     assert context.producto in context.vendedor.obtener_productos()
#
# @step("el producto se muestra al inicio de la lista de productos promocionados de esa categoría")
# def step_impl(context):
#     context.vendedor = Vendedor(nombre="Rafael", apellido="Piedra")
#     context.producto_promocionado = Producto(nombre="Herramienta2")
#     context.vendedor.agregar_producto(context.producto_promocionado)
#     context.vendedor.pagar_promocion(monto=10, producto=context.producto_promocionado)
#
#     # assert context.vendedor.tiene_promocion_activa() == True
#     assert context.producto_promocionado in context.clasificador.obtener_productos_promocionados()


@step("que existen vendedores que tienen productos que pertenecen a una sola categoría")
def step_impl(context):
    for row in context.table:
        categoria, created = Categoria.objects.get_or_create(nombre=row['categoria'])
        vendedor, created = Vendedor.objects.get_or_create(nombre=row['nombre_vendedor'],
                                                           apellido=row['apellido_vendedor'])
        Producto.objects.create(nombre=row['nombre_producto'], unidades_vendidas=0, vendedor=vendedor,
                                categoria=categoria)
    # assert Vendedor.objects.count() == len(set(row['nombre_vendedor'] for row in context.table.rows))
    # assert Producto.objects.count() == len(context.table.rows)
    for producto in Producto.objects.all():
        assert producto.categoria is not None
    assert Vendedor.objects.all() is not []
    assert Producto.objects.all() is not []


@step("que existen paquetes de promociones")
def step_impl(context):
    for row in context.table:
        # Convertir fecha de texto a objeto datetime
        fecha_inicio = datetime.datetime.strptime(row['fecha_inicio'], '%d/%m/%Y').date()

        # Crear la promoción
        Promocion.objects.create(
            tipo_promocion=row['tipo_promocion'],
            fecha_inicio=fecha_inicio,
            costo=row['costo'],
            dias_duracion=row['dias_duracion'],
            cantidad_productos=row['cantidad_productos']
        )
    assert Promocion.objects.all() is not []


@step("los vendedores realicen un pago para promocionar sus productos")
def step_impl(context):
    promociones = Promocion.objects.all()

    for vendedor in Vendedor.objects.all():
        productos_vendedor = Producto.objects.filter(vendedor=vendedor)
        for producto in productos_vendedor:
            for promocion in promociones:
                if not producto.promocion and promocion.tipo_promocion == 'gold':
                    producto.promocion = True
                    producto.save()
                    vendedor.pagar_promocion(monto=promocion.costo, producto=producto)
                    break

    productos_promocionados = sum(
        1 for vendedor in Vendedor.objects.all() for producto in vendedor.obtener_productos() if
        producto.tiene_promocion())
    assert Producto.objects.filter(promocion=True).count() == productos_promocionados



@step("se mostrará la sección de productos promocionados de la siguiente manera")
def step_impl(context):
    productos_promocionados = Producto.objects.filter(promocion=True)

    for row in context.table:
        assert productos_promocionados.filter(nombre=row['nombre_producto'], vendedor__nombre=row['nombre_vendedor'],
                                              vendedor__apellido=row['apellido_vendedor']).exists()
    pass
