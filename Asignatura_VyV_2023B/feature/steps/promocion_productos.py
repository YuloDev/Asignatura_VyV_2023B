from behave import *
from marketplace.models import *
use_step_matcher("re")


@step("que existen productos que pertenecen a una categoria con un record de ventas")
def step_impl(context):
    context.producto = Producto(nombre="Martillo",unidades_vendidas=12)
    context.producto= Producto(nombre="Destornillador",unidades_vendidas=1)
    context.categoria = Categoria("Herramientas",record=100)
    context.categoria.agregar_producto(context.producto)

    # Verificar que el producto pertenezca a la categoría
    assert context.producto in context.categoria.obtener_productos()


@step("las unidades vendidas del producto superen el récord de ventas de su categoría")
def step_impl(context):
    context.producto = Producto(nombre="Martillo",unidades_vendidas=120)
    context.categoria = Categoria("Herramientas",record=100)
    context.producto.asignar_categoria(categoria=context.categoria)
    # Verificar que el producto haya superado el record de ventas de su categoria
    assert context.producto.unidades_vendidas_ha_superado_record() == True


@step("el producto se asigna como recomendado dentro de su categoria durante una semana")
def step_impl(context):
    # Crear un producto y una instancia de Recomendacion
    context.producto = Producto(nombre="Martillo", unidades_vendidas=120)
    context.categoria = Categoria("Herramientas",record=100)
    context.producto.asignar_categoria(categoria=context.categoria)
    context.recomendacion = Recomendacion()

    # Asignar el producto como recomendado con duración 7
    context.recomendacion.asignar_recomendado(context.producto, duracion=7)

    # Obtener la lista de productos recomendados
    recomendados_por_categoria = context.recomendacion.obtener_recomendados()

    # Verificar que los productos están recomendados en su categoria y que la duración es 7
    assert context.producto in recomendados_por_categoria[context.categoria].keys()
    assert recomendados_por_categoria[context.categoria][context.producto] == 7


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

