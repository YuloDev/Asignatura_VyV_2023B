from enum import Enum


class Producto:
    def __init__(self, precio, costo):
        self.precio = precio
        self.costo = costo


class Metrica:
    def __init__(self, tipo, valor, fecha):
        self.tipo = tipo
        self.valor = valor
        self.fecha = fecha


class Vendedor:
    def __init__(self, nombre):
        self.nombre = nombre
        self.metas = []
        self.venta = []
        self.numero_ventas = 0
        self.metricas = []

    def vender(self, lista_producto, fecha):
        self.numero_ventas += 1
        self.venta.append(Venta(lista_producto, fecha))

    def obtener_dashboard(self, fecha):
        """
        Todo
        """
        pass


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


class TipoDeMetrica(Enum):
    NUMERO_DE_VENTAS = "Número de ventas"
    NUEVOS_INGRESOS = "Nuevos ingresos"
    COSTOS = "Costos"
    BENEFICIO_POR_VENTA = "Beneficio por venta"
