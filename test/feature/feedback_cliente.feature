#language:es
Característica: Recolección de feedback de compras de los clientes (servicio/producto)
  Como vendedor
  quiero que mis clientes puedan calificar el producto y el servicio después del proceso de compra de un producto
  para aprender de los resultados y mejorar la satisfacción de mis clientes.

  Esquema del escenario: Obtener feedback de calificaciones de los clientes
    Dado que el Cliente ha realizado el pago y el proceso de envío de la compra ha finalizado
    Cuando el Cliente envíe una Calificación de <cantidad_estrellas> estrellas del Producto y del Servicio, y mencione las <causas> de su Calificación.
    Entonces la valoración total de calificaciones del <item_de_calificacion> aumentará
    Y el vendedor podrá visualizar el porcentaje de calificaciones de cada cantidad de estrellas junto con los motivos correspondientes al <item_de_calificacion>.
    Ejemplos:
      | item_de_calificacion | causas | cantidad_estrellas |
      | Martillo | Buena calidad, Concuerda con la descripción | 5 |
      | Servicio | Paquete dañado, Entrega Tardía | 2 |