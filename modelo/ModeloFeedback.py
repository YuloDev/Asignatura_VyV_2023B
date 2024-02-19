class Cliente:
    def __init__(self, identificador, nombres, apellidos, correoElectronico, numeroTelefonico, pedido):
        self.identificador = identificador
        self.nombres = nombres
        self.apellidos = apellidos
        self.correoElectronico = correoElectronico
        self.numeroTelefonico = numeroTelefonico
        self.pedidos = [pedido]

    def calificar_producto(self, identificador_pedido, identificador_producto, cantidad_estrellas, causas):
        pedido = self.encontrar_pedido_por_identificador(identificador_pedido)
        if pedido:
            producto_encontrado = None
            for producto in pedido.productos:
                if producto.identificador == identificador_producto:
                    #calificacion = Calificacion(cantidad_estrellas, identificador_producto)
                    #calificacion.agregar_causas(causas)
                    #producto.calificaciones_recibidas.append(calificacion)
                    break
                if not producto_encontrado:
                    print(
                        f"No se encontró un producto con identificador {identificador_producto} en el pedido {identificador_pedido}")
        else:
            print(f"No se encontró un pedido con identificador {identificador_pedido}")


class Producto:
    def __init__(self, identificador, nombre, descripcion):
        self.identificador = identificador
        self.nombre = nombre
        self.descripcion = descripcion



class Servicio:
    def __init__(self):


class Pedido:
    def __init__(self, identificador, estado, cantidad, direccion, productos, servicio):
        self.identificador = identificador
        self.estado = estado
        self.cantidad = cantidad
        self.direccion = direccion
        self.productos = productos
        self.servicio = servicio
        self.pagado = True