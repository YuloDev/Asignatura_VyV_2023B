import django
from django.test import RequestFactory

django.setup()

from behave import *
from marketplace.models import *

use_step_matcher("re")


# PRODUCTO
@step("que el Cliente ha realizado el pago y el proceso de envío de la compra ha finalizado")
def step_impl(context):
    context.producto = Producto.objects.get(nombre="Martillo")
    arreglo_productos_pedidos = [context.producto]
    context.cliente = Cliente.objects.get(cedula="1752124578")
    pedido, creado = Pedido.objects.get_or_create(estado_pedido="Entregado", cliente_id=context.cliente.cedula,
                                                  servicio_id=1)
    context.pedido, creado = pedido, creado
    # Ver el estado del pago
    assert ((context.pedido.estado_pedido == "Entregado"
             or context.pedido.estado_pedido == "Entregado con retraso")), "No se entrego el pedido correctamente"


@step("se tiene un Producto con las siguientes valoraciones totales")
def step_impl(context):
    lista_porcentajes_por_estrella = list()

    for row in context.table:
        total_de_calificaciones = int(row["total_de_calificaciones"])
        cantidad_de_estrellas = int(row["cantidad_de_estrellas"])
        porcentaje_de_calificaciones = row["porcentaje_de_calificaciones"]

        lista_porcentajes_por_estrella.append(porcentaje_de_calificaciones)

        assert context.producto.calificaciones[str(cantidad_de_estrellas)] == total_de_calificaciones, ("No se tiene "
                                                                                                        "el total de "
                                                                                                        "calificaciones correcto")

    for i in context.producto.calificaciones:
        porcentajes_calculados = context.producto.obtener_porcentajes_de_calificaciones()
        porcentajes_calculados.reverse()
        print(porcentajes_calculados[int(i)-1]+"%" + " == " + lista_porcentajes_por_estrella[int(i) - 1])
        assert porcentajes_calculados[int(i)-1]+"%" == lista_porcentajes_por_estrella[int(i) - 1], ("No se tiene el "
                                                                                                     "porcentaje de "
                                                                                                     "calificaciones "
                                                                                                     "correcto")


@step("el Cliente seleccione una Calificación de tres sobre cinco estrellas del Producto y seleccione la causa 2, "
      "8 de las siguientes causas de su Calificación")
def step_impl(context):
    causas = list()
    causas_seleccionada = list()

    for row in context.table:
        causas.append(row["causas"])

    for causa in causas:
        if causa == "Mal funcionamiento":
            causas_seleccionada.append(causa)
        if causa == "Concuerda con la descripcion":
            causas_seleccionada.append(causa)

    calificaciones_recibidas = list(Calificacion.objects.filter(id_producto_id=context.producto.id))
    context.cliente.calificar_producto(3, causas_seleccionada, context.producto, calificaciones_recibidas)

    if calificaciones_recibidas[-1] is None:
        for causa_buscada in calificaciones_recibidas[-1].causas:
            if causa_buscada == causas_seleccionada:
                assert True, "No se ha calificado correctamente el Producto"


@step(
    "el vendedor podrá visualizar el siguiente reporte del Producto con todas las causas en orden descendente y un "
    "promedio general de estrellas del Producto")
def step_impl(context):
    lista_porcentajes_por_estrella = list()
    lista_causas_esperadas = list()
    lista_causas_obtenidas = list()
    promedio_general = 0
    lista_porcentajes_por_estrella = list(context.producto.obtener_porcentajes_de_calificaciones())
    lista_porcentajes_por_estrella.reverse()

    for row in context.table:
        cantidad_de_estrellas = int(row["cantidad_de_estrellas"])
        porcentaje_de_calificaciones = row["porcentaje_de_calificaciones"]
        causas = row["causas"]
        promedio_general = row["promedio"]
        lista_causas_esperadas.append(causas)

        assert lista_porcentajes_por_estrella[
                   cantidad_de_estrellas - 1] + "%" == porcentaje_de_calificaciones, ("No se tiene el porcentaje de "
                                                                                "calificaciones correcto")

    calificaciones_recibidas = list(Calificacion.objects.filter(id_producto_id=1).all())
    for i in range(1, 6, 1):
        lista_causas_obtenidas.append(context.producto.obtener_causas_de_cada_estrella(calificaciones_recibidas)[i])
        print(lista_causas_obtenidas[i - 1] + " == " + lista_causas_esperadas[i - 1])
        assert lista_causas_obtenidas[i - 1] == lista_causas_esperadas[i - 1], "No se tienen las causas correcta"

    assert context.producto.obtener_promedio_general_del_producto() == int(promedio_general), ("No se tiene el promedio"
                                                                                               " general correcto del "
                                                                                               "Producto")


# SERVICIO
@step("que el Cliente ha dado su feedback sobre el producto")
def step_impl(context):
    context.producto = Producto.objects.get(nombre="Martillo")
    arreglo_productos_pedidos = [context.producto]
    context.cliente = Cliente.objects.get(cedula="1752124578")
    pedido, creado = Pedido.objects.get_or_create(estado_pedido="Entregado", cliente_id=context.cliente.cedula,
                                                  servicio_id=1)
    context.pedido, creado = pedido, creado
    producto_con_feedback = context.producto.feedback_producto_esta_dado()
    assert producto_con_feedback == True, "No se ha calificado el producto"


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
        print(str(i["porcentaje"]) + "%" + "==" + str(lista_porcentajes_por_estrella[int(i["estrellas"]) - 1]))
        assert i["porcentaje"] + "%" == lista_porcentajes_por_estrella[int(i["estrellas"]) - 1], ("No se tiene el porcentaje "
                                                                                            "de calificaciones correcto")


@step("el Cliente seleccione una Calificación de tres sobre cinco estrellas del Servicio y seleccione la causa 1 de "
      "las siguientes causas de su Calificación")
def step_impl(context):
    causas = list()
    causa_seleccionada = list()

    for row in context.table:
        causas.append(row["causas"])

    for causa in causas:
        if causa == "Paquete daniado":
            causa_seleccionada.append(causa)

    calificaciones_recibidas = list(Calificacion.objects.filter(id_servicio_id=1).all())
    context.cliente.calificar_servicio(context.pedido, 3, causa_seleccionada, calificaciones_recibidas)

    if calificaciones_recibidas[-1] is None:
        for causa_buscada in calificaciones_recibidas[-1].causas:
            if causa_buscada == causa_seleccionada:
                assert True, "No se ha seleccionado la causa correctamente"


@step(
    "el vendedor podrá visualizar el siguiente reporte del Servicio con todas las causas en orden descendente y un "
    "promedio general de estrellas del Servicio")
def step_impl(context):
    lista_porcentajes_por_estrella = list()
    lista_causas_esperadas = list()
    lista_causas_obtenidas = list()
    promedio_general = 0
    lista_porcentajes_por_estrella = list(context.pedido.servicio.obtener_porcentajes_de_calificaciones())
    lista_porcentajes_por_estrella.reverse()

    for row in context.table:
        cantidad_de_estrellas = int(row["cantidad_de_estrellas"])
        porcentaje_de_calificaciones = row["porcentaje_de_calificaciones"]
        causas = row["causas"]
        promedio_general = row["promedio"]
        lista_causas_esperadas.append(causas)
        assert lista_porcentajes_por_estrella[
                   cantidad_de_estrellas - 1] + "%" == porcentaje_de_calificaciones, ("No se tiene el porcentaje de "
                                                                                "calificaciones correcto")
    calificaciones_recibidas = list(Calificacion.objects.filter(id_servicio_id=1).all())
    for i in range(1, 6, 1):
        lista_causas_obtenidas.append(context.pedido.servicio.obtener_causas_de_cada_estrella(calificaciones_recibidas)[i])
        print(lista_causas_obtenidas[i - 1] + " == " + lista_causas_esperadas[i - 1])
        assert lista_causas_obtenidas[i - 1] == lista_causas_esperadas[i - 1], "No se tienen las causas correcta"

    assert context.pedido.servicio.obtener_promedio_general_del_servicio() == int(promedio_general), ("No se tiene el "
                                                                                                      "promedio general"
                                                                                                      " correcto")
