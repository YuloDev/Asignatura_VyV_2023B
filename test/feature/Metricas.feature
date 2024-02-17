# Created by Mateo at 17/02/2024
# language: es

Característica: Obtención de métricas de ventas mensualizadas por vendedor
  Como vendedor
  Quiero evaluar mi rendimiento mensual mediante [medidas]
  Para determinar posibles soluciones al presentarse un bajo rendimiento.

  Esquema del escenario: Vendedor evalúa su rendimiento
    Dado que un vendedor tiene X productos en N tiempo
    Cuando se despliegue el Dashboard de Métricas
    Entonces Se mostrará [medidas]
    Y si es <comparacion> a la meta actual se mostrará
    Y si es <comparacion> al mes anterior se mostrará
    Y se recomendará <recomendacion> al producto
    Ejemplos:
      | lapso_tiempo | comparacion | recomendacion         |
      | 6            | menores     | dar de baja           |
      | 3            | menores     | ajustar el precio     |
      | 6            | mayores     | darle más importancia |