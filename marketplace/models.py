

# Create your models here.
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
    def __init__(self, nombre, unidades_vendidas):
        self.unidades_vendidas = unidades_vendidas
        self.categoria = None
        self.nombre = nombre
        self.supera_record = False
        self.promocion = False

    def asignar_categoria(self, categoria):
        self.categoria = categoria

    def unidades_vendidas_ha_superado_record(self,categoria):
        self.supera_record = categoria.producto_supera_record(self.unidades_vendidas)
        return self.supera_record

    def agregar_promocion(self):
        self.promocion = True

    def tiene_promocion(self):
        return self.promocion


class Categoria:
    def __init__(self, nombreCategoria, record):
        self.nombreCategoria = nombreCategoria
        self.record = record
        self.listaProductos = []

    def producto_supera_record(self,unidades_vendidas):
        if unidades_vendidas > self.record:
            return True
        else:
            return False

    def agregar_producto(self, producto):
        self.listaProductos.append(producto)

    def obtener_productos(self):
        return self.listaProductos


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


class Recomendacion:
    def __init__(self):
        self.recomendados_por_categoria = {}

    def asignar_recomendado(self, categoria,producto, duracion):

        if categoria not in self.recomendados_por_categoria:
            self.recomendados_por_categoria[categoria] = {}
        self.recomendados_por_categoria[categoria][producto] = duracion

    def obtener_recomendados(self):
        return self.recomendados_por_categoria
