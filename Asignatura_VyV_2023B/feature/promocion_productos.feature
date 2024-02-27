# Created by Natasha at 17/02/2024
# language: es
Característica: Promoción de productos
  Como vendedor
  quiero promocionar mis productos
  para aumentar mis ganancias.


  Escenario: El producto supera el récord de ventas de su categoría
    Dado que existen productos que pertenecen a una categoria con un record de ventas
    Cuando las unidades vendidas del producto superen el récord de ventas de su categoría
    Entonces el producto se asigna como recomendado dentro de su categoria durante una semana

  Escenario: El vendedor paga para promocionar los productos
    Dado que existe un vendedor y su producto
    Cuando el vendedor realice un pago para promocionar su producto
    Entonces el producto se muestra al inicio de la lista de productos promocionados de esa categoría

