# Created by rafae at 17/02/2024
  # language: es

Característica:
  Como vendedor
  Quiero monitorear el estado de los pedidos en cada una de sus fases
  Para saber la eficacia y eficiencia de mi proceso.

  Escenario: Visualizar resumen del seguimiento interno de los pedidos en la etapa de precompra
    Dado que un vendedor tiene uno o varios pedidos
      | numero_pedido | estado_pedido | etapa_pedido        | fecha_creacion_pedido | fecha_estimada_etapa_esperada_ | fecha_estimada_etapa_real |
      | 01            | a_tiempo      | precompra           | 2024-02-18            | 2024-02-20                     | 2024-02-19                |
      | 02            | atrasado      | reserva             | 2024-02-18            | 2024-02-22                     | 2024-02-23                |
      | 03            | cancelado     | listo_para_entregar | 2024-02-18            | 2024-02-20                     | 2024-02-19                |
      | 04            | cancelado     | precompra           | 2024-02-18            | 2024-02-20                     | 2024-02-19                |
      | 05            | a_tiempo      | reserva             | 2024-02-18            | 2024-02-22                     | 2024-02-21                |
      | 06            | atrasado      | listo_para_entregar | 2024-02-18            | 2024-02-20                     | 2024-02-20                |
    Y el numero de pedidos totales y el tiempo estimado para cada etapa en dias es el siguiente
      | etapa_pedido        | total_pedidos | tiempo_etapa |
      | precompra           | 2             | 2            |
      | reserva             | 2             | 4            |
      | listo_para_entregar | 2             | 2            |
    Cuando accede al resumen del seguimiento interno en la etapa de precompra
    Entonces puede visualizar gráficas que proporcionen información sobre el numero de pedidos totales, el numero de pedidos cancelados, el numero de pedidos a tiempo y el numero de pedidos atrasados cuando sobrepasan el tiempo estimado para la etapa de precompra
      | estado_pedido | numero_pedidos |
      | a_tiempo      | 1              |
      | atrasado      | 0              |
      | cancelado     | 1              |

  Escenario: Visualizar resumen del seguimiento interno de los pedidos en la etapa de reserva
    Dado que un vendedor tiene uno o varios pedidos
      | numero_pedido | estado_pedido | etapa_pedido        | fecha_creacion_pedido | fecha_estimada_etapa_esperada_ | fecha_estimada_etapa_real |
      | 01            | a_tiempo      | precompra           | 2024-02-18            | 2024-02-20                     | 2024-02-19                |
      | 02            | atrasado      | reserva             | 2024-02-18            | 2024-02-22                     | 2024-02-23                |
      | 03            | cancelado     | listo_para_entregar | 2024-02-18            | 2024-02-20                     | 2024-02-19                |
      | 04            | cancelado     | precompra           | 2024-02-18            | 2024-02-20                     | 2024-02-19                |
      | 05            | a_tiempo      | reserva             | 2024-02-18            | 2024-02-22                     | 2024-02-21                |
      | 06            | atrasado      | listo_para_entregar | 2024-02-18            | 2024-02-20                     | 2024-02-20                |
    Y el numero de pedidos totales y el tiempo estimado para cada etapa en dias es el siguiente
      | etapa_pedido        | total_pedidos | tiempo_etapa |
      | precompra           | 2             | 2            |
      | reserva             | 2             | 4            |
      | listo_para_entregar | 2             | 2            |
    Cuando accede al resumen del seguimiento interno en la etapa de reserva
    Entonces puede visualizar gráficas que proporcionen información sobre el numero de pedidos totales, el numero de pedidos cancelados, el numero de pedidos a tiempo y el numero de pedidos atrasados cuando sobrepasan el tiempo estimado para la etapa de reserva
      | estado_pedido | numero_pedidos |
      | a_tiempo      | 1              |
      | atrasado      | 1              |
      | cancelado     | 0              |

  Escenario: Visualizar resumen del seguimiento interno de los pedidos en la etapa de listo_para_entregar
    Dado que un vendedor tiene uno o varios pedidos
      | numero_pedido | estado_pedido | etapa_pedido        | fecha_creacion_pedido | fecha_estimada_etapa_esperada_ | fecha_estimada_etapa_real |
      | 01            | a_tiempo      | precompra           | 2024-02-18            | 2024-02-20                     | 2024-02-19                |
      | 02            | atrasado      | reserva             | 2024-02-18            | 2024-02-22                     | 2024-02-23                |
      | 03            | cancelado     | listo_para_entregar | 2024-02-18            | 2024-02-20                     | 2024-02-19                |
      | 04            | cancelado     | precompra           | 2024-02-18            | 2024-02-20                     | 2024-02-19                |
      | 05            | a_tiempo      | reserva             | 2024-02-18            | 2024-02-22                     | 2024-02-21                |
      | 06            | atrasado      | listo_para_entregar | 2024-02-18            | 2024-02-20                     | 2024-02-20                |
    Y el numero de pedidos totales y el tiempo estimado para cada etapa en dias es el siguiente
      | etapa_pedido        | total_pedidos | tiempo_etapa |
      | precompra           | 2             | 2            |
      | reserva             | 2             | 4            |
      | listo_para_entregar | 1             | 2            |
    Cuando accede al resumen del seguimiento interno en la etapa de listo_para_entregar
    Entonces puede visualizar gráficas que proporcionen información sobre el numero de pedidos totales, el numero de pedidos cancelados, el numero de pedidos a tiempo y el numero de pedidos atrasados cuando sobrepasan el tiempo estimado para la etapa de listo_para_entregar
      | estado_pedido | numero_pedidos |
      | a_tiempo      | 0              |
      | atrasado      | 1              |
      | cancelado     | 1              |