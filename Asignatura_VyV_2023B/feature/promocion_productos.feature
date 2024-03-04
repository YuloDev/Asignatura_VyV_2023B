# Created by Natasha at 17/02/2024
# language: es
Característica: Promoción de productos
  Como vendedor
  quiero promocionar mis productos
  para aumentar mis ganancias.

  Escenario: Producto supera récord de ventas en su categoría
    Dado que existen clientes con preferencias establecidas
      | cliente       | preferencias                        |
      | Rafael Piedra | categoria_x categoria_y categoria_z |
    Y que existen categorías con record de ventas
      | categoria   | record_ventas |
      | categoria_x | 100           |
      | categoria_y | 200           |
      | categoria_z | 300           |
    Y existen productos que pertenecen a una unica categoría con unidades vendidas
      | producto    | categoria   | unidades_vendidas |
      | Producto X1 | categoria_x | 202               |
      | Producto X2 | categoria_x | 30                |
      | Producto X3 | categoria_x | 40                |
      | Producto Y1 | categoria_y | 259               |
      | Producto Y2 | categoria_y | 104               |
      | Producto Y3 | categoria_y | 69                |
      | Producto Z1 | categoria_z | 502               |
      | Producto Z2 | categoria_z | 100               |
      | Producto Z3 | categoria_z | 200               |
    Y al menos una de las categorías pertenece a las preferencias del cliente
    Y las unidades vendidas de algun producto superan el record de ventas de la categoría
    Cuando se muestre la pagina principal del marketplace
    Entonces los productos que han superado el record de ventas y pertenecen a una categoría que está incluida en las preferencias del cliente se muestran en la seccion de productos destacados
    Y el record de ventas de la categoria se actualiza con el valor de las unidades vendidas del producto


  Escenario: El vendedor paga para promocionar sus productos
    Dado que existen vendedores que tienen productos
      | vendedor | nombres_productos                                                                            |
      | Carlos   | Martillo,Destornillador,Sierra                                                               |
      | Slayther | Llave ajustable,Taladro eléctrico,Serrucho de mano,Destornillador eléctrico,Lijadora orbital |
      | Juan     | Sierra Circular,Llave inglesa,Caja de herramientas,metro                                     |
    Y que existen paquetes de promociones
      | paquete  | costo | dias_duracion |
      | gold     | 50    | 30            |
      | platinum | 35    | 20            |
      | basic    | 20    | 15            |
    Y los vendedores adquieren un paquete de promoción
      | vendedor | paquete_contratado | producto_promocionado |
      | Carlos   | basic              | Martillo              |
      | Juan     | platinum           | Llave inglesa         |
      | Juan     | basic              | Caja de herramientas  |
      | Juan     | platinum           | Llave inglesa         |
      | Slayther | gold               | Llave ajustable       |
      | Slayther | basic              | Serrucho de mano      |
      | Slayther | gold               | Destornillador        |
    Cuando se realice una búsqueda de algún producto
    Entonces los productos promocionados se mostrarán como primer resultado en la búsqueda que coincida con el nombre del producto, ordenados por el tipo del paquete y la fecha de adquisición del paquete


