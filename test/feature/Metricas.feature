# Created by Mateo at 17/02/2024
# language: es

Característica: Obtención de métricas de ventas mensualizadas por vendedor
  Como vendedor
  Quiero evaluar mi rendimiento mensual mediante las métricas: el número de ventas, nuevos ingresos, costos, beneficio por venta
  Para determinar posibles soluciones al presentarse un bajo rendimiento.

  Esquema del escenario: Vendedor evalúa su rendimiento
    Dado que un vendedor tiene <cantidad> productos vendidos
    Y el vendedor tiene una meta para cada métrica en el mes de diciembre
    Cuando se despliegue el Dashboard de Métricas de diciembre
    Entonces se mostrará el número de ventas, nuevos ingresos, costos, beneficio por venta de diciembre
    Y se indicará la diferencia, como porcentaje, en la que los valores reales de las métricas <comparación> las metas
    Y se indicará la diferencia, como porcentaje, en la que los valores reales de las métricas de diciembre <comparación> las valores reales de las métricas de noviembre
    Y se recomendará <recomendacion>
    Ejemplos:
      | cantidad | comparacion | recomendacion                    |
      | 2        |             | ajustar precios de los productos |
      | 4        |             | promocionar productos            |