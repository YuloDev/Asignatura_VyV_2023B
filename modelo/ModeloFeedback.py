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

    def calificar_servicio(self, identificador_pedido, cantidad_estrellas, causas):
        pedido = self.encontrar_pedido_por_identificador(identificador_pedido)
        servicio = pedido.servicio
        if pedido:
            #calificacion = Calificacion(cantidad_estrellas, 0)
            #calificacion.agregar_causas(causas)
            #servicio.calificaciones_recibidas.append(calificacion)
        else:
            print(f"No se encontró un pedido con identificador {identificador_pedido}")
    def encontrar_pedido_por_identificador(self, identificador_pedido):
        for pedido in self.pedidos:
            if pedido.identificador == identificador_pedido:
                return pedido
        return None


class Producto:
    def __init__(self, identificador, nombre, descripcion):
        self.identificador = identificador
        self.nombre = nombre
        self.descripcion = descripcion

    def obtener_nombre_por_identificador(self, identificador):
        if identificador == self.identificador:
            return self.nombre



class Servicio:
    def __init__(self):
        pass

    def agregar_motivo_calificacion(self, motivo_calificacion):
        self.motivos_calificacion.append(motivo_calificacion)

    def obtener_motivos_calificacion_servicio(self):
        return self.motivos_calificacion


class Pedido:
    def __init__(self, identificador, estado, cantidad, direccion, productos, servicio):
        self.identificador = identificador
        self.estado = estado
        self.cantidad = cantidad
        self.direccion = direccion
        self.productos = productos
        self.servicio = servicio
        self.pagado = True