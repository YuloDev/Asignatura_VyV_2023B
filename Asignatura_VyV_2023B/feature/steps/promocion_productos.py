from behave import *


use_step_matcher("re")




@step("que existen clientes con preferencias establecidas")
def step_impl(context):
    pass
    # for row in context.table:
    #     Cliente.objects.get_or_create(nombre=row["cliente"])

    # assert Cliente.objects.exists(Cliente.objects.filter(nombre=row["cliente"]))


@step("que existen categorías con record de ventas")
def step_impl(context):
    pass


@step("las categorías pertenecen a las preferencias del cliente")
def step_impl(context):
    pass


@step("productos que pertenecen a una categoría con unidades vendidas")
def step_impl(context):
    pass


@step("las unidades vendidas de algun producto superan el record de ventas de la categoría")
def step_impl(context):
    pass


@step(
    "en la parte superior de la ventana principal del marketplace se muestran las categorias pertenecientes a las preferencias del cliente con el producto que superó el record de ventas")
def step_impl(context):
    pass


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


def step_impl(context):
    pass


@step(
    "los productos promocionados se mostrarán como primer resultado en la búsqueda que coincida con el nombre del producto, ordenados por el tipo del paquete y la fecha de adquisición del")
def step_impl(context):
    pass
