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
                    calificacion = Calificacion(cantidad_estrellas, identificador_producto)
                    calificacion.agregar_causas(causas)
                    producto.calificaciones_recibidas.append(calificacion)
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
            calificacion = Calificacion(cantidad_estrellas, 0)
            calificacion.agregar_causas(causas)
            servicio.calificaciones_recibidas.append(calificacion)
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
        self.calificaciones_recibidas = []
        self.calificaciones = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}

    def obtener_nombre_por_identificador(self, identificador):
        if identificador == self.identificador:
            return self.nombre



class Servicio:
    def __init__(self):
        self.calificaciones_recibidas = []
        self.calificaciones = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}

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


class Calificacion:
    def __init__(self, cantidad_estrellas, identificador_item_calificado):
        self.cantidad_estrellas = cantidad_estrellas
        self.causas = []
        self.item_calificado = identificador_item_calificado

    def agregar_causas(self, causas):
        self.causas = causas.split(",")

    def obtener_causas(self, identificador_item_calificado):
        if identificador_item_calificado == self.item_calificado:
            return self.causas

    def existen_causas(self, test, item_calificado, cantidad_estrellas):
        causas = ""
        if isinstance(test, Producto):
            for calificacion in test.calificaciones_recibidas:
                if calificacion.cantidad_estrellas == cantidad_estrellas:
                    for causa in calificacion.causas:
                        causas += causa
                else:
                    return ""
        elif isinstance(test, Servicio):
            for calificacion in test.calificaciones_recibidas:
                if calificacion.cantidad_estrellas == cantidad_estrellas:
                    for causa in calificacion.causas:
                        causas += causa
                else:
                    return ""
        return causas


    def mostrar_resultados_calificaciones(self, test, identificador_item):
        total_calificaciones = 0
        if isinstance(test, Producto):
            if identificador_item == 1:
                total_calificaciones = test.calificaciones[1] + test.calificaciones[2] + test.calificaciones[3] + test.calificaciones[4] + test.calificaciones[5]
                print(
                test.obtener_nombre_por_identificador(1) + "\n"
                + "1 estrella: " + str((test.calificaciones[1]/total_calificaciones)*100) + "% " + self.existen_causas(test,1,1) + "\n"
                + "2 estrellas: " + str((test.calificaciones[2]/total_calificaciones)*100) + "% " + self.existen_causas(test,1,2) + "\n"
                + "3 estrellas: " + str((test.calificaciones[3]/total_calificaciones)*100) + "% " + self.existen_causas(test,1,3) + "\n"
                + "4 estrellas: " + str((test.calificaciones[4]/total_calificaciones)*100) + "% " + self.existen_causas(test,1,4) + "\n"
                + "5 estrellas: " + str((test.calificaciones[5]/total_calificaciones)*100) + "% " + self.existen_causas(test,1,5) + "\n"
                )
            return True
        if isinstance(test, Servicio):
            if identificador_item == 0:
                total_calificaciones = test.calificaciones[1] + test.calificaciones[2] + test.calificaciones[3] + test.calificaciones[4] + test.calificaciones[5]
                print(
                    "Servicio\n" +
                    "1 estrella: " + str((test.calificaciones[1] / total_calificaciones) * 100) + "% " + self.existen_causas(test,0,1) + "\n" +
                    "2 estrellas: " + str((test.calificaciones[2] / total_calificaciones) * 100) + "% " + self.existen_causas(test,0,2) + "\n" +
                    "3 estrellas: " + str((test.calificaciones[3] / total_calificaciones) * 100) + "% " + self.existen_causas(test,0,3) + "\n" +
                    "4 estrellas: " + str((test.calificaciones[4] / total_calificaciones) * 100) + "% " + self.existen_causas(test,0,4) + "\n" +
                    "5 estrellas: " + str((test.calificaciones[5] / total_calificaciones) * 100) + "% " + self.existen_causas(test,0,5) + "\n"
                )
            return True
        if identificador_item == -1:

            return True