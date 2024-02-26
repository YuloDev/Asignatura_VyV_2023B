from datetime import date
from enum import Enum


class Producto:
    def __init__(self, nombre, precio, costo):
        self.nombre = nombre
        self.precio = precio
        self.costo = costo

    def obtener_precio(self):
        return self.precio

    def obtener_costo(self):
        return self.costo

class Meta:
    def __init__(self, tipo_de_metrica, valor, anio, mes):
        self.tipo_de_metrica = tipo_de_metrica
        self.valor = valor
        self.anio = anio
        self.mes = mes

    def obtener_tipo_de_metrica(self):
        return self.tipo_de_metrica

    def obtener_valor(self):
        return self.valor

    def obtener_anio(self):
        return self.anio

    def obtener_mes(self):
        return self.mes


class Vendedor:
    def __init__(self, nombre):
        self.nombre = nombre
        self.metas = []
        self.ventas = []

    def vender(self, lista_de_productos, anio, mes, dia):
        self.ventas.append(Venta(lista_de_productos, date(anio, mes, dia)))

    def obtener_ventas(self):
        return self.ventas

    def establecer_meta(self, meta):
        self.metas.append(meta)

    def obtener_meta(self, tipo_de_metrica, anio, mes):
        for meta in self.metas:
            if tipo_de_metrica == meta.obtener_tipo_de_metrica() and meta.obtener_anio() == anio and meta.obtener_mes() == mes:
                return meta.obtener_valor()
        return -1


class Venta:
    def __init__(self, lista_de_productos, fecha):
        self.lista_de_productos = lista_de_productos
        self.ingreso_total = sum(producto.obtener_precio() for producto in lista_de_productos)
        self.costo_total = sum(producto.obtener_costo() for producto in lista_de_productos)
        self.beneficio_total = self.ingreso_total - self.costo_total
        self.fecha = fecha

    def obtener_ingreso_total(self):
        return self.ingreso_total

    def obtener_costo_total(self):
        return self.costo_total

    def obtener_beneficio_total(self):
        return self.beneficio_total


class Dashboard:
    def __init__(self, vendedor):
        self.vendedor = vendedor
        self.metricas_actuales = {metrica: 0 for metrica in TipoDeMetrica}
        self.metricas_mes_anterior = {metrica: 0 for metrica in TipoDeMetrica}
        self.porcentajes_comparacion_meta = {metrica: 0 for metrica in TipoDeMetrica}
        self.porcentajes_comparacion_mes_anterior = {metrica: 0 for metrica in TipoDeMetrica}
        self.recomendaciones = []
        self.bandera_metrica = False
        self.anio = 0
        self.mes = 0

    def generar_metricas(self, anio, mes):
        self.anio = anio
        self.mes = mes
        lista_de_ventas = self.vendedor.obtener_ventas()

        metricas_actuales = self._calcular_metricas(lista_de_ventas, mes)
        metricas_mes_anterior = self._calcular_metricas(lista_de_ventas, mes - 1 if mes > 1 else 12)

        self._actualizar_metricas_y_recomendaciones(metricas_actuales, metricas_mes_anterior)
        self.bandera_metrica = True

    def _calcular_metricas(self, lista_de_ventas, mes):
        metricas = {metrica: 0 for metrica in TipoDeMetrica}
        for venta in lista_de_ventas:
            if venta.fecha.year == self.anio and venta.fecha.month == mes:
                metricas[TipoDeMetrica.NUMERO_DE_VENTAS] += 1
                metricas[TipoDeMetrica.INGRESOS] += venta.obtener_ingreso_total()
                metricas[TipoDeMetrica.COSTOS] += venta.obtener_costo_total()
                metricas[TipoDeMetrica.BENEFICIO_POR_VENTA] = (
                    metricas[TipoDeMetrica.BENEFICIO_POR_VENTA] * (metricas[TipoDeMetrica.NUMERO_DE_VENTAS] - 1) +
                    venta.obtener_beneficio_total()) / metricas[TipoDeMetrica.NUMERO_DE_VENTAS]
        return metricas

    def _actualizar_metricas_y_recomendaciones(self, metricas_actuales, metricas_mes_anterior):
        for metrica in TipoDeMetrica:
            self.metricas_actuales[metrica] = metricas_actuales[metrica]
            self.metricas_mes_anterior[metrica] = metricas_mes_anterior[metrica]

            meta = self.vendedor.obtener_meta(metrica, self.anio, self.mes)
            porcentaje_comparacion_meta = int((metricas_actuales[metrica] / meta - 1) * 100)
            porcentaje_comparacion_mes_anterior = int(
                (metricas_actuales[metrica] / metricas_mes_anterior[metrica] - 1) * 100)

            self.porcentajes_comparacion_meta[metrica] = porcentaje_comparacion_meta
            self.porcentajes_comparacion_mes_anterior[metrica] = porcentaje_comparacion_mes_anterior

            self._agregar_recomendacion(metrica, porcentaje_comparacion_meta)

    def _agregar_recomendacion(self, tipo_de_metrica, porcentaje_comparacion_meta):
        recomendaciones_por_metrica = {
            TipoDeMetrica.NUMERO_DE_VENTAS: {
                'superior': Recomendacion.MANTENER_PROMOCION_DE_PRODUCTOS,
                'inferior': Recomendacion.OFERTA_DE_PRODUCTOS
            },
            TipoDeMetrica.INGRESOS: {
                'superior': Recomendacion.PROMOCION_PRODUCTOS_ESTRELLA,
                'inferior': Recomendacion.COMBO_DE_PRODUCTO
            },
            TipoDeMetrica.COSTOS: {
                'superior': Recomendacion.OPTIMIZAR_PROCESOS,
                'inferior': Recomendacion.NEGOCIAR_DESCUENTO
            },
            TipoDeMetrica.BENEFICIO_POR_VENTA: {
                'superior': Recomendacion.MANTENER_PRECIO_SOBRE_COSTO,
                'inferior': Recomendacion.AJUSTAR_PRECIO_SOBRE_COSTO
            }
        }
        recomendacion_al_superar_la_meta = recomendaciones_por_metrica[tipo_de_metrica]['superior']
        recomendacion_al_no_superar_la_meta = recomendaciones_por_metrica[tipo_de_metrica]['inferior']
        if porcentaje_comparacion_meta >= 0:
            self.recomendaciones.append(recomendacion_al_superar_la_meta)
        else:
            self.recomendaciones.append(recomendacion_al_no_superar_la_meta)

    def obtener_metrica(self, tipo_de_metrica):
        return self.metricas_actuales[tipo_de_metrica]

    def se_realizaron_metricas(self):
        return self.bandera_metrica

    def obtener_comparacion_por_meta(self, tipo_de_metrica):
        if self.porcentajes_comparacion_meta[tipo_de_metrica] >= 0:
            return TipoDeComparacion.SUPERIOR
        else:
            return TipoDeComparacion.INFERIOR

    def obtener_comparacion_por_mes_anterior(self, tipo_de_metrica):
        if self.porcentajes_comparacion_mes_anterior[tipo_de_metrica] >= 0:
            return TipoDeComparacion.SUPERIOR
        else:
            return TipoDeComparacion.INFERIOR

    def obtener_recomendaciones(self):
        return self.recomendaciones


class TipoDeMetrica(Enum):
    NUMERO_DE_VENTAS = "Número de ventas"
    INGRESOS = "Nuevos ingresos"
    COSTOS = "Costos"
    BENEFICIO_POR_VENTA = "Beneficio por venta"


class Recomendacion(Enum):
    OFERTA_DE_PRODUCTOS = "Crear oferta en los productos para generar más ventas."
    MANTENER_PROMOCION_DE_PRODUCTOS = "Aumentar tu meta para el siguiente mes."
    COMBO_DE_PRODUCTO = "Crear combos o conjunto de productos similares."
    PROMOCION_PRODUCTOS_ESTRELLA = "Promocionar productos estrella."
    NEGOCIAR_DESCUENTO = "Negociar descuentos con proveedores o buscar alternativas más económicas."
    OPTIMIZAR_PROCESOS = "Optimizar procesos internos para reducir costos operativos. "
    AJUSTAR_PRECIO_SOBRE_COSTO = "Ajustar los precios de los productos con respecto a sus costos."
    MANTENER_PRECIO_SOBRE_COSTO = "Mantener los precios de los productos con respecto a sus costos."


class TipoDeComparacion(Enum):
    INFERIOR = "son inferiores"
    SUPERIOR = "superan"
    IGUAL = "igual"
