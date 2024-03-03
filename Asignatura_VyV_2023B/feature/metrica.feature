# Created by Mateo at 17/02/2024
# language: es

Característica: Obtención de métricas de ventas mensualizadas por vendedor
  Como vendedor
  Quiero evaluar mi rendimiento mensual mediante las métricas: número de ventas, ingresos, costos, beneficio por venta
  Para determinar posibles soluciones al presentarse un bajo rendimiento.

  Esquema del escenario: Vendedor evalúa su rendimiento con el número de venta
    Dado que un vendedor realizó <ventas_mes_actual> ventas en el mes actual, diciembre, de productos cuyo costo y precio fueron 10 y 15, respectivamente, y <ventas_mes_anterior> ventas en el mes anterior de productos cuyo costo y precio fueron 10 y 15, respectivamente
    Y el vendedor estableció como meta de número de ventas para el mes actual el valor <meta_ventas>
    Cuando se despliegue el Dashboard de Métricas
    Entonces se mostrarán <ventas> ventas
    Y se indicará que las ventas del mes actual <comparacion_por_meta> a la meta de ventas del mes actual, con el porcentaje de avance <porcentaje>%
    Y se indicará que las ventas del mes actual <comparacion_por_mes> a las ventas del mes anterior
    Y se recomendará <recomendacion>
    Ejemplos:
      | ventas_mes_actual | ventas_mes_anterior | meta_ventas | ventas | comparacion_por_meta | comparacion_por_mes | recomendacion                                          | porcentaje |
      | 4                 | 3                   | 5           | 4      | son inferiores       | superan             | Crear oferta en los productos para generar más ventas. | 80         |
      | 4                 | 5                   | 5           | 4      | son inferiores       | son inferiores      | Crear oferta en los productos para generar más ventas. | 80         |
      | 4                 | 4                   | 5           | 4      | son inferiores       | igualan             | Crear oferta en los productos para generar más ventas. | 80         |
      | 4                 | 3                   | 3           | 4      | superan              | superan             | Aumentar tu meta para el siguiente mes.                | 100        |
      | 4                 | 3                   | 4           | 4      | igualan              | superan             | Aumentar tu meta para el siguiente mes.                | 100        |
      | 4                 | 3                   | 0           | 4      | superan              | superan             | Aumentar tu meta para el siguiente mes.                | 0          |
      | 4                 | 0                   | 3           | 4      | superan              | superan             | Aumentar tu meta para el siguiente mes.                | 100        |

  Esquema del escenario: Vendedor evalúa su rendimiento con los ingresos
    Dado que un vendedor realizó <ventas_mes_actual> ventas en el mes actual, diciembre, de productos cuyo costo y precio fueron 10 y 15, respectivamente, y <ventas_mes_anterior> ventas en el mes anterior de productos cuyo costo y precio fueron 10 y 15, respectivamente
    Y el vendedor estableció como meta de ingresos para el mes actual la cantidad de <meta_ingresos> dólares
    Cuando se despliegue el Dashboard de Métricas
    Entonces se mostrarán <ingresos> dólares de ingresos
    Y se indicará que los ingresos del mes actual <comparacion_por_meta> a la meta de ingresos del mes actual, con el porcentaje de avance <porcentaje>%
    Y se indicará que los ingresos del mes actual <comparacion_por_mes> a los ingresos del mes anterior
    Y se recomendará <recomendacion>
    Ejemplos:
      | ventas_mes_actual | ventas_mes_anterior | meta_ingresos | ingresos | comparacion_por_meta | comparacion_por_mes | recomendacion                                   | porcentaje |
      | 4                 | 3                   | 61            | 60       | son inferiores       | superan             | Crear combos o conjunto de productos similares. | 98         |
      | 4                 | 5                   | 61            | 60       | son inferiores       | son inferiores      | Crear combos o conjunto de productos similares. | 98         |
      | 4                 | 4                   | 61            | 60       | son inferiores       | igualan             | Crear combos o conjunto de productos similares. | 98         |
      | 4                 | 3                   | 59            | 60       | superan              | superan             | Promocionar productos estrella.                 | 100        |
      | 4                 | 3                   | 60            | 60       | igualan              | superan             | Promocionar productos estrella.                 | 100        |
      | 4                 | 3                   | 0             | 60       | superan              | superan             | Promocionar productos estrella.                 | 0          |
      | 4                 | 0                   | 59            | 60       | superan              | superan             | Promocionar productos estrella.                 | 100        |

  Esquema del escenario: Vendedor evalúa su rendimiento con los costos
    Dado que un vendedor realizó <ventas_mes_actual> ventas en el mes actual, diciembre, de productos cuyo costo y precio fueron 10 y 15, respectivamente, y <ventas_mes_anterior> ventas en el mes anterior de productos cuyo costo y precio fueron 10 y 15, respectivamente
    Y el vendedor estableció como la meta de costos para el mes actual la cantidad de <meta_costos> dólares
    Cuando se despliegue el Dashboard de Métricas
    Entonces se mostrarán <costos> dólares de costos
    Y se indicará que los costos del mes actual <comparacion_por_meta> a la meta de costos del mes actual, con el porcentaje de avance <porcentaje>%
    Y se indicará que los costos del mes actual <comparacion_por_mes> a los costos del mes anterior
    Y se recomendará <recomendacion>
    Ejemplos:
      | ventas_mes_actual | ventas_mes_anterior | meta_costos | costos | comparacion_por_meta | comparacion_por_mes | recomendacion                                                             | porcentaje |
      | 4                 | 3                   | 41          | 40     | son inferiores       | superan             | Negociar descuentos con proveedores o buscar alternativas más económicas. | 97         |
      | 4                 | 5                   | 41          | 40     | son inferiores       | son inferiores      | Negociar descuentos con proveedores o buscar alternativas más económicas. | 97         |
      | 4                 | 4                   | 41          | 40     | son inferiores       | igualan             | Negociar descuentos con proveedores o buscar alternativas más económicas. | 97         |
      | 4                 | 3                   | 39          | 40     | superan              | superan             | Optimizar procesos internos para reducir costos operativos.               | 100        |
      | 4                 | 3                   | 40          | 40     | igualan              | superan             | Optimizar procesos internos para reducir costos operativos.               | 100        |
      | 4                 | 3                   | 0           | 40     | superan              | superan             | Optimizar procesos internos para reducir costos operativos.               | 0          |
      | 4                 | 0                   | 39          | 40     | superan              | superan             | Optimizar procesos internos para reducir costos operativos.               | 100        |

  Esquema del escenario: Vendedor evalúa su rendimiento con los beneficios por venta
    Dado que un vendedor realizó 4 ventas en el mes actual, diciembre, de productos cuyo costo y precio fueron 10 y <precio_mes_actual>, respectivamente, y 4 ventas en el mes anterior de productos cuyo costo y precio fueron 10 y <precio_mes_anterior>, respectivamente
    Y el vendedor estableció como meta de beneficio por venta para el mes actual la cantidad de <meta_beneficio> dólares
    Cuando se despliegue el Dashboard de Métricas
    Entonces se mostrarán <beneficio> dólares de beneficio por venta
    Y se indicará que los beneficio por venta del mes actual <comparacion_por_meta> a la meta de los beneficios por venta del mes actual, con el porcentaje de avance <porcentaje>%
    Y se indicará que los beneficio por venta del mes actual <comparacion_por_mes> a los beneficios por venta del mes anterior
    Y se recomendará <recomendacion>
    Ejemplos:
      | precio_mes_actual | precio_mes_anterior | meta_beneficio | beneficio | comparacion_por_meta | comparacion_por_mes | recomendacion                                                    | porcentaje |
      | 15                | 14                  | 6              | 5         | son inferiores       | superan             | Ajustar los precios de los productos con respecto a sus costos.  | 83         |
      | 15                | 16                  | 6              | 5         | son inferiores       | son inferiores      | Ajustar los precios de los productos con respecto a sus costos.  | 83         |
      | 15                | 15                  | 6              | 5         | son inferiores       | igualan             | Ajustar los precios de los productos con respecto a sus costos.  | 83         |
      | 15                | 14                  | 4              | 5         | superan              | superan             | Mantener los precios de los productos con respecto a sus costos. | 100        |
      | 15                | 14                  | 5              | 5         | igualan              | superan             | Mantener los precios de los productos con respecto a sus costos. | 100        |
      | 15                | 14                  | 0              | 5         | superan              | superan             | Mantener los precios de los productos con respecto a sus costos. | 0          |
      | 15                | 10                  | 4              | 5         | superan              | superan             | Mantener los precios de los productos con respecto a sus costos. | 100        |
