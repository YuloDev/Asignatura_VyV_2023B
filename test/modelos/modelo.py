from enum import Enum

# Definicion de la clase Vendedor
class Vendedor:
    # Constructor
    def __init__(self, nombre_vendedor):
        self.nombre_vendedor = nombre_vendedor
        self.pedidos = []  # Inicializa la lista de pedidos del vendedor

#Este metodo pueden cambiar a su criterio
    def agregar_pedido(self, pedido):
        # Método para agregar un pedido a la lista de pedidos del vendedor
        self.pedidos.append(pedido)

    # Este metodo pueden cambiar a su criterio
    def visualizar_resumen(self):
        pass


# Definicion de la clase ResumenSeguimiento
class ResumenSeguimiento:
    def __init__(self, nombre_etapa, tiempo_etapa, num_pedido_cancelados, num_pedidos_atrasados, num_pedidos_a_tiempo):
        self.nombre_etapa = nombre_etapa
        self.tiempo_etapa = tiempo_etapa

        self.num_pedido_cancelados = num_pedido_cancelados
        self.num_pedidos_atrasados = num_pedidos_atrasados
        self.num_pedidos_a_tiempo = num_pedidos_a_tiempo

        self.num_pedidos_total = None  # Inicializamos la variable total_pedidos como None

    # Este metodo pueden cambiar a su criterio
    def visualizar_graficas(self):
        pass

    def sumar_pedidos(self):
        self.total_pedidos = self.num_pedidos_atrasados + self.num_pedidos_a_tiempo + self.num_pedido_cancelados
        return self.total_pedidos

# Arreglo de instancias de ResumenSeguimiento con diferentes datos
resumenes = [
    ResumenSeguimiento("PreCompra", 2, 2, 3, 13),
    ResumenSeguimiento("Reserva", 4, 0, 1, 11),
    ResumenSeguimiento("ListoDespacho", 2, 1, 2, 5)
]


# Definicion de la clase Pedido
class Pedido:
    # Constructor
    def __init__(self, nombre_pedido, tiempo_pedidoPC, tiempo_pedidoR, tiempo_pedidoAT, estadoAnulado):
        self.nombre_pedido = nombre_pedido
        self.estado_pedido = None  # Inicializa el atributo estado_pedido como None
        self.tiempo_pedidoPC = tiempo_pedidoPC
        self.tiempo_pedidoR = tiempo_pedidoR
        self.tiempo_pedidoAT = tiempo_pedidoAT
        self.estadoAnulado = None

    # Este metodo pueden cambiar a su criterio, nosotros medio le adelatamos la logica pensandole algo asi, pero pueden cambiarle dependiendo lo que necesiten
    # Método para cambiar el estado de un pedido
    def cambiar_estado(self, estadoAnulado, nombre_etapa):
        if nombre_etapa == "PreCompra" and estadoAnulado == "Vigente":
            if self.tiempo_pedidoPC <= 2:
                self.estado_pedido = "A tiempo"
            else:
                self.estado_pedido = "Atrasado"
        elif nombre_etapa == "Reserva" and estadoAnulado == "Vigente":
            if self.tiempo_pedidoR <= 4:
                self.estado_pedido = "A tiempo"
            else:
                self.estado_pedido = "Atrasado"
        elif nombre_etapa == "ListoDespacho" and estadoAnulado == "Vigente":
            if self.tiempo_pedidoAT <= 2:
                self.estado_pedido = "A tiempo"
            else:
                self.estado_pedido = "Atrasado"
        else:
            self.estado_pedido = "Anulado"


# Definicion de la clase Etapa
class Etapa:
    # Constructor
    def __init__(self, nombre_etapa, tiempo_etapa):
        self.nombre_etapa = nombre_etapa
        self.pedidos = []  # Inicializa la lista de pedidos de la etapa
        self.tiempo_etapa = tiempo_etapa

    # Este metodo pueden cambiar a su criterio
    def agregar_pedido(self, pedido):
        # Método para agregar un pedido a la lista de pedidos de la etapa
        self.pedidos.append(pedido)


class EtapaEncuentra(Enum):
    PreCompra = "PreCompra"
    Reserva = "Reserva"
    ListoDespacho = "ListoDespacho"


class EstadoPedido(Enum):
    Atrasado = "Atrasado"
    A_tiempo = "A tiempo"
