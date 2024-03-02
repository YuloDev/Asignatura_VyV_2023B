# Created by Natasha at 17/02/2024
# language: es
Característica: Promoción de productos
  Como vendedor
  quiero promocionar mis productos
  para aumentar mis ganancias.

  Escenario: Producto supera récord de ventas en su categoría
    Dado que existen "<cliente>" con "<preferencias>"
      | cliente       | preferencias                          |
      | Rafael Piedra | categoria_x, categoria_y, categoria_z |
    Y "<producto>" con "<unidades_vendidas>"que pertenece a una única "<categoria>" que tiene un "<record_ventas>"
      | producto     | categoria   | record_ventas | unidades_vendidas |
      | Smartphone X | categoria_x | 200           | 300               |
    Cuando las <unidades_vendidas> del "<producto>" superan el <record_ventas> de la "<categoria>"
    Y la "<categoría>" de ese "<producto>" pertenece a las "<preferencias>" del "<cliente>"
    Entonces en la parte superior de la ventana principal del marketplace se muestran las "<categoria>" pertenecientes a las "<preferencias>" del "<cliente>" con el "<producto>" que superó el "<record_ventas>"
    Y el "<record_ventas>" de la "<categoria>" se actualiza con el valor de las "<unidades_vendidas>" del "<producto>"


  Escenario: El vendedor paga para promocionar los productos
    Dado que existe un vendedor y su producto
    Cuando el vendedor realice un pago para promocionar su producto
    Entonces el producto se muestra al inicio de la lista de productos promocionados de esa categoría

