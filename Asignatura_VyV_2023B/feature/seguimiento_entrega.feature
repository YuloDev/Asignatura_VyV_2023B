# Created by grupo 7 at 25/2/2024
# language: es
Característica: : Seguimiento de entrega de compras de clientes
  Como vendedor
  Quiero llevar seguimiento del tiempo y estado de entrega de las compras de mis clientes
  Para obtener un informe de los envíos y mejorar la experiencia de los clientes

Esquema del escenario: : Visualizar resumen de pedidos en diferentes etapas para los estados a tiempo y atrasado
    Dado que un Vendedor tiene los siguientes Pedidos
      | estado_pedido | etapa_pedido | fecha_listo_para_entregar | Vendedor     |
      | a_tiempo      | E            | 2024-02-18                | Luis Almache |
      | a_tiempo      | EC           | 2024-02-18                | Luis Almache |
      | a_tiempo      | RA           | 2024-02-18                | Luis Almache |
      | a_tiempo      | RA           | 2024-02-18                | Luis Almache |
      | a_tiempo      | LPE          | 2024-02-25                | Luis Almache |
    Cuando el Vendedor visualice el resumen de los Pedidos en una etapa <etapa>
    Entonces se actualizarán los estados de los Pedidos según el tiempo actual de la zona
    Y se mostrarán el siguiente estado <estado_pedido> con la siguiente cantidad de pedidos <numero_pedidos>
    Ejemplos:
      | etapa | estado_pedido | numero_pedidos |
      | LPE   | AT            | 0              |
      | LPE   | A             | 1              |
      | RA    | AT            | 0              |
      | RA    | A             | 2              |
      | EC    | AT            | 1              |
      | EC    | A             | 0              |
      | E     | AT            | 0              |
      | E     | A             | 1              |


