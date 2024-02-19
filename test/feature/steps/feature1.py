from behave import *
from test.modelos.modelo import *

use_step_matcher("re")

# Variable global para mantener el índice actual del arreglo de resumenes
indice_resumenes = 0

@step("que un vendedor tiene uno o varios pedidos")
def step_impl(context):
    context.vendedor = Vendedor("Vendedor1")
    #Aqui tendrian que implementar la logica para la lista de pedidos, ahorita esta quemado un solo pedido.
    context.pedido = Pedido("Pedido1", 1, 5, 2, "Vigente") # Esta linea pueden cambiar a su criterio
    context.vendedor.agregar_pedido(context.pedido) # Esta linea pueden cambiar a su criterio
    assert (context.vendedor.pedidos != []), f"El vendedor no tiene pedidos" # Esta linea pueden cambiar a su criterio

@step("accede al resumen del seguimiento interno")
def step_impl(context):
    global indice_resumenes  # Utilizamos la variable global para cargar el arreglo de resumenes
    context.vendedor.visualizar_resumen()
    # Accedemos al elemento correspondiente en el arreglo resumenes
    context.resumen = resumenes[indice_resumenes]
    indice_resumenes += 1  # Incrementamos el índice para el próximo paso
    assert (context.resumen != None), "El resumen no se ha generado"


@step(
    "puede visualizar e interactuar con gráficas que proporcionen información por (?P<etapa>.+) sobre el (?P<num_pedidos_total>.+), el (?P<num_pedido_cancelados>.+) y el desempeño de los pedidos reflejados como el (?P<num_pedidos_atrasados>.+) y el (?P<num_pedidos_a_tiempo>.+) cuando se sobrepasa el (?P<tiempo_etapa>.+)")
def step_impl(context, etapa, num_pedidos_total, num_pedido_cancelados, num_pedidos_atrasados, num_pedidos_a_tiempo,
              tiempo_etapa):
    # Verificamos que los datos del resumen sean correctos
    assert (context.resumen.sumar_pedidos() == int(num_pedidos_total)), f"El número total de pedidos no coincide"

    # Aqui tienen que hacer la suma de pedidos cancelados y comparar con los pedidos cancelados en el esquema de escenario como esta en la linea de arriba.
    # Aqui tienen que hacer la suma de pedidos atrasados y a tiempo y comparar con el esquema de escenario como esta en la linea de arriba.