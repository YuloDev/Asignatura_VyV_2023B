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
    "el Cliente envíe una Calificación de (?P<cantidad_estrellas>.+) estrellas del Producto y del Servicio, y mencione las (?P<causas>.+) de su Calificación.")
def step_impl(context, cantidad_estrellas, causas):
    context.cliente.calificar_producto(1, 1, int(cantidad_estrellas), causas)
    context.cliente.calificar_servicio(1, int(cantidad_estrellas), causas)
    calificacion_producto = context.producto.calificaciones_recibidas[-1].cantidad_estrellas
    calificacion_servicio = context.servicio.calificaciones_recibidas[-1].cantidad_estrellas
    motivos_calificacion_producto = context.producto.calificaciones_recibidas[-1].obtener_causas(1)
    motivos_calificacion_servicio = context.servicio.calificaciones_recibidas[-1].obtener_causas(0)
    assert (
            1 <= calificacion_producto <= 5
            and 1 <= calificacion_servicio <= 5
            and motivos_calificacion_producto is not None and len(motivos_calificacion_producto) > 0
            and motivos_calificacion_servicio is not None and len(motivos_calificacion_servicio) > 0
    ), "La calificación del producto o del servicio no es válida o los motivos no han sido proporcionados"


@step("la valoración total de calificaciones del (?P<item_de_calificacion>.+) aumentará")
def step_impl(context, item_de_calificacion):
    calificacion_anterior_producto = 0
    calificacion_anterior_servicio = 0
    if item_de_calificacion.lower() == context.producto.nombre.lower():
        calificacion_anterior_producto = context.producto.calificaciones[
                                             context.producto.calificaciones_recibidas[-1].cantidad_estrellas] + 1
        context.producto.calificaciones[context.producto.calificaciones_recibidas[-1].cantidad_estrellas] += 1
    elif item_de_calificacion.lower() == "servicio":
        calificacion_anterior_servicio = context.servicio.calificaciones[
                                             context.servicio.calificaciones_recibidas[-1].cantidad_estrellas] + 1
        context.servicio.calificaciones[context.servicio.calificaciones_recibidas[-1].cantidad_estrellas] += 1
    assert (
            context.servicio.calificaciones[
                context.servicio.calificaciones_recibidas[-1].cantidad_estrellas] == calificacion_anterior_servicio
            and context.producto.calificaciones[
                context.producto.calificaciones_recibidas[-1].cantidad_estrellas] == calificacion_anterior_producto
    ), "La valoración total de calificaciones no aumentó"


@step(
    "el vendedor podrá visualizar el porcentaje de calificaciones de cada cantidad de estrellas junto con los motivos correspondientes al (?P<item_de_calificacion>.+).")
def step_impl(context, item_de_calificacion):
    opcion = item_de_calificacion.lower()
    se_presento = False
    calificacion = Calificacion(3, -1)
    if context.producto.nombre.lower() == opcion:
        se_presento = calificacion.mostrar_resultados_calificaciones(context.producto, 1)
    elif "servicio" == opcion:
        se_presento = calificacion.mostrar_resultados_calificaciones(context.servicio, 0)
    elif "productos" == opcion:
        se_presento = calificacion.mostrar_resultados_calificaciones(context.calificacion, -1)
    else:
        se_presento = False

    assert se_presento == True, "No se encontró el item de calificación"