#language:es
Característica: Recolección de feedback de compras de los clientes (servicio/producto)
  Como vendedor
  quiero que mis clientes puedan calificar el producto y el servicio después del proceso de compra de un producto
  para aprender de los resultados y mejorar la satisfacción de mis clientes.

  Escenario: Obtener feedback de las calificaciones de los clientes sobre el producto
    Dado que el Cliente ha realizado el pago y el proceso de envío de la compra ha finalizado
    Y se tiene un Producto con las siguientes valoraciones totales
      | total_de_calificaciones | cantidad_de_estrellas | porcentaje_de_calificaciones |
      | 0                       | 1                     | 0%                           |
      | 1                       | 2                     | 20%                          |
      | 2                       | 3                     | 40%                          |
      | 0                       | 4                     | 0%                           |
      | 2                       | 5                     | 40%                          |
    Cuando el Cliente seleccione una Calificación de tres sobre cinco estrellas del Producto y seleccione la causa 2, 8 de las siguientes causas de su Calificación
      | No. | causas                          |
      | 1   | Buenos acabados                 |
      | 2   | Concuerda con la descripción    |
      | 3   | Buena calidad de materiales     |
      | 4   | Buen funcionamiento             |
      | 5   | No concuerda con la descripción |
      | 6   | Mala calidad de materiales      |
      | 7   | Malos acabados                  |
      | 8   | Mal funcionamiento              |
    Entonces el vendedor podrá visualizar el siguiente reporte del Producto con todas las causas en orden descendente
      | cantidad_de_estrellas | porcentaje_de_calificaciones | causas                                               |
      | 1                     | 0%                           |                                                      |
      | 2                     | 17%                          | Mala calidad de materiales (1)                                                |
      | 3                     | 50%                          | Concuerda con la descripción (3), Mal funcionamiento (2), Buenos acabados (1) |
      | 4                     | 0%                           |                                                      |
      | 5                     | 33%                          | Buenos acabados (2), Buena calidad de materiales (2)                          |


  Escenario: Obtener feedback de las calificaciones de los clientes sobre el servicio
    Dado que el Cliente ha dado su feedback sobre el producto
    Y se tiene un Servicio con las siguientes valoraciones totales
      | total_de_calificaciones | cantidad_de_estrellas | porcentaje_de_calificaciones |
      | 10                      | 1                     | 30%                          |
      | 6                       | 2                     | 18%                          |
      | 2                       | 3                     | 6%                           |
      | 5                       | 4                     | 15%                          |
      | 10                      | 5                     | 30%                          |
    Cuando el Cliente seleccione una Calificación de tres sobre cinco estrellas del Servicio y seleccione la causa 1 de las siguientes causas de su Calificación
      | No. | causas           |
      | 1   | Paquete dañado   |
      | 2   | Entrega tardía   |
      | 3   | Entrega a tiempo |
      | 4   | Entrega rápida   |
    Entonces el vendedor podrá visualizar el siguiente reporte del Servicio con todas las causas en orden descendente
      | cantidad_de_estrellas | porcentaje_de_calificaciones | causas             |
      | 1                     | 29%                          |                    |
      | 2                     | 18%                          | Entrega tardía (1) |
      | 3                     | 9%                           | Paquete dañado (1) |
      | 4                     | 15%                          |                    |
      | 5                     | 29%                          |                    |