# Created by Natasha at 17/02/2024
# language: es
Característica: Promoción de productos
  Como vendedor
  quiero promocionar mis productos
  para aumentar mis ganancias.


  Escenario: El producto supera el récord de ventas de su categoría
    Dado que existen productos que pertenecen a una categoria con un record de ventas
    Cuando las unidades vendidas del producto superen el récord de ventas de su categoría
    Entonces el producto se asigna como recomendado dentro de su categoria durante una semana

  Escenario: El vendedor paga para promocionar sus productos
    Dado que existen vendedores que tienen productos que pertenecen a una sola categoría
      | nombre_vendedor | apellido_vendedor | nombre_producto | categoria                   |
      | Carlos          | Anchundia         | Martillo        | Herramientas_de_impacto     |
      | Rafael          | Correa            | Destornillador  | Herramientas_de_fijación    |
      | Rafael          | Piedra            | Sierra          | Herramientas_de_corte       |
      | Genesis         | Guachamin         | Taladro         | Herramientas_de_perforación |
    Dado que existen paquetes de promociones
      | tipo_promocion | costo | fecha_inicio | dias_duracion | cantidad_productos |
      | gold           | 50    | 26/02/2024   | 30            | 5                  |
      | platinum       | 35    | 26/02/2024   | 20            | 3                  |
      | basic          | 20    | 26/02/2024   | 15            | 1                  |
    Cuando los vendedores realicen un pago para promocionar sus productos
    Entonces se mostrará la sección de productos promocionados de la siguiente manera
      | nombre_producto | nombre_vendedor | apellido_vendedor |
      | Destornillador  | Rafael          | Correa            |
      | Sierra          | Rafael          | Piedra            |
      | Taladro         | Genesis         | Guachamin         |
      | Martillo        | Carlos          | Anchundia         |




