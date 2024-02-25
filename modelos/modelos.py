from datetime import date
from enum import Enum


class Producto:
    def __init__(self, nombre, precio, costo):
        self.nombre = nombre
        self.precio = precio
        self.costo = costo


class Meta:
    def __init__(self, tipo_de_metrica, valor, anio, mes):
        self.tipo_de_metrica = tipo_de_metrica
        self.valor = valor
        self.anio = anio
        self.mes = mes


class Vendedor:
    def __init__(self, nombre):
        self.nombre = nombre
        self.metas = []
        self.venta = []

    def vender(self, lista_producto, anio, mes, dia):
        self.venta.append(Venta(lista_producto, date(anio, mes, dia)))

    def obtener_ventas(self):
        return self.venta

    def establecer_meta(self, meta):
        self.metas.append(meta)

    def obtener_meta(self, tipo_de_metrica, anio, mes):
        for meta in self.metas:
            if tipo_de_metrica == meta.tipo_de_metrica and meta.anio == anio and meta.mes == mes:
                return meta.valor
            else:
                return -1


class Venta:
    def __init__(self, lista_producto, fecha):
        self.lista_productos = lista_producto
        self.ingreso_total = 0
        self.calcular_ingreso_total()
        self.costo_total = 0
        self.calcular_costo_total()
        self.beneficio_total = 0
        self.calcular_beneficio_total()
        self.fecha = fecha

    def calcular_ingreso_total(self):
        for producto in self.lista_productos:
            self.ingreso_total += producto.precio

    def calcular_costo_total(self):
        for producto in self.lista_productos:
            self.costo_total += producto.costo

    def calcular_beneficio_total(self):
        self.beneficio_total = self.ingreso_total - self.costo_total


class Dashboard:
    def __init__(self, vendedor):
        self.vendedor = vendedor
        self.metricas_actuales = {
            TipoDeMetrica.NUMERO_DE_VENTAS: 0,
            TipoDeMetrica.INGRESOS: 0,
            TipoDeMetrica.COSTOS: 0,
            TipoDeMetrica.BENEFICIO_POR_VENTA: 0
        }
        self.metricas_mes_anterior = {
            TipoDeMetrica.NUMERO_DE_VENTAS: 0,
            TipoDeMetrica.INGRESOS: 0,
            TipoDeMetrica.COSTOS: 0,
            TipoDeMetrica.BENEFICIO_POR_VENTA: 0
        }
        self.porcentajes_comparacion_meta = {
            TipoDeMetrica.NUMERO_DE_VENTAS: 0,
            TipoDeMetrica.INGRESOS: 0,
            TipoDeMetrica.COSTOS: 0,
            TipoDeMetrica.BENEFICIO_POR_VENTA: 0
        }
        self.porcentajes_comparacion_mes_anterior = {
            TipoDeMetrica.NUMERO_DE_VENTAS: 0,
            TipoDeMetrica.INGRESOS: 0,
            TipoDeMetrica.COSTOS: 0,
            TipoDeMetrica.BENEFICIO_POR_VENTA: 0
        }
        self.bandera_metrica = False
        self.anio = 0
        self.mes = 0

    def generar_metricas(self, anio, mes):
        self.anio = anio
        self.mes = mes
        lista_de_ventas = self.vendedor.obtener_ventas()
        numero_de_ventas_actuales = 0
        numero_de_ventas_mes_anterior = 0
        mes_anterior = mes - 1
        if mes_anterior == 0:
            mes_anterior = 12
            anio -= 1
        for venta in lista_de_ventas:
            if (venta.fecha.year == anio) and (venta.fecha.month == mes):
                numero_de_ventas_actuales += 1
            if (venta.fecha.year == anio) and (venta.fecha.month == mes_anterior):
                numero_de_ventas_mes_anterior += 1
        self.metricas_actuales[TipoDeMetrica.NUMERO_DE_VENTAS] = numero_de_ventas_actuales
        self.metricas_mes_anterior[TipoDeMetrica.NUMERO_DE_VENTAS] = numero_de_ventas_mes_anterior
        meta_ventas = self.vendedor.obtener_meta(TipoDeMetrica.NUMERO_DE_VENTAS, self.anio, self.mes)
        self.porcentajes_comparacion_meta[TipoDeMetrica.NUMERO_DE_VENTAS] = int((numero_de_ventas_actuales / meta_ventas - 1) * 100)
        self.porcentajes_comparacion_mes_anterior[TipoDeMetrica.NUMERO_DE_VENTAS] = int(
            ((numero_de_ventas_actuales / numero_de_ventas_mes_anterior) - 1) * 100)
        self.bandera_metrica = True

    def obtener_ventas(self):
        return self.vendedor.obtener_ventas()
    def se_realizaron_metricas(self):
        return self.bandera_metrica

    def obtener_comparacion_por_meta(self, tipo_de_metrica):
        if self.porcentajes_comparacion_meta[tipo_de_metrica] >= 0:
            return TipoDeComparacion.SUPERIOR
        else:
            return TipoDeComparacion.INFERIOR

    def obtener_comparacion_por_mes(self, tipo_de_metrica):
        if self.porcentajes_comparacion_mes_anterior[tipo_de_metrica] >= 0:
            return TipoDeComparacion.SUPERIOR
        else:
            return TipoDeComparacion.INFERIOR


class TipoDeMetrica(Enum):
    NUMERO_DE_VENTAS = "Número de ventas"
    INGRESOS = "Nuevos ingresos"
    COSTOS = "Costos"
    BENEFICIO_POR_VENTA = "Beneficio por venta"


class TipoDeRecomendacion(Enum):
    INFERIOR_A_META_DE_VENTAS = "ajustar precios de los productos"
    SUPERIOR_A_META_DE_VENTAS = "promocionar productos"


class TipoDeComparacion(Enum):
    INFERIOR = "son inferiores"
    SUPERIOR = "superan"
