# Created by Natasha at 17/02/2024
# language: es
Característica: Promoción de productos
  Como vendedor
  quiero promocionar mis productos
  para aumentar mis ganancias.

     Esquema del escenario: Producto supera récord de ventas en su categoría
      Dado que existen "<producto>"que pertenecen a una "<categoria>" con <unidades_vendidas>
      Cuando las <unidades_vendidas> del "<producto>" superan el <recordDeVentas> de la "<categoria>"
      Entonces el "<producto>" se muestra en la sección de recomendados dentro de la "<categoria>" durante "<tiempo>"

  Ejemplos:
    | categoria     | recordDeVentas | producto        | tiempo |unidades_vendidas|
    | Electrónicos   | 100             | Smartphone X    |1 Semana|200             |
    | Ropa           | 50              | Camiseta Y      |2 dias     |80          |
    | Deportes       | 200             | Zapatillas Z    | 3 dias      |240        |
    | Hogar          | 80              | Aspiradora A    | 4 dias    |90          |


  Escenario: El vendedor paga para promocionar los productos
    Dado que existe un vendedor y su producto
    Cuando el vendedor realice un pago para promocionar su producto
    Entonces el producto se muestra al inicio de la lista de productos promocionados de esa categoría

