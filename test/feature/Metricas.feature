# Created by Mateo at 17/02/2024
# language: es

Característica: Obtención de métricas de ventas mensualizadas por vendedor
  Como vendedor
  Quiero evaluar mi rendimiento mensual mediante las métricas: el número de ventas, ingresos, costos, beneficio por venta
  Para determinar posibles soluciones al presentarse un bajo rendimiento.

  Esquema del escenario: Vendedor evalúa su rendimiento
    Dado que un vendedor tiene 4 productos vendidos en diciembre
    Y el vendedor estableció las metas: número de ventas, ingresos, costos y beneficio por venta para diciembre
    Cuando se despliegue el Dashboard de Métricas en diciembre
    Entonces se mostrará el número de ventas, ingresos, costos, beneficio por venta de diciembre
    Y se indicará que las métricas de diciembre <comparacion_por_meta> las metas de diciembre mediante un porcentaje
    Y se indicará que las métricas de diciembre <comparacion_por_mes> las métricas de noviembre mediante un porcentaje
    Y se recomendará <recomendacion>
    Ejemplos:
      | comparacion_por_meta | comparacion_por_mes | recomendacion                    |
      | son infreriores      | superan             | ajustar precios de los productos |
      | superan              | superan             | promocionar productos            |