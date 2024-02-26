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

@step("seleccione algunas de las siguientes causas de su Calificación para el Servicio")
def step_impl(context):
    causas = list()
    causa_seleccionada = ""

    for row in context.table:
        causas.append(row["causas"])

    for causa in causas:
        if causa == "Paquete dañado":
            causa_seleccionada = causa

    if context.pedido.servicio.calificaciones_recibidas[-1] is None:
        for causa_buscada in context.pedido.servicio.calificaciones_recibidas[-1].causas:
            if causa_buscada == causa_seleccionada:
                assert True, "No se ha seleccionado la causa correctamente"

@step("la valoración total de calificaciones de 3 estrellas del Servicio aumentará en 1 de la siguiente manera")
def step_impl(context):
    assert context.pedido.servicio.puntuaciones_calificaciones[2]["cantidad"] == 3, "No se ha aumentado la calificación correctamente"


@step("el vendedor podrá visualizar el siguiente reporte con todas las causas en orden descendente")
def step_impl(context):
    lista_porcentajes_por_estrella = list()
    lista_causas_esperadas = list()
    lista_causas_obtenidas = list()

    lista_porcentajes_por_estrella = context.pedido.servicio.obtener_porcentajes_de_calificaciones()

    for row in context.table:
        cantidad_de_estrellas = int(row["cantidad_de_estrellas"])
        porcentaje_de_calificaciones = row["porcentaje_de_calificaciones"]
        causas = row["causas"]
        lista_causas_esperadas.append(causas)
        assert lista_porcentajes_por_estrella[
                   cantidad_de_estrellas - 1] == porcentaje_de_calificaciones, ("No se tiene el porcentaje de "
                                                                                "calificaciones correcto")

    for i in range(1, 6, 1):
        lista_causas_obtenidas.append(context.pedido.servicio.obtener_causas_de_cada_estrella()[i])
        print(lista_causas_obtenidas[i - 1] + " == " + lista_causas_esperadas[i - 1])
        assert lista_causas_obtenidas[i - 1] == lista_causas_esperadas[i - 1], "No se tienen las causas correcta"


@step("que el Cliente ha realizado el pago y el proceso de envío de la compra ha finalizado")
def step_impl(context):
    context.producto = Producto(1, "Martillo", "De madera")
    arreglo_productos_pedidos = [context.producto]
    context.pedido = Pedido(1, "Entregado", 6, "direccion", arreglo_productos_pedidos)
    context.cliente = Cliente("1752458974", "Juan", "Herrera", "juan.herrera@hotmail.com",
                              "0984759642", context.pedido)
    assert ((context.pedido.estado == "Entregado"
             or context.pedido.estado == "Entregado con retraso")
            and context.pedido.pagado), "No se entrego el pedido correctamente"


@step("se tiene un Producto con las siguientes valoraciones totales")
def step_impl(context):
    lista_porcentajes_por_estrella = list()

    for row in context.table:
        total_de_calificaciones = int(row["total_de_calificaciones"])
        cantidad_de_estrellas = int(row["cantidad_de_estrellas"])
        porcentaje_de_calificaciones = row["porcentaje_de_calificaciones"]

        lista_porcentajes_por_estrella.append(porcentaje_de_calificaciones)

        assert context.producto.calificaciones[
                   cantidad_de_estrellas] == total_de_calificaciones, "No se tiene el total de calificaciones correcto"

    for i in context.producto.calificaciones:
        porcentajes_calculados = context.producto.obtener_porcentajes_de_calificaciones()
        assert porcentajes_calculados[i - 1] == lista_porcentajes_por_estrella[
            i - 1], "No se tiene el porcentaje de calificaciones correcto"


@step("el Cliente envíe una Calificación de tres sobre cinco estrellas del Producto")
def step_impl(context):
    pass


@step("seleccione algunas de las siguientes causas de su Calificación para el Producto")
def step_impl(context):
    pass


@step("la valoración total de calificaciones de 3 estrellas del Producto aumentará en 1")
def step_impl(context):
    pass


@step("el vendedor podrá visualizar el siguiente reporte")
def step_impl(context):
    pass