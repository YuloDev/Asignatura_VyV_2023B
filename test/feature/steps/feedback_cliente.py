from behave import *
from modelo.ModeloFeedback import *

use_step_matcher("re")


# SERVICIO
@step("que el Cliente ha dado su feedback sobre el producto")
def step_impl(context):
    context.producto = Producto(1, "Martillo", "De madera")
    arreglo_productos_pedidos = [context.producto]
    context.pedido = Pedido(1, "Entregado", 6, "direccion", arreglo_productos_pedidos)

    assert context.producto.feedback_producto_esta_dado()


@step("se tiene un Servicio con las siguientes valoraciones totales")
def step_impl(context):
    calificaciones_totalizadas = 0
    lista_porcentajes_por_estrella = list()

    for i in context.pedido.servicio.puntuaciones_calificaciones:
        calificaciones_totalizadas += i["cantidad"]

    for row in context.table:
        total_de_calificaciones = int(row["total_de_calificaciones"])
        cantidad_de_estrellas = int(row["cantidad_de_estrellas"])
        porcentaje_de_calificaciones = row["porcentaje_de_calificaciones"]
        lista_porcentajes_por_estrella.append(porcentaje_de_calificaciones)

        assert context.pedido.servicio.puntuaciones_calificaciones[cantidad_de_estrellas - 1][
                   "cantidad"] == total_de_calificaciones, "No se tiene el total de calificaciones correcto"

    context.pedido.servicio.calcular_porcentajes()
    for i in context.pedido.servicio.puntuaciones_calificaciones:
        assert i["porcentaje"] == lista_porcentajes_por_estrella[int(i["estrellas"]) - 1], ("No se tiene el porcentaje "
                                                                                            "de calificaciones correcto")


@step("el Cliente envíe una Calificación de tres sobre cinco estrellas del Servicio")
def step_impl(context):
    context.cliente = Cliente("1752458974", "Juan", "Herrera", "juan.herrera@hotmail.com", "0984759642",
                              context.pedido)
    context.cliente.calificar_servicio(context.pedido, 3, ["Paquete dañado"], context.producto)

    assert context.pedido.servicio.puntuaciones_calificaciones[2]["cantidad"] == 3, "No se ha calificado correctamente el producto"
    return True