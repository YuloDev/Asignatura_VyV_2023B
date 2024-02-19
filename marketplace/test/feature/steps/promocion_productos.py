from behave import *
from marketplace.models import *

use_step_matcher("re")


class Vendedor:
    def __init__(self, nombre, apellido):
        self.promocion = False
        self.productos = []
        self.nombre = nombre
        self.apellido = apellido

    def agregar_producto(self, producto):
        self.productos.append(producto)

    def obtener_productos(self):
        return self.productos

    def pagar_promocion(self, monto, producto):
        producto.agregar_promocion()
        self.promocion = True

    def tiene_promocion_activa(self):
        return self.promocion


class Producto:
    def __init__(self, nombre):
        self.cantidad_venta = 10000
        self.categoria = None
        self.nombre = nombre
        self.promocion = False

    def asignar_categoria(self, categoria):
        self.categoria = categoria

    def ha_superado_record(self):
        return self.categoria.producto_supera_record(self.cantidad_venta)
    
    def agregar_promocion(self):
        self.promocion = True
        
    def tiene_promocion(self):
        return self.promocion

class Categoria:
    def __init__(self, record):
        self.record = record

    def producto_supera_record(self, cantidad_venta):
        if cantidad_venta > self.record:
            self.record = cantidad_venta
            return True
        else:
            return False



class Clasificador:
    def __init__(self):
        self.productos_promocionados = []
        self.productos_mas_vendidos = []
        self.vendedores = []

    def notificar(self, vendedor):
        pass

    def listar_productos_mas_vendidos(self):
        return self.productos_mas_vendidos

        pass

    def buscar_productos_mas_vendidos(self):
        for vendedor in self.vendedores:
            for producto in vendedor.obtener_productos():
                if producto.ha_superado_record():
                    self.productos_mas_vendidos.append(producto)

    def agregar_vendedor(self, vendedor):
        self.vendedores.append(vendedor)
        pass

    def buscar_productos_promocionados(self):
        for vendedor in self.vendedores:
            for producto in vendedor.obtener_productos():
                if producto.tiene_promocion():
                    self.productos_promocionados.append(producto)

    def listar_productos_destacados(self):
        return self.productos_promocionados



@step("que existe un vendedor y su producto")
def step_impl(context):
    context.vendedor = Vendedor(nombre="Rafael", apellido="Piedra")
    context.producto = Producto(nombre="Herramienta")
    context.vendedor.agregar_producto(context.producto)

    assert context.producto in context.vendedor.obtener_productos()


@step("ese producto supere el récord de ventas de su categoría")
def step_impl(context):
    context.categoria = Categoria(record=100)
    context.producto.asignar_categoria(context.categoria)

    assert context.producto.ha_superado_record() == True


@step("se informa al vendedor y muestra el producto en  la lista de productos más vendidos\.")
def step_impl(context):
    context.categoria = Categoria(record=100)
    context.producto.asignar_categoria(context.categoria)
    context.vendedor.agregar_producto(context.producto)
    context.clasificador = Clasificador()
    context.clasificador.agregar_vendedor(context.vendedor)
    context.clasificador.notificar(context.vendedor)
    context.clasificador.buscar_productos_mas_vendidos()

    assert context.producto in context.clasificador.listar_productos_mas_vendidos()


@step("el vendedor realice un pago para promocionar su producto")
def step_impl(context):
    context.vendedor = Vendedor(nombre="Rafael", apellido="Piedra")
    context.producto_promocionado = Producto(nombre="Herramienta2")
    context.vendedor.agregar_producto(context.producto_promocionado)
    context.vendedor.pagar_promocion(monto=10, producto=context.producto_promocionado)

    assert context.vendedor.tiene_promocion_activa() == True


@step("se destaca ese producto")
def step_impl(context):
    context.clasificador = Clasificador()
    context.vendedor = Vendedor(nombre="Rafael", apellido="Piedra")
    context.producto_promocionado = Producto(nombre="Herramienta2")
    context.vendedor.agregar_producto(context.producto_promocionado)
    context.vendedor.pagar_promocion(1008, producto=context.producto_promocionado)
    context.clasificador.agregar_vendedor(context.vendedor)
    context.clasificador.buscar_productos_promocionados()
    assert context.producto_promocionado in context.clasificador.listar_productos_destacados()

