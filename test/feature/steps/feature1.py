from behave import *
from test.modelos.modelo import *
from datetime import datetime

use_step_matcher("re")

@step("que un vendedor tiene uno o varios pedidos")
def step_impl(context):
    # Crear un vendedor
    context.vendedor = Vendedor("Juan", [])  # Se le proporciona una lista vacía de pedidos al instanciar el vendedor

    # Iterar sobre las filas de la tabla
    for row in context.table:
        # Crear un objeto Pedido con los datos de la fila
        pedido = Pedido.from_row(row)

        # Agregar el pedido a la lista de pedidos del vendedor
        context.vendedor.agregar_pedido(pedido)

    print(f"El vendedor {context.vendedor.nombre_vendedor} tiene {context.vendedor.contar_pedidos()} pedidos.")

    # Verificar que el vendedor tenga al menos un pedido
    assert context.vendedor.contar_pedidos() > 0, "El vendedor no tiene ningún pedido"

    # Obtener el último pedido del vendedor
    ultimo_pedido = context.vendedor.lista_pedidos[-1]

    # Comparar el número de pedido del último pedido con la suma total de pedidos
    suma_total_pedidos = context.vendedor.contar_pedidos()
    assert ultimo_pedido.numero_pedido == str(suma_total_pedidos).zfill(2), "El número total de pedidos del vendedor no coincide"

@step("el numero de pedidos totales y el tiempo estimado para cada etapa en dias es el siguiente")
def step_impl(context):
    pass


@step("accede al resumen del seguimiento interno en la etapa de precompra")
def step_impl(context):
    pass


@step(
    "puede visualizar gráficas que proporcionen información sobre el numero de pedidos totales, el numero de pedidos cancelados, el numero de pedidos a tiempo y el numero de pedidos atrasados cuando sobrepasan el tiempo estimado para la etapa de precompra")
def step_impl(context):
    pass
