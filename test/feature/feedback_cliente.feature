#language:es
Característica: Recolección de feedback de compras de los clientes (servicio/producto)
  Como vendedor
  quiero que mis clientes puedan calificar el producto y el servicio después del proceso de compra de un producto
  para aprender de los resultados y mejorar la satisfacción de mis clientes.

  Escenario: Obtener feedback de las calificaciones de los clientes sobre el servicio
    Dado que el Cliente ha dado su feedback sobre el producto
    Y se tiene un Servicio con las siguientes valoraciones totales
      | total_de_calificaciones | cantidad_de_estrellas | porcentaje_de_calificaciones |
      | 10                      | 1                     | 30%                          |
      | 6                       | 2                     | 18%                          |
      | 2                       | 3                     | 6%                           |
      | 5                       | 4                     | 15%                          |
      | 10                      | 5                     | 30%                          |
    Cuando el Cliente envíe una Calificación de tres sobre cinco estrellas del Servicio
    Y seleccione algunas de las siguientes causas de su Calificación para el Servicio
      | causas           |
      | Paquete dañado   |
      | Entrega tardía   |
      | Entrega a tiempo |
      | Entrega rápida   |
    Entonces la valoración total de calificaciones de 3 estrellas del Servicio aumentará en 1 de la siguiente manera
    Y el vendedor podrá visualizar el siguiente reporte con todas las causas en orden descendente
      | cantidad_de_estrellas | porcentaje_de_calificaciones | causas             |
      | 1                     | 29%                          |                    |
      | 2                     | 18%                          | Entrega tardía (1) |
      | 3                     | 9%                           | Paquete dañado (1) |
      | 4                     | 15%                          |                    |
      | 5                     | 29%                          |                    |