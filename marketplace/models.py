from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Vendedor(models.Model):
    vendedorID = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

    def establecer_meta(self, meta):
        self.metas.add(meta)
        meta.save()

    def obtener_meta(self, tipo_de_metrica, anio, mes):
        return self.metas.filter(tipo_de_metrica=tipo_de_metrica, anio=anio, mes=mes).first()

    def obtener_ventas(self):
        return self.pedidos.all()

    def obtener_ventas_por_fecha(self, anio, mes):
        ventas_por_fecha = self.pedidos.filter(fecha_listo_para_entregar__year=anio,
                                               fecha_listo_para_entregar__month=mes)
        return ventas_por_fecha

    def obtener_cantidad_de_ventas_por_fecha(self, anio, mes):
        return self.obtener_ventas_por_fecha(anio, mes).count()

    def generar_reporte(self, anio, mes):
        reportes = self.reportes.filter(anio=anio, mes=mes)

        if reportes.exists():
            reporte = reportes.first()
        else:
            reporte = self.reportes.create(anio=anio, mes=mes)

        reporte.determinar_metricas_y_recomendaciones()
        return reporte


class Producto(models.Model):
    productoID = models.AutoField(primary_key=True)
    nombre_producto = models.CharField(max_length=100)
    precio = models.FloatField()
    costo = models.FloatField()
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE, related_name='productos')

    def __str__(self):
        return self.nombre_producto

    def obtener_precio(self):  # Necesario?
        return self.precio

    def obtener_costo(self):  # Necesario?
        return self.costo


class Pedido(models.Model):
    pedidoID = models.AutoField(primary_key=True)
    fecha_listo_para_entregar = models.DateField()
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE, related_name='pedidos')

    def obtener_ingreso_total(self):
        return sum(producto.obtener_precio_total() for producto in self.detalles.all())

    def obtener_costo_total(self):
        return sum(producto.obtener_costo_total() for producto in self.detalles.all())

    def obtener_beneficio_total(self):
        ingreso_total = self.obtener_ingreso_total()
        costo_total = self.obtener_costo_total()
        return ingreso_total - costo_total

    def __str__(self):
        return f"{self.pedidoID} / {self.fecha_listo_para_entregar} / {self.vendedor}"


class DetalleDePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    def obtener_precio_total(self):
        return self.producto.precio * self.cantidad

    def obtener_costo_total(self):
        return self.producto.costo * self.cantidad

    def __str__(self):
        return f"{self.pedido.pedidoID} / {self.producto} / {self.cantidad}"


class TipoDeMetrica(models.TextChoices):
    NUMERO_DE_VENTAS = "NV", _("Número de ventas")
    INGRESOS = "IS", _("Ingresos")
    COSTOS = "CS", _("Costos")
    BENEFICIO_POR_VENTA = "BV", _("Beneficio por venta")


class Meta(models.Model):
    metaID = models.AutoField(primary_key=True)
    tipo_de_metrica = models.CharField(max_length=2, choices=TipoDeMetrica)
    valor = models.FloatField(null=True)
    anio = models.IntegerField(null=True)
    mes = models.IntegerField(null=True)
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE, related_name='metas')

    def obtener_tipo_de_metrica(self):  # Necesario?
        return self.tipo_de_metrica

    def obtener_valor(self):  # Necesario?
        return self.valor

    def obtener_anio(self):  # Necesario?
        return self.anio

    def obtener_mes(self):  # Necesario?
        return self.mes

    def __str__(self):
        return f"{self.tipo_de_metrica} / {self.valor}"


class TipoDeComparacion(models.TextChoices):
    INFERIOR = 'IR', _('son inferiores')
    SUPERIOR = 'SR', _('superan')
    IGUAL = 'IL', _('igualan')


class Reporte(models.Model):
    reporteID = models.AutoField(primary_key=True)
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE, related_name='reportes')
    anio = models.IntegerField(null=True)
    mes = models.IntegerField(null=True)

    def determinar_metricas_y_recomendaciones(self):
        for tipo_de_metrica in TipoDeMetrica:
            metrica = self.obtener_metrica(tipo_de_metrica)
            metrica.save()

        recomendaciones = self.obtener_recomendaciones()

    def obtener_metrica(self, tipo_de_metrica):
        metrica = self.metricas.filter(tipo_de_metrica=tipo_de_metrica, reporte=self).first()

        if not metrica:
            metrica = self.metricas.create(tipo_de_metrica=tipo_de_metrica, anio=self.anio, mes=self.anio, reporte=self)
            metrica.save()

        metrica.calcular_metrica(self.vendedor.obtener_ventas_por_fecha(self.anio, self.mes))
        return metrica

    def obtener_comparacion_por_meta(self, tipo_de_metrica):
        metrica = self.obtener_metrica(tipo_de_metrica)
        meta = self.vendedor.obtener_meta(tipo_de_metrica, self.anio, self.mes)
        if meta is not None:
            if metrica.obtener_valor() < meta.obtener_valor():
                return TipoDeComparacion.INFERIOR.label
            elif metrica.obtener_valor() > meta.obtener_valor():
                return TipoDeComparacion.SUPERIOR.label
            else:
                return TipoDeComparacion.IGUAL.label

    def obtener_comparacion_por_mes_anterior(self, tipo_de_metrica):
        metrica_mes_actual = self.obtener_metrica(tipo_de_metrica)
        metrica_mes_anterior = self.obtener_metrica_mes_anterior(tipo_de_metrica)

        if metrica_mes_actual.obtener_valor() < metrica_mes_anterior.obtener_valor():
            return TipoDeComparacion.INFERIOR.label
        elif metrica_mes_actual.obtener_valor() > metrica_mes_anterior.obtener_valor():
            return TipoDeComparacion.SUPERIOR.label
        else:
            return TipoDeComparacion.IGUAL.label

    def obtener_metrica_mes_anterior(self, tipo_de_metrica):
        anio_anterior = self.anio if self.mes > 1 else self.anio - 1
        mes_anterior = self.mes - 1 if self.mes > 1 else 12

        metrica_mes_anterior = self.vendedor.generar_reporte(anio_anterior,mes_anterior).obtener_metrica(tipo_de_metrica)

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
            recomendaciones.append(recomendacion_existente.obtener_contenido().label)
            self.save()

        return recomendaciones

    def obtener_porcentaje_de_avance(self, tipo_de_metrica):
        meta = self.vendedor.obtener_meta(tipo_de_metrica, self.anio, self.mes)
        metrica_actual = self.obtener_metrica(tipo_de_metrica)
        if meta is not None and meta.obtener_valor() != 0:
            porcentaje_de_avance = min(int(metrica_actual.obtener_valor() / meta.obtener_valor() * 100), 100)
        else:
            porcentaje_de_avance = 0

        return porcentaje_de_avance

    def __str__(self):
        return f"{self.vendedor} / {self.anio} / {self.mes}"


class Metrica(models.Model):
    metricaID = models.AutoField(primary_key=True)
    tipo_de_metrica = models.CharField(max_length=19, choices=TipoDeMetrica)
    valor = models.FloatField(null=True)
    anio = models.IntegerField(null=True)
    mes = models.IntegerField(null=True)
    reporte = models.ForeignKey(Reporte, on_delete=models.CASCADE, related_name='metricas')

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

        if cantidad_ventas == 0:
            self.valor = 0
        elif self.tipo_de_metrica == TipoDeMetrica.NUMERO_DE_VENTAS:
            self.valor = cantidad_ventas
        elif self.tipo_de_metrica == TipoDeMetrica.INGRESOS:
            self.valor = ingresos_total
        elif self.tipo_de_metrica == TipoDeMetrica.COSTOS:
            self.valor = costos_total
        elif self.tipo_de_metrica == TipoDeMetrica.BENEFICIO_POR_VENTA and cantidad_ventas > 0:
            self.valor = beneficio_total / cantidad_ventas

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


class Recomendacion(models.Model):
    contenido = models.CharField(max_length=31, choices=TipoDeRecomendacion)
    reporte = models.ForeignKey(Reporte, on_delete=models.CASCADE, related_name='recomendaciones')

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

        if comparacion_meta == TipoDeComparacion.SUPERIOR.label or comparacion_meta == TipoDeComparacion.IGUAL.label:
            self.contenido = recomendacion_al_superar_o_igualar_la_meta
        else:
            self.contenido = recomendacion_al_no_superar_la_meta

    def obtener_contenido(self):
        return self.contenido

    def __str__(self):
        return f"{self.contenido}"
