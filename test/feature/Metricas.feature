# Created by Mateo at 17/02/2024
# language: es

Característica: Obtención de métricas de ventas mensualizadas por vendedor
  Como vendedor
  Quiero evaluar mi rendimiento mensual mediante las métricas: número de ventas, ingresos, costos, beneficio por venta
  Para determinar posibles soluciones al presentarse un bajo rendimiento.

  Esquema del escenario: Vendedor evalúa su rendimiento con el número de venta
    Dado que un vendedor realizó 4 ventas en diciembre y 2 ventas en noviembre
      | fecha      | producto               | costo | precio | cantidad |
      | 2023-12-01 | Teclado                | 10.0  | 15.0   | 2        |
      | 2023-12-02 | Cable USB              | 10.0  | 15.0   | 2        |
      | 2023-12-03 | Cafetera               | 10.0  | 15.0   | 2        |
      | 2023-12-04 | Memoria USB            | 10.0  | 15.0   | 2        |
      | 2023-11-05 | Refrigeración Liquida  | 10.0  | 15.0   | 2        |
      | 2023-11-06 | Cable de Interconexión | 10.0  | 15.0   | 2        |
    Y el vendedor estableció como meta de número de ventas para diciembre el valor <meta_ventas>
    Cuando se despliegue el Dashboard de Métricas en diciembre
    Entonces se mostrarán <ventas> ventas en diciembre
    Y se indicará, mediante porcentaje, que las ventas de diciembre <comparacion_por_meta> a la meta de ventas de diciembre
    Y se indicará, mediante porcentaje, que las ventas de diciembre <comparacion_por_mes> a las ventas de noviembre
    Y se recomendará <recomendacion>
    Ejemplos:
      | meta_ventas | ventas | comparacion_por_meta | comparacion_por_mes | recomendacion             |
      | 6           | 4      | son inferiores       | superan             | Crear oferta en los productos para generar más ventas. |
      | 2           | 4      | superan              | superan             | Aumentar tu meta para el siguiente mes.    |

  Esquema del escenario: Vendedor evalúa su rendimiento con los ingresos
    Dado que un vendedor realizó 4 ventas en diciembre y 2 ventas en noviembre
      | fecha      | producto               | costo | precio | cantidad |
      | 2023-12-01 | Teclado                | 10    | 15     | 2        |
      | 2023-12-02 | Cable USB              | 10    | 15     | 2        |
      | 2023-12-03 | Cafetera               | 10    | 15     | 2        |
      | 2023-12-04 | Memoria USB            | 10    | 15     | 2        |
      | 2023-11-05 | Refrigeración Liquida  | 10    | 15     | 2        |
      | 2023-11-06 | Cable de Interconexión | 10    | 15     | 2        |
    Y el vendedor estableció como meta de ingresos para diciembre la cantidad de <meta_ingresos> dólares
    Cuando se despliegue el Dashboard de Métricas en diciembre
    Entonces se mostrarán <ingresos> dólares de ingresos en diciembre
    Y se indicará, mediante porcentaje, que los ingresos de diciembre <comparacion_por_meta> a la meta de ingresos de diciembre
    Y se indicará, mediante porcentaje, que los ingresos de diciembre <comparacion_por_mes> a los ingresos de noviembre
    Y se recomendará <recomendacion>
    Ejemplos:
      | meta_ingresos | ingresos | comparacion_por_meta | comparacion_por_mes | recomendacion                            |
      | 140           | 120      | son inferiores       | superan             | Crear combos o conjunto de productos similares. |
      | 100           | 120      | superan              | superan             | Promocionar productos estrella. |

  Esquema del escenario: Vendedor evalúa su rendimiento con los costos
    Dado que un vendedor realizó 4 ventas en diciembre y 2 ventas en noviembre
      | fecha      | producto               | costo | precio | cantidad |
      | 2023-12-01 | Teclado                | 10    | 15     | 2        |
      | 2023-12-02 | Cable USB              | 10    | 15     | 2        |
      | 2023-12-03 | Cafetera               | 10    | 15     | 2        |
      | 2023-12-04 | Memoria USB            | 10    | 15     | 2        |
      | 2023-11-05 | Refrigeración Liquida  | 10    | 15     | 2        |
      | 2023-11-06 | Cable de Interconexión | 10    | 15     | 2        |
    Y el vendedor estableció como la meta de costos para diciembre la cantidad de <meta_costos> dólares
    Cuando se despliegue el Dashboard de Métricas en diciembre
    Entonces se mostrarán <costos> dólares de costos en diciembre
    Y se indicará, mediante porcentaje, que los costos de diciembre <comparacion_por_meta> a la meta de costos de diciembre
    Y se indicará, mediante porcentaje, que los costos de diciembre <comparacion_por_mes> a los costos de noviembre
    Y se recomendará <recomendacion>
    Ejemplos:
      | meta_costos | costos | comparacion_por_meta | comparacion_por_mes | recomendacion                    |
      | 100         | 80     | son inferiores       | superan             | Negociar descuentos con proveedores o buscar alternativas más económicas. |
      | 60          | 80     | superan              | superan             | Optimizar procesos internos para reducir costos operativos.  |

  Esquema del escenario: Vendedor evalúa su rendimiento con los beneficios por venta
    Dado que un vendedor realizó 4 ventas en diciembre y 2 ventas en noviembre
      | fecha      | producto               | costo | precio | cantidad |
      | 2023-12-01 | Teclado                | 10    | 15     | 2        |
      | 2023-12-02 | Cable USB              | 10    | 15     | 2        |
      | 2023-12-03 | Cafetera               | 10    | 15     | 2        |
      | 2023-12-04 | Memoria USB            | 10    | 15     | 2        |
      | 2023-11-05 | Refrigeración Liquida  | 10    | 15     | 2        |
      | 2023-11-06 | Cable de Interconexión | 10    | 15     | 2        |
    Y el vendedor estableció como meta de beneficio por venta para diciembre la cantidad de <meta_beneficio> dólares
    Cuando se despliegue el Dashboard de Métricas en diciembre
    Entonces se mostrarán <beneficio> dólares de beneficio por venta en diciembre
    Y se indicará, mediante porcentaje, que los beneficio por venta de diciembre <comparacion_por_meta> a la meta de los beneficios por venta de diciembre
    Y se indicará, mediante porcentaje, que los beneficio por venta de diciembre <comparacion_por_mes> a los beneficios por venta de noviembre
    Y se recomendará <recomendacion>
    Ejemplos:
      | meta_beneficio | beneficio | comparacion_por_meta | comparacion_por_mes | recomendacion                                     |
      | 12             | 10        | son inferiores       | superan             | Ajustar los precios de los productos con respecto a sus costos. |
      | 8              | 10        | superan              | superan             | Mantener los precios de los productos con respecto a sus costos. |

  Esquema del escenario: Vendedor evalúa su rendimiento con el número de venta, pero no realizó ventas el mes anterior y se impuso la meta de cero
    Dado que un vendedor realizó 4 ventas en diciembre y 0 ventas en noviembre
      | fecha      | producto               | costo | precio | cantidad |
      | 2023-12-01 | Teclado                | 10.0  | 15.0   | 2        |
      | 2023-12-02 | Cable USB              | 10.0  | 15.0   | 2        |
      | 2023-12-03 | Cafetera               | 10.0  | 15.0   | 2        |
      | 2023-12-04 | Memoria USB            | 10.0  | 15.0   | 2        |
    Y el vendedor estableció como meta de número de ventas para diciembre el valor <meta_ventas>
    Cuando se despliegue el Dashboard de Métricas en diciembre
    Entonces se mostrarán <ventas> ventas en diciembre
    Y se indicará que las ventas de diciembre <comparacion_por_meta> a la meta de ventas de diciembre
    Y se indicará que las ventas de diciembre <comparacion_por_mes> a las ventas de noviembre
    Y se recomendará <recomendacion>
    Ejemplos:
      | meta_ventas | ventas | comparacion_por_meta | comparacion_por_mes | recomendacion             |
      | 0           | 4      | superan              | superan             | Mantener promoción de productos que generan ventas.       |
