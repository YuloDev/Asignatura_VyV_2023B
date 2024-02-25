from enum import Enum
from datetime import datetime

# Definicion de la clase Vendedor
class Vendedor:
    # Constructor
    def __init__(self, nombre_vendedor, lista_pedidos=None):
        self.nombre_vendedor = nombre_vendedor
        self.lista_pedidos = []  # Inicializa la lista de pedidos del vendedor

#Este metodo pueden cambiar a su criterio
    def agregar_pedido(self, pedido):
        # Método para agregar un pedido a la lista de pedidos del vendedor
        self.lista_pedidos.append(pedido)

    def contar_pedidos(self):
        return len(self.lista_pedidos)

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
    def __init__(self, numero_pedido, etapa_pedido, pedido_activo, fecha_creacion_pedido,
                 fecha_maxima_etapa_precompra=None, fecha_real_etapa_precompra=None, estado_pedido_precompra=None,
                 fecha_maxima_etapa_reserva=None, fecha_real_etapa_reserva=None, estado_pedido_reserva=None,
                 fecha_maxima_etapa_listo_para_entregar=None, fecha_real_etapa_listo_para_entregar=None,
                 estado_pedido_listo_para_entregar=None):
        self.numero_pedido = numero_pedido
        self.etapa_pedido = etapa_pedido
        self.pedido_activo = pedido_activo
        self.fecha_creacion_pedido = fecha_creacion_pedido
        self.fecha_maxima_etapa_precompra = fecha_maxima_etapa_precompra
        self.fecha_real_etapa_precompra = fecha_real_etapa_precompra
        self.estado_pedido_precompra = estado_pedido_precompra
        self.fecha_maxima_etapa_reserva = fecha_maxima_etapa_reserva
        self.fecha_real_etapa_reserva = fecha_real_etapa_reserva
        self.estado_pedido_reserva = estado_pedido_reserva
        self.fecha_maxima_etapa_listo_para_entregar = fecha_maxima_etapa_listo_para_entregar
        self.fecha_real_etapa_listo_para_entregar = fecha_real_etapa_listo_para_entregar
        self.estado_pedido_listo_para_entregar = estado_pedido_listo_para_entregar

    @classmethod
    def from_row(cls, row):
        numero_pedido = row["numero_pedido"]
        etapa_pedido = row["etapa_pedido"]
        pedido_activo = row["pedido_activo"] == "true"
        fecha_creacion_pedido = datetime.strptime(row["fecha_creacion_pedido"], "%Y-%m-%d")
        fecha_maxima_etapa_precompra = datetime.strptime(row["fecha_maxima_etapa_precompra"], "%Y-%m-%d") if row["fecha_maxima_etapa_precompra"] else None
        fecha_real_etapa_precompra = datetime.strptime(row["fecha_real_etapa_precompra"], "%Y-%m-%d") if row["fecha_real_etapa_precompra"] else None
        estado_pedido_precompra = row["estado_pedido_precompra"]
        fecha_maxima_etapa_reserva = datetime.strptime(row["fecha_maxima_etapa_reserva"], "%Y-%m-%d") if row["fecha_maxima_etapa_reserva"] else None
        fecha_real_etapa_reserva = datetime.strptime(row["fecha_real_etapa_reserva"], "%Y-%m-%d") if row["fecha_real_etapa_reserva"] else None
        estado_pedido_reserva = row["estado_pedido_reserva"]
        fecha_maxima_etapa_listo_para_entregar = datetime.strptime(row["fecha_maxima_etapa_listo_para_entregar"], "%Y-%m-%d") if row["fecha_maxima_etapa_listo_para_entregar"] else None
        fecha_real_etapa_listo_para_entregar = datetime.strptime(row["fecha_real_etapa_listo_para_entregar"], "%Y-%m-%d") if row["fecha_real_etapa_listo_para_entregar"] else None
        estado_pedido_listo_para_entregar = row["estado_pedido_listo_para_entregar"]

        return cls(numero_pedido, etapa_pedido, pedido_activo, fecha_creacion_pedido, fecha_maxima_etapa_precompra,
                   fecha_real_etapa_precompra, estado_pedido_precompra, fecha_maxima_etapa_reserva,
                   fecha_real_etapa_reserva, estado_pedido_reserva, fecha_maxima_etapa_listo_para_entregar,
                   fecha_real_etapa_listo_para_entregar, estado_pedido_listo_para_entregar)

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