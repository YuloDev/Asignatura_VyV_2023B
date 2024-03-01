from behave import *
from marketplace.models import *

use_step_matcher("re")


@step('que existen "(?P<producto>.+)"que pertenecen a una "(?P<categoria>.+)" con (?P<unidades_vendidas>\\d+)')
def step_impl(context, producto, categoria, unidades_vendidas):
    context.producto1 = Producto(nombre=producto, unidades_vendidas=unidades_vendidas)
    context.categoria1 = Categoria(nombreCategoria=categoria, record=120)
    context.producto1.asignar_categoria(context.categoria1)
    assert context.producto1.categoria is not None, "No posee una categoria"


@step( 'las (?P<unidades_vendidas>\\d+) del "(?P<producto>.+)" superan el (?P<record_ventas>\\d+) de la "(?P<categoria>.+)"')
def step_impl(context, unidades_vendidas, producto, record_ventas, categoria):
    context.producto1 = Producto(nombre=producto, unidades_vendidas=unidades_vendidas)
    context.categoria1 = Categoria(nombreCategoria=categoria, record=record_ventas)
    context.producto1.asignar_categoria(context.categoria1)
    # Verificar que las unidades vendidas superen el record de la categoría
    assert context.producto1.unidades_vendidas_ha_superado_record(
        context.categoria1), f"Las unidades vendidas no superan el record en la categoría {context.categoria1.nombreCategoria}"


@step( 'el "(?P<producto>.+)" se muestra en la sección de recomendados dentro de la "(?P<categoria>.+)" durante (?P<tiempo>.+)')
def step_impl(context, producto, categoria, tiempo):
    context.recomendacion = Recomendacion()

    # Asignar el producto como recomendado con duración 7
    context.recomendacion.asignar_recomendado(categoria,producto, duracion=tiempo)

    # Obtener la lista de productos recomendados
    recomendados_por_categoria = context.recomendacion.obtener_recomendados()

    assert producto in recomendados_por_categoria[categoria]
    assert recomendados_por_categoria[categoria][producto] == tiempo


@step("que existe un vendedor y su producto")
def step_impl(context):
    context.vendedor = Vendedor(nombre="Rafael", apellido="Piedra")
    context.producto = Producto(nombre="Herramienta")

    assert context.producto in context.vendedor.obtener_productos()


@step("el producto se muestra al inicio de la lista de productos promocionados de esa categoría")
def step_impl(context):
    context.vendedor = Vendedor(nombre="Rafael", apellido="Piedra")
    context.producto_promocionado = Producto(nombre="Herramienta2")
    context.vendedor.agregar_producto(context.producto_promocionado)
    context.vendedor.pagar_promocion(monto=10, producto=context.producto_promocionado)

    # assert context.vendedor.tiene_promocion_activa() == True
    assert context.producto_promocionado in context.clasificador.obtener_productos_promocionados()
