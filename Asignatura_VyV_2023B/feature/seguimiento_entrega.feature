# Created by grupo 7 at 25/2/2024
# language: es
Característica: : Seguimiento de entrega de compras de clientes
  Como vendedor
  Quiero llevar seguimiento del tiempo y estado de entrega de las compras de mis clientes
  Para obtener un informe de los envíos y mejorar la experiencia de los clientes

Esquema del escenario: : Visualizar resumen de pedidos en diferentes etapas para los estados a tiempo y atrasado
    Dado que un Vendedor tiene los siguientes Pedidos registrados
      | estado_pedido | etapa_pedido | fecha_listo_para_entregar |
      | a_tiempo      | E            | 2024-02-18                |
      | a_tiempo      | RA           | 2024-02-18                |
      | a_tiempo      | LPE          | 2024-02-25                |
      | a_tiempo      | PNE          | 2024-02-25                |
    Y ha pasado <anios> años <meses> meses <semanas> semanas <dias> dias, desde su fecha listo para entregar
    Cuando el Vendedor visualice el resumen de los Pedidos en la etapa <etapa>
    Entonces se actualizarán los estados de los Pedidos según el tiempo que ha pasado
    Y se mostrara el estado <estado_pedido> con la siguiente cantidad de pedidos <numero_pedidos>
    Ejemplos:
      | anios | meses | semanas | dias | etapa | estado_pedido | numero_pedidos |
      | 1     | 0     | 1       | 5    | LPE   | AT            | 0              |
      | 1     | 0     | 1       | 5    | LPE   | A             | 1              |
      | 0     | 3     | 2       | 10   | RA    | A             | 1              |
      | 0     | 0     | 0       | 1    | RA    | AT            | 1              |
      | 0     | 0     | 0       | 11   | PNE   | AT             | 0              |


Esquema del escenario: : Visualizar resumen de pedidos en los cuales los clientes no han sido encontrados
    Dado que un Vendedor tiene los siguientes Pedidos registrados en estado PNE
      | estado_pedido | etapa_pedido | fecha_listo_para_entregar |
      | a_tiempo      | PNE          | 2024-02-18                |
      | atrasado      | PNE          | 2024-02-18                |
    Y los Pedidos estan registrados como cliente no encontrado
    Cuando el Vendedor visualice el resumen de los Pedidos en la etapa PNE
    Entonces se mostrara el estado <estado> con la siguiente cantidad de pedidos <numero_pedidos>
    Ejemplos:
      | numero_pedidos | estado |
      | 2              | CNE    |



