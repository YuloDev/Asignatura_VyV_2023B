from behave import *
from marketplace.models import *
use_step_matcher("re")






@step("que existe un vendedor y su producto y una categoría con un record de ventas inicial")
def step_impl(context):
    context.vendedor = Vendedor(nombre="Rafael", apellido="Piedra")
    context.producto = Producto(nombre="Herramienta")
    context.categoria = Categoria(record=100)
    context.vendedor.agregar_producto(context.producto)

    assert context.producto in context.vendedor.obtener_productos()


@step("ese producto supere el récord de ventas de su categoría")
def step_impl(context):
    context.producto.asignar_categoria(context.categoria)

    assert context.producto.ha_superado_record() == True


@step("El producto se muestra en el inicio de la lista de productos de esa categoría.")
def step_impl(context):
    context.clasificador = Clasificador()
    context.clasificador.agregar_vendedor(context.vendedor)
    context.clasificador.notificar(context.vendedor)
    context.clasificador.buscar_productos_mas_vendidos()

    assert context.producto in context.clasificador.listar_productos_mas_vendidos()

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