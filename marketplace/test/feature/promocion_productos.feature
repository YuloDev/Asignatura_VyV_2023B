# Created by Natasha at 17/02/2024
# language: es
Característica: Promoción de productos
  Como vendedor
  quiero promocionar mis productos
  para aumentar mis ganancias.


  Escenario: El producto supera el récord de ventas de su categoría
    Dado que existe un vendedor y su producto
    Cuando ese producto supere el récord de ventas de su categoría
    Entonces se informa al vendedor y muestra el producto en  la lista de productos más vendidos.

  Escenario: El vendedor paga para promocionar los productos
    Cuando el vendedor realice un pago para promocionar su producto
    Entonces se destaca ese producto

