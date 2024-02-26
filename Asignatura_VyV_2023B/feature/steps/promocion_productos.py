from behave import *
from marketplace.models import *
from marketplace.models import  *
use_step_matcher("re")






@step("que existe un vendedor y su producto")
def step_impl(context):
    context.vendedor = Vendedor(nombre="Rafael", apellido="Piedra")
    context.producto = Producto(nombre="Herramienta")
    context.vendedor.agregar_producto(context.producto)

    assert context.producto in context.vendedor.obtener_productos()


@step("ese producto supere el récord de ventas de su categoría")
def step_impl(context):
    context.categoria = Categoria(record=100)
    context.producto.asignar_categoria(context.categoria)

    assert context.producto.ha_superado_record() == True


@step("se informa al vendedor y muestra el producto en  la lista de productos más vendidos\.")
def step_impl(context):
    context.categoria = Categoria(record=100)
    context.producto.asignar_categoria(context.categoria)
    context.vendedor.agregar_producto(context.producto)
    context.clasificador = Clasificador()
    context.clasificador.agregar_vendedor(context.vendedor)
    context.clasificador.notificar(context.vendedor)
    context.clasificador.buscar_productos_mas_vendidos()

    assert context.producto in context.clasificador.listar_productos_mas_vendidos()


@step("el vendedor realice un pago para promocionar su producto")
def step_impl(context):
    context.vendedor = Vendedor(nombre="Rafael", apellido="Piedra")
    context.producto_promocionado = Producto(nombre="Herramienta2")
    context.vendedor.agregar_producto(context.producto_promocionado)
    context.vendedor.pagar_promocion(monto=10, producto=context.producto_promocionado)

    assert context.vendedor.tiene_promocion_activa() == True


@step("se destaca ese producto")
def step_impl(context):
    context.clasificador = Clasificador()
    context.vendedor = Vendedor(nombre="Rafael", apellido="Piedra")
    context.producto_promocionado = Producto(nombre="Herramienta2")
    context.vendedor.agregar_producto(context.producto_promocionado)
    context.vendedor.pagar_promocion(1008, producto=context.producto_promocionado)
    context.clasificador.agregar_vendedor(context.vendedor)
    context.clasificador.buscar_productos_promocionados()
    assert context.producto_promocionado in context.clasificador.listar_productos_destacados()

