from django.db import models
from django.utils import timezone
from enum import Enum
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    record = models.IntegerField(default=0)

    def producto_supera_record(self, unidades_vendidas):
        if unidades_vendidas > self.record:
            self.record = unidades_vendidas
            self.save()
            return True
        else:
            return False


class Promocion(models.Model):
    TIPO_PROMOCION = (
        ('GD', 'Gold'),
        ('PG', 'Platinum'),
        ('BS', 'Basic'),
    )
    COSTO = (
        ('GD', 50),
        ('PG', 35),
        ('BS', 20),
    )

    fecha_inicio = models.DateField()
    tipo_promocion = models.CharField(max_length=2, choices=TIPO_PROMOCION)
    costo = models.CharField(max_length=2, choices=COSTO, default='BS')
    dias_duracion = models.IntegerField()
    cantidad_productos = models.IntegerField()


class Vendedor(models.Model):
    nombre = models.CharField(max_length=20)
    apellido = models.CharField(max_length=20)

    def agregar_producto(self, producto):
        self.productos.add(producto)
        self.save()

    def obtener_productos(self):
        return self.productos.all()

    def pagar_promocion(self, monto, producto):
        producto.promocion = True
        producto.save()

    def tiene_promocion_activa(self):
        return any(producto.promocion for producto in self.obtener_productos())


class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    unidades_vendidas = models.IntegerField()
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE, related_name='productos')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    promocion = models.BooleanField(default=False)

    def asignar_categoria(self, categoria):
        self.categoria = categoria
        self.save()

    def unidades_vendidas_ha_superado_record(self):
        return self.categoria.producto_supera_record(self.unidades_vendidas)

    def agregar_promocion(self):
        self.promocion = True
        self.save()

    def tiene_promocion(self):
        return self.promocion


##################################### CODIGO GRUPO 3 #####################################

# class ProductoG3(models.Model):
#     nombre_producto = models.CharField(max_length=100)
#     precio = models.DecimalField(max_digits=10, decimal_places=2)
#     costo = models.DecimalField(max_digits=10, decimal_places=2)
#
#     def obtener_precio(self):
#         return self.precio
#
#     def obtener_costo(self):
#         return self.costo
#
#
# class MetaG3(models.Model):
#     tipo_de_metrica = models.CharField(max_length=100)
#     valor = models.DecimalField(max_digits=10, decimal_places=2)
#     anio = models.PositiveIntegerField()
#     mes = models.PositiveIntegerField()
#
#     def obtener_tipo_de_metrica(self):
#         return self.tipo_de_metrica
#
#     def obtener_valor(self):
#         return self.valor
#
#     def obtener_anio(self):
#         return self.anio
#
#     def obtener_mes(self):
#         return self.mes
#
#
# class PedidoG3(models.Model):
#     lista_de_productos = models.ManyToManyField(ProductoG3)
#     fecha_listo_para_entregar = models.DateField(default=timezone.now)
#
#     def obtener_ingreso_total(self):
#         return sum(producto.obtener_precio() for producto in self.lista_de_productos.all())
#
#     def obtener_costo_total(self):
#         return sum(producto.obtener_costo() for producto in self.lista_de_productos.all())
#
#     def obtener_beneficio_total(self):
#         return self.obtener_ingreso_total() - self.obtener_costo_total()
#
#
# class VendedorG3(models.Model):
#     nombre = models.CharField(max_length=100)
#     metas = models.ManyToManyField(MetaG3)
#     lista_pedidos = models.ManyToManyField(PedidoG3)
#
#     def obtener_ventas(self):
#         return self.lista_pedidos.all()
#
#     def obtener_cantidad_de_ventas_por_fecha(self, anio=-1, mes=-1):
#         if anio == -1 or mes == -1:
#             return self.lista_pedidos.count()
#         else:
#             return self.lista_pedidos.filter(fecha__year=anio, fecha__month=mes).count()
#
#     def establecer_meta(self, meta):
#         self.metas.add(meta)
#
#     def obtener_meta(self, tipo_de_metrica, anio, mes):
#         meta = self.metas.filter(tipo_de_metrica=tipo_de_metrica, anio=anio, mes=mes).first()
#         return meta.valor if meta else -1
#
#
# class TipoDeMetricaG3(Enum):
#     NUMERO_DE_VENTAS = "Número de ventas"
#     INGRESOS = "Nuevos ingresos"
#     COSTOS = "Costos"
#     BENEFICIO_POR_VENTA = "Beneficio por venta"
#
#
# class RecomendacionG3(Enum):
#     OFERTA_DE_PRODUCTOS = "Crear oferta en los productos para generar más ventas."
#     MANTENER_PROMOCION_DE_PRODUCTOS = "Aumentar tu meta para el siguiente mes."
#     COMBO_DE_PRODUCTO = "Crear combos o conjunto de productos similares."
#     PROMOCION_PRODUCTOS_ESTRELLA = "Promocionar productos estrella."
#     NEGOCIAR_DESCUENTO = "Negociar descuentos con proveedores o buscar alternativas más económicas."
#     OPTIMIZAR_PROCESOS = "Optimizar procesos internos para reducir costos operativos."
#     AJUSTAR_PRECIO_SOBRE_COSTO = "Ajustar los precios de los productos con respecto a sus costos."
#     MANTENER_PRECIO_SOBRE_COSTO = "Mantener los precios de los productos con respecto a sus costos."
#
#
# class TipoDeComparacionG3(Enum):
#     INFERIOR = "son inferiores"
#     SUPERIOR = "superan"
#     IGUAL = "igualan"
#
#
# class DashboardDeMetricas():
#     def __init__(self):
#         self.metricas_actuales = {metrica: 0 for metrica in TipoDeMetricaG3}
#         self.metricas_mes_anterior = {metrica: 0 for metrica in TipoDeMetricaG3}
#         self.porcentajes_de_avance = {metrica: 0 for metrica in TipoDeMetricaG3}
#         self.recomendaciones = []
#         self.bandera_metrica = False
#         self.anio = 0
#         self.mes = 0
#
#     def generar_metricas(self, ventas, vendedor_id, anio, mes):
#         self.anio = anio
#         self.mes = mes
#         lista_de_ventas_ultimo_mes = ventas.all().obetnerPedidos(vendedor_id,anio,mes)
#         lista_de_ventas_mes_anterior = ventas.all().obetnerPedidos(vendedor_id, anio, mes - 1 if mes > 1 else 12)
#         metricas_actuales = self._calcular_metricas(lista_de_ventas_ultimo_mes)
#         metricas_mes_anterior = self._calcular_metricas(lista_de_ventas_mes_anterior)
#
#         self._actualizar_metricas_y_recomendaciones(metricas_actuales, metricas_mes_anterior)
#         self.bandera_metrica = True
#
#     def _calcular_metricas(self, lista_de_ventas):
#         metricas = {metrica: 0 for metrica in TipoDeMetricaG3}
#         beneficio_total = 0
#         for venta in lista_de_ventas:
#             metricas[TipoDeMetricaG3.NUMERO_DE_VENTAS] += 1
#             metricas[TipoDeMetricaG3.INGRESOS] += venta.obtener_ingreso_total()
#             metricas[TipoDeMetricaG3.COSTOS] += venta.obtener_costo_total()
#             beneficio_total += venta.obtener_beneficio_total()
#         if metricas[TipoDeMetricaG3.NUMERO_DE_VENTAS] > 0:
#             metricas[TipoDeMetricaG3.BENEFICIO_POR_VENTA] = beneficio_total / metricas[TipoDeMetricaG3.NUMERO_DE_VENTAS]
#         else:
#             metricas[TipoDeMetricaG3.BENEFICIO_POR_VENTA] = 0
#         return metricas
#
#     def _actualizar_metricas_y_recomendaciones(self, metricas_actuales, metricas_mes_anterior):
#         for metrica in TipoDeMetricaG3:
#             self.metricas_actuales[metrica] = metricas_actuales[metrica]
#             self.metricas_mes_anterior[metrica] = metricas_mes_anterior[metrica]
#
#             meta = self.vendedor.obtener_meta(metrica, self.anio, self.mes)
#             if meta is not None and meta != 0:
#                 porcentaje_de_avance = min(int(metricas_actuales[metrica] / meta * 100), 100)
#             else:
#                 porcentaje_de_avance = 0
#
#             self.porcentajes_de_avance[metrica] = porcentaje_de_avance
#
#             self._agregar_recomendacion(metrica)
#
#     def _agregar_recomendacion(self, tipo_de_metrica):
#         recomendaciones_por_metrica = {
#             TipoDeMetricaG3.NUMERO_DE_VENTAS: {
#                 'igual o superior': RecomendacionG3.MANTENER_PROMOCION_DE_PRODUCTOS,
#                 'inferior': RecomendacionG3.OFERTA_DE_PRODUCTOS
#             },
#             TipoDeMetricaG3.INGRESOS: {
#                 'igual o superior': RecomendacionG3.PROMOCION_PRODUCTOS_ESTRELLA,
#                 'inferior': RecomendacionG3.COMBO_DE_PRODUCTO
#             },
#             TipoDeMetricaG3.COSTOS: {
#                 'igual o superior': RecomendacionG3.OPTIMIZAR_PROCESOS,
#                 'inferior': RecomendacionG3.NEGOCIAR_DESCUENTO
#             },
#             TipoDeMetricaG3.BENEFICIO_POR_VENTA: {
#                 'igual o superior': RecomendacionG3.MANTENER_PRECIO_SOBRE_COSTO,
#                 'inferior': RecomendacionG3.AJUSTAR_PRECIO_SOBRE_COSTO
#             }
#         }
#         recomendacion_al_superar_o_igualar_la_meta = recomendaciones_por_metrica[tipo_de_metrica]['igual o superior']
#         recomendacion_al_no_superar_la_meta = recomendaciones_por_metrica[tipo_de_metrica]['inferior']
#         if self.obtener_comparacion_por_meta(
#                 tipo_de_metrica) is TipoDeComparacionG3.SUPERIOR or self.obtener_comparacion_por_meta(
#             tipo_de_metrica) is TipoDeComparacionG3.IGUAL:
#             self.recomendaciones.append(recomendacion_al_superar_o_igualar_la_meta)
#         else:
#             self.recomendaciones.append(recomendacion_al_no_superar_la_meta)
#
#     def obtener_metrica(self, tipo_de_metrica):
#         return self.metricas_actuales[tipo_de_metrica]
#
#     def se_realizaron_metricas(self):
#         return self.bandera_metrica
#
#     def obtener_comparacion_por_meta(self, tipo_de_metrica):
#         if self.metricas_actuales[tipo_de_metrica] > self.vendedor.obtener_meta(tipo_de_metrica, self.anio, self.mes):
#             return TipoDeComparacionG3.SUPERIOR
#         if self.metricas_actuales[tipo_de_metrica] == self.vendedor.obtener_meta(tipo_de_metrica, self.anio, self.mes):
#             return TipoDeComparacionG3.IGUAL
#         if self.metricas_actuales[tipo_de_metrica] < self.vendedor.obtener_meta(tipo_de_metrica, self.anio, self.mes):
#             return TipoDeComparacionG3.INFERIOR
#
#     def obtener_comparacion_por_mes_anterior(self, tipo_de_metrica):
#         if self.metricas_actuales[tipo_de_metrica] > self.metricas_mes_anterior[tipo_de_metrica]:
#             return TipoDeComparacionG3.SUPERIOR
#         if self.metricas_actuales[tipo_de_metrica] == self.metricas_mes_anterior[tipo_de_metrica]:
#             return TipoDeComparacionG3.IGUAL
#         if self.metricas_actuales[tipo_de_metrica] < self.metricas_mes_anterior[tipo_de_metrica]:
#             return TipoDeComparacionG3.INFERIOR
#
#     def obtener_porcentaje_de_avance(self, tipo_de_metrica):
#         return self.porcentajes_de_avance[tipo_de_metrica]
#
#     def obtener_recomendaciones(self):
#         return self.recomendaciones


class VendedorG3(models.Model):
    vendedorID = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

    def establecer_meta(self, meta):
        self.metas.add(meta)
        meta.save()

    def obtener_meta(self, tipo_de_metrica, anio, mes):
        meta = self.metas.filter(tipo_de_metrica=tipo_de_metrica, anio=anio, mes=mes).first()

        if meta is not None:
            return meta.valor
        else:
            return -1

    def obtener_ventas(self):
        return self.pedidos.all()

    def obtener_ventas_por_fecha(self, anio, mes):
        ventas_por_fecha = self.pedidos.filter(fecha_listo_para_entregar__year=anio,
                                               fecha_listo_para_entregar__month=mes)
        return ventas_por_fecha

    def obtener_cantidad_de_ventas_por_fecha(self, anio, mes):
        return self.obtener_ventas_por_fecha(anio, mes).count()

    def obtener_reporte(self, anio, mes):
        reportes = self.reportes.filter(anio=anio, mes=mes)

        if reportes.exists():
            reporte = reportes.first()
        else:
            reporte = self.reportes.create(anio=anio, mes=mes)

        reporte.determinar_metricas_y_recomendaciones()
        return reporte


class ProductoG3(models.Model):
    productoID = models.AutoField(primary_key=True)
    nombre_producto = models.CharField(max_length=100)
    precio = models.FloatField()
    costo = models.FloatField()
    vendedor = models.ForeignKey(VendedorG3, on_delete=models.CASCADE, related_name='productos')

    def __str__(self):
        return self.nombre_producto

    def obtener_precio(self):  # Necesario?
        return self.precio

    def obtener_costo(self):  # Necesario?
        return self.costo


class PedidoG3(models.Model):
    pedidoID = models.AutoField(primary_key=True)
    fecha_listo_para_entregar = models.DateField()
    vendedor = models.ForeignKey(VendedorG3, on_delete=models.CASCADE, related_name='pedidos')

    def obtener_ingreso_total(self):
        return sum(producto.obtener_precio_total() for producto in self.detalledepedidog3_set.all())

    def obtener_costo_total(self):
        return sum(producto.obtener_costo_total() for producto in self.detalledepedidog3_set.all())

    def obtener_beneficio_total(self):
        ingreso_total = self.obtener_ingreso_total()
        costo_total = self.obtener_costo_total()
        return ingreso_total - costo_total

    def __str__(self):
        return f"{self.pedidoID} / {self.fecha_listo_para_entregar} / {self.vendedor}"


class DetalleDePedidoG3(models.Model):
    pedido = models.ForeignKey(PedidoG3, on_delete=models.CASCADE)
    producto = models.ForeignKey(ProductoG3, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    def __str__(self):
        return f"{self.pedido.pedidoID} / {self.producto} / {self.cantidad}"


class TipoDeMetrica(models.TextChoices):
    NUMERO_DE_VENTAS = "NV", _("Número de ventas")
    INGRESOS = "IS", _("Ingresos")
    COSTOS = "CS", _("Costos")
    BENEFICIO_POR_VENTA = "BV", _("Beneficio por venta")


class MetaG3(models.Model):
    metaID = models.AutoField(primary_key=True)
    tipo_de_metrica = models.CharField(max_length=2, choices=TipoDeMetrica)
    valor = models.FloatField()
    anio = models.IntegerField()
    mes = models.IntegerField()
    vendedor = models.ForeignKey(VendedorG3, on_delete=models.CASCADE, related_name='metas')

    def obtener_tipo_de_metrica(self):  # Necesario?
        return self.tipo_de_metrica

    def obtener_valor(self):  # Necesario?
        return self.valor

    def obtener_anio(self):  # Necesario?
        return self.anio

    def obtener_mes(self):  # Necesario?
        return self.mes

    def __str__(self):
        return self.tipo_de_metrica


class TipoDeComparacion(models.TextChoices):
    INFERIOR = 'IR', _('son inferiores')
    SUPERIOR = 'SR', _('superan')
    IGUAL = 'IL', _('igualan')


class ReporteG3(models.Model):
    reporteID = models.AutoField(primary_key=True)
    vendedor = models.ForeignKey(VendedorG3, on_delete=models.CASCADE, related_name='reportes')
    anio = models.IntegerField()
    mes = models.IntegerField()

    def determinar_metricas_y_recomendaciones(self):
        for tipo_de_metrica in TipoDeMetrica:
            metrica = self.obtener_metrica(tipo_de_metrica)
            metrica.save()

        recomendaciones = self.obtener_recomendaciones()
        for recomendacion in recomendaciones:
            recomendacion.save()

    def obtener_metrica(self, tipo_de_metrica):
        metrica = self.metricas.filter(tipo_de_metrica=tipo_de_metrica, reporte=self).first()

        if not metrica:
            metrica = self.metricas.create(tipo_de_metrica=tipo_de_metrica, reporte=self)
            metrica.save()

        metrica.calcular_metrica(self.vendedor.obtener_ventas_por_fecha(self.anio, self.mes))
        return metrica

    def obtener_comparacion_por_meta(self, tipo_de_metrica):
        venta_misma_fecha = self.obtener_metrica(tipo_de_metrica)
        meta = self.vendedor.obtener_meta(tipo_de_metrica, venta_misma_fecha.anio, venta_misma_fecha.mes)

        if venta_misma_fecha.valor < meta:
            return TipoDeComparacion.INFERIOR.label
        elif venta_misma_fecha.valor > meta:
            return TipoDeComparacion.SUPERIOR.label
        else:
            return TipoDeComparacion.IGUAL.label

    def obtener_comparacion_por_mes_anterior(self, tipo_de_metrica):
        venta_misma_fecha = self.obtener_metrica(tipo_de_metrica)
        metrica_mes_anterior = self.obtener_metrica_mes_anterior(tipo_de_metrica)

        if venta_misma_fecha.valor < metrica_mes_anterior.valor:
            return TipoDeComparacion.INFERIOR.label
        elif venta_misma_fecha.valor > metrica_mes_anterior.valor:
            return TipoDeComparacion.SUPERIOR.label
        else:
            return TipoDeComparacion.IGUAL.label

    def obtener_metrica_mes_anterior(self, tipo_de_metrica):
        anio_anterior = self.vendedor.obtener_meta(tipo_de_metrica, self.anio, self.mes).obtener_anio_anterior()
        mes_anterior = self.vendedor.obtener_meta(tipo_de_metrica, self.anio, self.mes).obtener_mes_anterior()

        metrica_mes_anterior = self.metricas.filter(
            tipo_de_metrica=tipo_de_metrica,
            reporte__vendedor=self.vendedor,
            reporte__anio=anio_anterior,
            reporte__mes=mes_anterior
        ).first()

        if not metrica_mes_anterior:
            metrica_mes_anterior = self.metricas.create(
                tipo_de_metrica=tipo_de_metrica,
                reporte__vendedor=self.vendedor,
                reporte__anio=anio_anterior,
                reporte__mes=mes_anterior,
                valor=0
            )
            metrica_mes_anterior.save()

        return metrica_mes_anterior

    def obtener_recomendaciones(self):
        recomendaciones = []

        for tipo_de_metrica in TipoDeMetrica:
            comparacion_meta = self.obtener_comparacion_por_meta(tipo_de_metrica)

            recomendacion_existente = self.recomendaciones.filter(
                contenido=f'{tipo_de_metrica}'
            ).first()

            if not recomendacion_existente:
                recomendacion_existente = self.recomendaciones.create(
                    contenido=''
                )
            recomendacion_existente.determinar_contenido(comparacion_meta, tipo_de_metrica)
            recomendacion_existente.save()
            recomendaciones.append(recomendacion_existente)
            self.save()

        return recomendaciones

    def obtener_porcentaje_de_avance(self, tipo_de_metrica):
        meta = self.vendedor.obtener_meta(tipo_de_metrica, self.anio, self.mes)
        metrica_actual = self.obtener_metrica(tipo_de_metrica)
        if meta is not None and meta != 0:
            porcentaje_de_avance = min(int(metrica_actual / meta * 100), 100)
        else:
            porcentaje_de_avance = 0

        return porcentaje_de_avance

    def __str__(self):
        return f"{self.vendedor} / {self.anio} / {self.mes}"


class MetricaG3(models.Model):
    metricaID = models.AutoField(primary_key=True)
    tipo_de_metrica = models.CharField(max_length=19, choices=TipoDeMetrica)
    valor = models.FloatField()
    anio = models.IntegerField()
    mes = models.IntegerField()
    reporte = models.ForeignKey(ReporteG3, on_delete=models.CASCADE, related_name='metricas')

    def calcular_metrica(self, ventas):
        beneficio_total = 0
        cantidad_ventas = 0
        ingresos_total = 0
        costos_total = 0

        for venta in ventas:
            cantidad_ventas += 1
            ingresos_total += venta.obtener_ingreso_total()
            costos_total += venta.obtener_costo_total()
            beneficio_total += venta.obtener_beneficio_total()

        if self.tipo_de_metrica == TipoDeMetrica.NUMERO_DE_VENTAS:
            self.valor = cantidad_ventas
        elif self.tipo_de_metrica == TipoDeMetrica.INGRESOS:
            self.valor = ingresos_total
        elif self.tipo_de_metrica == TipoDeMetrica.COSTOS:
            self.valor = costos_total
        elif self.tipo_de_metrica == TipoDeMetrica.BENEFICIO_POR_VENTA and cantidad_ventas > 0:
            self.valor = beneficio_total / cantidad_ventas
        elif self.tipo_de_metrica == TipoDeMetrica.BENEFICIO_POR_VENTA:
            self.valor = 0

        self.save()

    def obtener_valor(self):
        return self.valor

    def __str__(self):
        return f"{self.tipo_de_metrica} / {self.valor}"


class TipoDeRecomendacion(models.TextChoices):
    OFERTA_DE_PRODUCTOS = 'OFERTA_DE_PRODUCTOS', _('Crear oferta en los productos para generar más ventas.')
    MANTENER_PROMOCION_DE_PRODUCTOS = 'MANTENER_PROMOCION_DE_PRODUCTOS', _('Aumentar tu meta para el siguiente mes.')
    COMBO_DE_PRODUCTO = 'COMBO_DE_PRODUCTO', _('Crear combos o conjunto de productos similares.')
    PROMOCION_PRODUCTOS_ESTRELLA = 'PROMOCION_PRODUCTOS_ESTRELLA', _('Promocionar productos estrella.')
    NEGOCIAR_DESCUENTO = 'NEGOCIAR_DESCUENTO', _(
        'Negociar descuentos con proveedores o buscar alternativas más económicas.')
    OPTIMIZAR_PROCESOS = 'OPTIMIZAR_PROCESOS', _('Optimizar procesos internos para reducir costos operativos.')
    AJUSTAR_PRECIO_SOBRE_COSTO = 'AJUSTAR_PRECIO_SOBRE_COSTO', _(
        'Ajustar los precios de los productos con respecto a sus costos.')
    MANTENER_PRECIO_SOBRE_COSTO = 'MANTENER_PRECIO_SOBRE_COSTO', _(
        'Mantener los precios de los productos con respecto a sus costos.')


class RecomendacionGR3(models.Model):
    contenido = models.CharField(max_length=31, choices=TipoDeRecomendacion)
    reporte = models.ForeignKey(ReporteG3, on_delete=models.CASCADE, related_name='recomendaciones')

    def determinar_contenido(self, comparacion_meta, tipo_de_metrica):
        recomendaciones_por_metrica = {
            TipoDeMetrica.NUMERO_DE_VENTAS: {
                'igual o superior': TipoDeRecomendacion.MANTENER_PROMOCION_DE_PRODUCTOS,
                'inferior': TipoDeRecomendacion.OFERTA_DE_PRODUCTOS
            },
            TipoDeMetrica.INGRESOS: {
                'igual o superior': TipoDeRecomendacion.PROMOCION_PRODUCTOS_ESTRELLA,
                'inferior': TipoDeRecomendacion.COMBO_DE_PRODUCTO
            },
            TipoDeMetrica.COSTOS: {
                'igual o superior': TipoDeRecomendacion.OPTIMIZAR_PROCESOS,
                'inferior': TipoDeRecomendacion.NEGOCIAR_DESCUENTO
            },
            TipoDeMetrica.BENEFICIO_POR_VENTA: {
                'igual o superior': TipoDeRecomendacion.MANTENER_PRECIO_SOBRE_COSTO,
                'inferior': TipoDeRecomendacion.AJUSTAR_PRECIO_SOBRE_COSTO
            }
        }

        recomendacion_al_superar_o_igualar_la_meta = recomendaciones_por_metrica[tipo_de_metrica]['igual o superior']
        recomendacion_al_no_superar_la_meta = recomendaciones_por_metrica[tipo_de_metrica]['inferior']

        if comparacion_meta == TipoDeComparacion.SUPERIOR or comparacion_meta == TipoDeComparacion.IGUAL:
            self.contenido = recomendacion_al_superar_o_igualar_la_meta
        else:
            self.contenido = recomendacion_al_no_superar_la_meta

    def obtener_contenido(self):
        return self.contenido

    def __str__(self):
        return f"{self.contenido}"
