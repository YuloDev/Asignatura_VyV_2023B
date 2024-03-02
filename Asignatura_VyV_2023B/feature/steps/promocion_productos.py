from behave import *

use_step_matcher("re")


@step("que existen clientes con preferencias establecidas")
def step_impl(context):
    raise NotImplementedError(u'STEP: Dado que existen clientes con preferencias establecidas')


@step("que existen categorías con record de ventas")
def step_impl(context):
    raise NotImplementedError(u'STEP:')


@step("las categorías pertenecen a las preferencias del cliente")
def step_impl(context):
    raise NotImplementedError(u'STEP: Y las categorías pertenecen a las preferencias del cliente')


@step("productos que pertenecen a una categoría con unidades vendidas")
def step_impl(context):
    raise NotImplementedError(u'STEP: Y productos que pertenecen a una categoría con unidades vendidas')


@step("las unidades vendidas de algun producto superan el record de ventas de la categoría")
def step_impl(context):
    raise NotImplementedError(
        u'STEP: Cuando las unidades vendidas de algun producto superan el record de ventas de la categoría')


@step(
    "en la parte superior de la ventana principal del marketplace se muestran las categorias pertenecientes a las preferencias del cliente con el producto que superó el record de ventas")
def step_impl(context):
    raise NotImplementedError(
        u'STEP: Entonces en la parte superior de la ventana principal del marketplace se muestran las categorias pertenecientes a las preferencias del cliente con el producto que superó el record de ventas')


@step("el record de ventas de la categoria se actualiza con el valor de las unidades vendidas del producto")
def step_impl(context):
    raise NotImplementedError(
        u'STEP: Y el record de ventas de la categoria se actualiza con el valor de las unidades vendidas del producto')


@step("que existen vendedores que tienen productos")
def step_impl(context):
    raise NotImplementedError(u'STEP: Dado que existen vendedores que tienen productos')


@step("que existen paquetes de promociones")
def step_impl(context):
    raise NotImplementedError(u'STEP: Y que existen paquetes de promociones')


@step("los vendedores adquieren un paquete de promoción")
def step_impl(context):
    raise NotImplementedError(u'STEP: Y los vendedores adquieren un paquete de promoción') \
 \
    @step("se realice una búsqueda de algún producto")


def step_impl(context):
    raise NotImplementedError(u'STEP: Cuando se realice una búsqueda de algún producto')


@step(
    "los productos promocionados se mostrarán como primer resultado en la búsqueda que coincida con el nombre del producto, ordenados por el tipo del paquete y la fecha de adquisición del")
def step_impl(context):
    raise NotImplementedError(
        u'STEP: Entonces los productos promocionados se mostrarán como primer resultado en la búsqueda que coincida con el nombre del producto, ordenados por el tipo del paquete y la fecha de adquisición del')
