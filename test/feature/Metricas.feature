# Created by Mateo at 17/02/2024
# language: es

Característica: Obtención de métricas de ventas mensualizadas por vendedor
  Como vendedor
  Quiero evaluar mi rendimiento mensual mediante las métricas: número de ventas, ingresos, costos, beneficio por venta
  Para determinar posibles soluciones al presentarse un bajo rendimiento.

  Esquema del escenario: Vendedor evalúa su rendimiento con el número de ventas
    Dado que un vendedor tiene 6 ventas
      | fecha      | producto               | costo | precio | cantidad |
      | 2023-12-01 | Teclado                | 10.0  | 15.0   | 2        |
      | 2023-12-02 | Cable USB              | 10.0  | 15.0   | 2        |
      | 2023-12-03 | Cafetera               | 10.0  | 15.0   | 2        |
      | 2023-12-04 | Memoria USB            | 10.0  | 15.0   | 2        |
      | 2023-11-05 | Refrigeración Liquida  | 10.0  | 15.0   | 2        |
      | 2023-11-06 | Cable de Interconexión | 10.0  | 15.0   | 2        |
    Y el vendedor estableció <meta_ventas> ventas como la meta de número de ventas para diciembre
    Cuando se despliegue el Dashboard de Métricas en diciembre
    Entonces se mostrarán <ventas> ventas
    Y se indicará, mediante porcentaje, que las ventas de diciembre <comparacion_por_meta> a la meta de ventas de diciembre
    Y se indicará, mediante porcentaje, que las ventas de diciembre <comparacion_por_mes> a las ventas de noviembre
    Y se recomendará <recomendacion>
    Ejemplos:
      | meta_ventas | ventas | comparacion_por_meta | comparacion_por_mes | recomendacion                    |
      | 6           | 4      | son inferiores       | superan             | ajustar precios de los productos |
      | 2           | 4      | superan              | superan             | promocionar productos            |

  Esquema del escenario: Vendedor evalúa su rendimiento con los ingresos
    Dado que un vendedor tiene 6 ventas
      | fecha      | producto               | costo | precio | cantidad |
      | 2023-12-01 | Teclado                | 10    | 15     | 2        |
      | 2023-12-02 | Cable USB              | 10    | 15     | 2        |
      | 2023-12-03 | Cafetera               | 10    | 15     | 2        |
      | 2023-12-04 | Memoria USB            | 10    | 15     | 2        |
      | 2023-11-05 | Refrigeración Liquida  | 10    | 15     | 2        |
      | 2023-11-06 | Cable de Interconexión | 10    | 15     | 2        |
    Y el vendedor estableció <meta_ingresos> dolares como la meta de ingresos para diciembre
    Cuando se despliegue el Dashboard de Métricas en diciembre
    Entonces se mostrarán <ingresos> dolares de ingresos
    Y se indicará, mediante porcentaje, que los ingresos de diciembre <comparacion_por_meta> a la meta de ingresos de diciembre
    Y se indicará, mediante porcentaje, que los ingresos de diciembre <comparacion_por_mes> a los ingresos de noviembre
    Y se recomendará <recomendacion>
    Ejemplos:
      | meta_ingresos | ingresos | comparacion_por_meta | comparacion_por_mes | recomendacion                            |
      | 140           | 120      | son inferiores       | superan             | promocionar más productos                |
      | 100           | 120      | superan              | superan             | mantener la promoción productos estrella |

  Esquema del escenario: Vendedor evalúa su rendimiento con los costos
    Dado que un vendedor tiene 6 ventas
      | fecha      | producto               | costo | precio | cantidad |
      | 2023-12-01 | Teclado                | 10    | 15     | 2        |
      | 2023-12-02 | Cable USB              | 10    | 15     | 2        |
      | 2023-12-03 | Cafetera               | 10    | 15     | 2        |
      | 2023-12-04 | Memoria USB            | 10    | 15     | 2        |
      | 2023-11-05 | Refrigeración Liquida  | 10    | 15     | 2        |
      | 2023-11-06 | Cable de Interconexión | 10    | 15     | 2        |
    Y el vendedor estableció <meta_costos> dolares como la meta de costos para diciembre
    Cuando se despliegue el Dashboard de Métricas en diciembre
    Entonces se mostrarán <costos> dolares de costos
    Y se indicará, mediante porcentaje, que los costos de diciembre <comparacion_por_meta> a la meta de costos de diciembre
    Y se indicará, mediante porcentaje, que los costos de diciembre <comparacion_por_mes> a los costos de noviembre
    Y se recomendará <recomendacion>
    Ejemplos:
      | meta_costos | costos | comparacion_por_meta | comparacion_por_mes | recomendacion                    |
      | 100         | 80     | son inferiores       | superan             | mantener costos de los productos |
      | 60          | 80     | superan              | superan             | reducir costos de los productos  |

  Esquema del escenario: Vendedor evalúa su rendimiento con los beneficios por venta
    Dado que un vendedor tiene 6 ventas
      | fecha      | producto               | costo | precio | cantidad |
      | 2023-12-01 | Teclado                | 10    | 15     | 2        |
      | 2023-12-02 | Cable USB              | 10    | 15     | 2        |
      | 2023-12-03 | Cafetera               | 10    | 15     | 2        |
      | 2023-12-04 | Memoria USB            | 10    | 15     | 2        |
      | 2023-11-05 | Refrigeración Liquida  | 10    | 15     | 2        |
      | 2023-11-06 | Cable de Interconexión | 10    | 15     | 2        |
    Y el vendedor estableció <meta_beneficio> dolares como la meta de beneficio por venta para diciembre
    Cuando se despliegue el Dashboard de Métricas en diciembre
    Entonces se mostrarán <beneficio> dolares de beneficio por venta
    Y se indicará, mediante porcentaje, que los beneficio por venta de diciembre <comparacion_por_meta> a la meta de los beneficios por venta de diciembre
    Y se indicará, mediante porcentaje, que los beneficio por venta de diciembre <comparacion_por_mes> a los beneficios por venta de noviembre
    Y se recomendará <recomendacion>
    Ejemplos:
      | meta_beneficio | beneficio | comparacion_por_meta | comparacion_por_mes | recomendacion                                     |
      | 12             | 10        | son inferiores       | superan             | ajustar precios sobre los costos de los productos |
      | 8              | 10        | superan              | superan             | promocionar productos estrella                    |
