from enum import Enum
from datetime import datetime
from datetime import timedelta


# Definición de la clase UtilidadesFecha
class UtilidadesFecha:
    @staticmethod
    def calcular_tiempo_entre_fechas(fecha_inicio, fecha_fin):
        if fecha_inicio and fecha_fin:
            diferencia = fecha_fin - fecha_inicio
            return diferencia.days
        else:
            return 0


# Definicion de la clase Vendedor
class Vendedor:
    # Constructor
    def __init__(self, nombre_vendedor, lista_pedidos=None):
        self.nombre_vendedor = nombre_vendedor
        self.lista_pedidos = []  # Inicializa la lista de pedidos del vendedor

    def agregar_pedido(self, pedido, nombre_etapa):
        # Método para agregar un pedido a la lista de pedidos del vendedor
        self.lista_pedidos.append(pedido)

        # Lógica para cambiar el estado del pedido
        pedido.cambiar_estado(pedido.pedido_activo, nombre_etapa)

    def contar_pedidos(self):
        return len(self.lista_pedidos)

    def obtener_resumen_etapa(self, nombre_etapa):
        # Limpiamos los resúmenes existentes
        resumen_etapa = ResumenSeguimiento(nombre_etapa, 0, 0, 0, 0)
        resultados = resumen_etapa.obtener_detalles_resumen(self.lista_pedidos, nombre_etapa)
        # Almacenamos los resultados devueltos en la variable 'resultados'
        resumen_etapa.num_pedidos_total, resumen_etapa.num_pedido_cancelados, resumen_etapa.num_pedidos_atrasados, resumen_etapa.num_pedidos_a_tiempo = resultados
        # Imprimimos solo el resumen
        print(f"Resumen para la etapa {nombre_etapa}:")
        print(f"Pedidos en esta etapa: {resumen_etapa.num_pedidos_total}")
        print(f"Total cancelados: {resumen_etapa.num_pedido_cancelados}")
        print(f"Total atrasados: {resumen_etapa.num_pedidos_atrasados}")
        print(f"Total a tiempo: {resumen_etapa.num_pedidos_a_tiempo}")
        print("Resumen actualizado:", resumen_etapa.num_pedidos_total, "total,",
              resumen_etapa.num_pedido_cancelados,
              "cancelados,", resumen_etapa.num_pedidos_atrasados, "atrasados,", resumen_etapa.num_pedidos_a_tiempo,
              "a tiempo\n")
        return resumen_etapa


# Creacion de la Clase Etapa
class Etapa:
    def __init__(self):
        # Diccionario que mapea el nombre de la etapa a su tiempo estimado en días
        self.nombre_etapa = {
            "precompra": 2,
            "reserva": 4,
            "listo_para_entregar": 2,
        }
        # Diccionario que almacenará los pedidos por etapa
        self.pedidos_por_etapa = {etapa: [] for etapa in self.nombre_etapa}

    def agregar_pedido(self, pedido, nombre_etapa):
        # Método para agregar un pedido a la lista de pedidos por etapa
        self.pedidos_por_etapa[nombre_etapa].append(pedido)

    def calcular_info_etapa(self, nombre_etapa):
        # Calcular la información de una etapa específica sin depender de la lista de pedidos
        total_pedidos = len(self.pedidos_por_etapa[nombre_etapa])
        tiempo_etapa = self.obtener_tiempo_etapa(nombre_etapa)

        # Almacenar la información en un diccionario
        info_etapa = {"total_pedidos": total_pedidos, "tiempo_etapa": tiempo_etapa}

        # Imprimir información para verificar (esto podría ser eliminado en producción)
        print(f"Etapa: {nombre_etapa}, Total Pedidos: {total_pedidos}, Tiempo Estimado: {tiempo_etapa} días")

        # Devolver el diccionario con la información de la etapa
        return info_etapa

    def calcular_info_etapas(self):
        # Diccionario que almacenará la información de todas las etapas
        info_etapas = {}

        # Iterar sobre todas las etapas y calcular la información para cada una
        for nombre_etapa in self.nombre_etapa:
            info_etapas[nombre_etapa] = self.calcular_info_etapa(nombre_etapa)

        # Devolver el diccionario con la información de todas las etapas
        return info_etapas

    def obtener_tiempo_etapa(self, nombre_etapa):
        # Obtener el tiempo estimado de una etapa por su nombre, si no está presente, devolver 0
        return self.nombre_etapa.get(nombre_etapa, 0)


# Definicion de la clase ResumenSeguimiento
class ResumenSeguimiento:
    def __init__(self, nombre_etapa, tiempo_etapa, num_pedido_cancelados, num_pedidos_atrasados, num_pedidos_a_tiempo):
        self.nombre_etapa = nombre_etapa
        self.tiempo_etapa = tiempo_etapa

        self.num_pedido_cancelados = num_pedido_cancelados
        self.num_pedidos_atrasados = num_pedidos_atrasados
        self.num_pedidos_a_tiempo = num_pedidos_a_tiempo

        self.num_pedidos_total = None  # Inicializamos la variable total_pedidos como None

    def sumar_pedidos(self):
        self.total_pedidos = self.num_pedidos_atrasados + self.num_pedidos_a_tiempo + self.num_pedido_cancelados
        return self.total_pedidos

    def obtener_detalles_resumen(self, pedidos, nombre_etapa):
        pedidos_etapa = [pedido for pedido in pedidos if pedido.etapa_pedido == nombre_etapa]

        # Inicializamos las variables
        total_pedidos = len(pedidos_etapa)
        pedidos_cancelados = sum(1 for pedido in pedidos_etapa if pedido.pedido_activo == False)
        pedidos_atrasados = sum(
            1 for pedido in pedidos_etapa if pedido.cambiar_estado(pedido.pedido_activo, pedido.etapa_pedido) == "atrasado")
        pedidos_a_tiempo = sum(1 for pedido in pedidos_etapa if pedido.cambiar_estado(pedido.pedido_activo, pedido.etapa_pedido) == "a_tiempo")

        # Almacenamos los resultados en el atributo 'resultados'
        self.resultados = (total_pedidos, pedidos_cancelados, pedidos_atrasados, pedidos_a_tiempo)

        # Devolvemos los resultados
        return self.resultados


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

        # Calcula dinámicamente los tiempos de cada etapa en función de las fechas reales
        self.tiempo_pedidoPC = UtilidadesFecha.calcular_tiempo_entre_fechas(fecha_maxima_etapa_precompra,
                                                                            fecha_real_etapa_precompra)
        self.tiempo_pedidoR = UtilidadesFecha.calcular_tiempo_entre_fechas(fecha_maxima_etapa_reserva,
                                                                           fecha_real_etapa_reserva)
        self.tiempo_pedidoAT = UtilidadesFecha.calcular_tiempo_entre_fechas(fecha_maxima_etapa_listo_para_entregar,
                                                                            fecha_real_etapa_listo_para_entregar)

    @classmethod
    def from_row(cls, row):
        numero_pedido = row["numero_pedido"]
        etapa_pedido = row["etapa_pedido"]
        pedido_activo = row["pedido_activo"] == "true"
        fecha_creacion_pedido = datetime.strptime(row["fecha_creacion_pedido"], "%Y-%m-%d")
        fecha_maxima_etapa_precompra = datetime.strptime(row["fecha_maxima_etapa_precompra"], "%Y-%m-%d") if row[
            "fecha_maxima_etapa_precompra"] else None
        fecha_real_etapa_precompra = datetime.strptime(row["fecha_real_etapa_precompra"], "%Y-%m-%d") if row[
            "fecha_real_etapa_precompra"] else None
        estado_pedido_precompra = row["estado_pedido_precompra"]
        fecha_maxima_etapa_reserva = datetime.strptime(row["fecha_maxima_etapa_reserva"], "%Y-%m-%d") if row[
            "fecha_maxima_etapa_reserva"] else None
        fecha_real_etapa_reserva = datetime.strptime(row["fecha_real_etapa_reserva"], "%Y-%m-%d") if row[
            "fecha_real_etapa_reserva"] else None
        estado_pedido_reserva = row["estado_pedido_reserva"]
        fecha_maxima_etapa_listo_para_entregar = datetime.strptime(row["fecha_maxima_etapa_listo_para_entregar"],
                                                                   "%Y-%m-%d") if row[
            "fecha_maxima_etapa_listo_para_entregar"] else None
        fecha_real_etapa_listo_para_entregar = datetime.strptime(row["fecha_real_etapa_listo_para_entregar"],
                                                                 "%Y-%m-%d") if row[
            "fecha_real_etapa_listo_para_entregar"] else None
        estado_pedido_listo_para_entregar = row["estado_pedido_listo_para_entregar"]

        return cls(numero_pedido, etapa_pedido, pedido_activo, fecha_creacion_pedido, fecha_maxima_etapa_precompra,
                   fecha_real_etapa_precompra, estado_pedido_precompra, fecha_maxima_etapa_reserva,
                   fecha_real_etapa_reserva, estado_pedido_reserva, fecha_maxima_etapa_listo_para_entregar,
                   fecha_real_etapa_listo_para_entregar, estado_pedido_listo_para_entregar)

    # Método para cambiar el estado de un pedido
    def cambiar_estado(self, pedido_activo, nombre_etapa):
        if pedido_activo == True:
            if nombre_etapa == "precompra":
                if self.tiempo_pedidoPC <= 0:
                    self.estado_pedido = "a_tiempo"
                else:
                    self.estado_pedido = "atrasado"
            elif nombre_etapa == "reserva":
                if self.tiempo_pedidoR <= 0:
                    self.estado_pedido = "a_tiempo"
                else:
                    self.estado_pedido = "atrasado"
            elif nombre_etapa == "listo_para_entregar":
                if self.tiempo_pedidoAT <= 0:
                    self.estado_pedido = "a_tiempo"
                else:
                    self.estado_pedido = "atrasado"
            else:
                self.estado_pedido = "cancelado"
        else:
            self.estado_pedido = "cancelado"
        return self.estado_pedido


class EtapaEncuentra(Enum):
    precompra = "PreCompra"
    reserva = "Reserva"
    listo_para_entregar = "listo_para_entregar"
class EstadoPedido(Enum):
    Atrasado = "Atrasado"
    A_tiempo = "A tiempo"
    Cancelado = "Cancelado"
