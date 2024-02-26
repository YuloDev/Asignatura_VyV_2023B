class Producto:
    def __init__(self, id, nombre, descripcion):
        self.id_producto = id
        self.nombre_producto = nombre
        self.descripcion = descripcion

    def feedback_producto_esta_dado(self):
        return True


class Pedido:
    def __init__(self, id, estado, cantidad, direccion, productos):
        self.id_pedido = id
        self.estado = estado
        self.cantidad = cantidad
        self.direccion = direccion
        self.productos = productos
        self.servicio = Servicio(self)
        self.pagado = True

class Cliente:
    def __init__(self, cedula, nombre, apellido, correo, telefono, pedido):
        self.cedula = cedula
        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo
        self.telefono = telefono
        self.pedido = pedido

    def calificar_servicio(self, pedido, estrellas, causas, producto):
        calificacion = Calificacion(estrellas, causas, producto)
        pedido.servicio.agregar_calificacion(calificacion)

class Servicio:
    def __init__(self, pedido):
        self.pedido = pedido

        self.puntuaciones_calificaciones = [
            {'estrellas': 1, "cantidad": 10, "porcentaje": "30%"},
            {'estrellas': 2, "cantidad": 6, "porcentaje": "16%"},
            {'estrellas': 3, "cantidad": 2, "porcentaje": "6%"},
            {'estrellas': 4, "cantidad": 5, "porcentaje": "18"},
            {'estrellas': 5, "cantidad": 10, "porcentaje": "30%"}
        ]
        self.calificaciones_recibidas = list()

    def aumentar_estrella(self, calificacion_cliente):
        for calificacion in self.puntuaciones_calificaciones:
            if calificacion["estrellas"] == calificacion_cliente:
                calificacion["cantidad"] += 1
                break
        self.calcular_porcentajes()

    def agregar_calificacion(self, calificacion):
        self.calificaciones_recibidas.append(calificacion)
        self.aumentar_estrella(calificacion.estrellas)

    def calcular_porcentajes(self):
        total_estrellas = sum(calificacion["cantidad"] for calificacion in self.puntuaciones_calificaciones)
        for calificacion in self.puntuaciones_calificaciones:
            porcentaje_calculado = (calificacion["cantidad"] / total_estrellas) * 100
            porcentaje_calculado = round(porcentaje_calculado)
            calificacion["porcentaje"] = str(porcentaje_calculado) + "%"


class Calificacion:
    def __init__(self, estrellas, causas, producto):
        self.estrellas = estrellas
        self.causas = causas
        self.producto = producto