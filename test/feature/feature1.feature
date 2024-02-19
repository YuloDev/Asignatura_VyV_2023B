# Created by rafae at 17/02/2024
  # language: es

Característica:
  Como vendedor
  Quiero monitorear el estado de los pedidos en cada una de sus fases
  Para saber la eficacia y eficiencia de mi proceso.

  Esquema del escenario:
    Dado que un vendedor tiene uno o varios pedidos
    Cuando accede al resumen del seguimiento interno
    Entonces puede visualizar e interactuar con gráficas que proporcionen información por <etapa> sobre el <num_pedidos_total>, el <num_pedido_cancelados> y el desempeño de los pedidos reflejados como el <num_pedidos_atrasados> y el <num_pedidos_a_tiempo> cuando se sobrepasa el <tiempo_etapa>

    Ejemplos:
      | etapa         | num_pedidos_total | num_pedido_cancelados | num_pedidos_atrasados | num_pedidos_a_tiempo | tiempo_etapa |
      | PreCompra     | 18                | 2                     | 3                     | 13                   | 2               |
      | Reserva       | 12                | 0                     | 1                     | 11                   | 4               |
      | ListoDespacho | 8                 | 1                     | 2                     | 5                    | 2               |