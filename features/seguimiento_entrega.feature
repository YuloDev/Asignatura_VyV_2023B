# Created by grupo 7 at 25/2/2024
# language: es
Característica: : Seguimiento de entrega de compras de clientes
  Como vendedor
  Quiero llevar seguimiento del tiempo y estado de entrega de las compras de mis clientes
  Para obtener un informe de los envíos y mejorar la experiencia de los clientes

  Escenario: : Visualizar resumen de pedidos en estado "listo para entregar"
    Dado que un Vendedor tiene varios Pedidos
      | estado_pedido | etapa_pedido | fecha_creacion_pedido | fecha_entrega_cliente | Vendedor     |
      | a_tiempo      | E            | 2024-02-18            | 2024-02-29            | Luis Almache |
      | a_tiempo      | EC           | 2024-02-18            | 2024-02-29            | Luis Almache |
      | a_tiempo      | RA           | 2024-02-18            | 2024-02-29            | Luis Almache |
      | a_tiempo      | RA           | 2024-02-18            | 2024-02-29            | Luis Almache |
      | a_tiempo      | LPE          | 2024-02-25            | 2024-03-07            | Luis Almache |
    Cuando el Vendedor visualice el resumen de los Pedidos en etapa "listo para entregar"
    Entonces se actulizarán los estados de los Pedidos según el tiempo actual
    Y se mostrarán los siguientes datos
      | estado_pedido | numero_pedidos |
      | a_tiempo      | 1              |
      | atrasado      | 0              |
