from behave import *
from modelo.ModeloFeedback import *

use_step_matcher("re")


@step("que el Cliente ha realizado el pago y el proceso de envío de la compra ha finalizado")
def step_impl(context):
    context.producto = Producto(1, "Martillo", "De madera")
    arreglo_productos_pedidos = [context.producto]

    context.servicio = Servicio()
    context.pedido = Pedido(1, "Entregado", 6, "direccion", arreglo_productos_pedidos, context.servicio)
    context.cliente = Cliente("identificador", "nombres", "apellidos", "correoElectronico", "numeroTelefonico",
                              context.pedido)
    assert context.pedido.estado == "Entregado" and context.pedido.pagado, "No se entrego el pedido correctamente"



@step(
    "el Cliente envíe una Calificación de (?P<cantidad_estrellas>.+) estrellas del Producto y del Servicio, y mencione las (?P<causas>.+) de su Calificación\.")
def step_impl(context, cantidad_estrellas, causas):
    raise NotImplementedError(
        u'STEP: Cuando el Cliente envíe una Calificación de <cantidad_estrellas> estrellas del Producto y del Servicio, y mencione las <causas> de su Calificación.')


@step("la valoración total de calificaciones del (?P<item_de_calificacion>.+) aumentará")
def step_impl(context, item_de_calificacion):
    raise NotImplementedError(
        u'STEP: Entonces la valoración total de calificaciones del <item_de_calificacion> aumentará')


@step(
    "el vendedor podrá visualizar el porcentaje de calificaciones de cada cantidad de estrellas junto con los motivos correspondientes al (?P<item_de_calificacion>.+)\.")
def step_impl(context, item_de_calificacion):
    raise NotImplementedError(
        u'STEP: Y el vendedor podrá visualizar el porcentaje de calificaciones de cada cantidad de estrellas junto con los motivos correspondientes al <item_de_calificacion>.')