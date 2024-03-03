from django.db import models
from django.template.defaultfilters import default
from datetime import datetime
from datetime import timedelta
from django.utils import timezone
import datetime


# Create your models here.

class Cliente(models.Model):
    nombre = models.CharField(max_length=50)
    preferencias = models.CharField(max_length=200, blank=True)


class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    record_ventas = models.IntegerField()

    def __str__(self):
        return self.nombre

    def supera_record(self, cantidad):
        return cantidad > self.record_ventas


class Promocion(models.Model):
    id_promocion = models.AutoField(primary_key=True)
    paquete = models.CharField(max_length=30)
    costo = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    dias_duracion = models.IntegerField(default=0)
    fecha_inicio = models.DateField()


class Vendedor(models.Model):
    nombre = models.CharField(max_length=20)

    # def __str__(self):
    #     return self.nombre

    def listar_pedidos(self):
        # Utiliza el acceso inverso para obtener todos los pedidos relacionados
        return self.pedido_set.all()

    def listar_pedidos_por_etapa(self, etapa):
        # Cuenta los pedidos por estado en una etapa específica
        return self.pedido_set.filter(etapa_pedido=etapa)

    def contar_pedidos_por_etapa(self, etapa):
        # Cuenta los pedidos por estado en una etapa específica
        return self.pedido_set.filter(etapa_pedido=etapa).count()

    def contar_pedidos_por_estado_en_etapa(self, etapa, estado):
        # Cuenta los pedidos por estado en una etapa específica
        return self.pedido_set.filter(etapa_pedido=etapa, estado_pedido=estado).count()

    def contar_pedidos_por_estado(self, estado):
        # Cuenta los pedidos por estado en una etapa específica
        return self.pedido_set.filter(estado_pedido=estado).count()

    def total_pedidos_vendedor(vendedor_id):
        return Pedido.objects.filter(vendedor_id=vendedor_id).count()

    def sumar_y_contar_por_etapa(etapa, vendedor_id):
        pedidos_vendedor = Pedido.objects.filter(vendedor_id=vendedor_id)
        pedidos_etapa = pedidos_vendedor.filter(etapa_pedido=etapa)
        total_pedidos_etapa = pedidos_etapa.count()
        atrasados = pedidos_etapa.filter(estado_pedido=Pedido.ATRASADO).count()
        a_tiempo = pedidos_etapa.filter(estado_pedido=Pedido.A_TIEMPO).count()
        cancelados = pedidos_etapa.filter(estado_pedido=Pedido.CANCELADO).count()
        return total_pedidos_etapa, atrasados, a_tiempo, cancelados


class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50, default="")
    unidades_vendidas = models.IntegerField(default=0)
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE, null=True)
    promocion = models.ForeignKey(Promocion, on_delete=models.CASCADE, null=True)

    def ha_superado_record(self):
        return self.categoria.supera_record(self.unidades_vendidas)

    def tiene_promocion(self):
        return self.promocion


class Pedido(models.Model):
    A_TIEMPO = 'AT'
    ATRASADO = 'A'
    CANCELADO = 'C'
    PRECOMPRA = 'PC'
    RESERVA = 'R'
    LISTO_PARA_ENTREGAR = 'LE'
    REPARTIDOR_ASIGNADO = 'RA'
    EMBARCADO = 'E'
    PAQUETE_NO_ENTREGADO = 'PNE'
    PAQUETE_ENTREGADO = 'PE'
    CLIENTE_NO_ENCONTRADO = 'CNE'

    ETAPA = (
        (PRECOMPRA, 'precompra'),
        (RESERVA, 'reserva'),
        (LISTO_PARA_ENTREGAR, 'listo_para_entregar'),
        (REPARTIDOR_ASIGNADO, 'Repartidor asignado'),
        (EMBARCADO, 'Embarcado'),
        (PAQUETE_NO_ENTREGADO, 'Paquete no entregado'),
        (PAQUETE_ENTREGADO, 'Paquete entregado'),
    )

    ESTADO = (
        (A_TIEMPO, 'a_tiempo'),
        (ATRASADO, 'atrasado'),
        (CANCELADO, 'cancelado'),
        (CLIENTE_NO_ENCONTRADO, 'Cliente no encontrado'),

    )

    etapa_pedido = models.CharField(max_length=20, choices=ETAPA, default=PRECOMPRA)
    estado_pedido = models.CharField(max_length=20, choices=ESTADO, default=A_TIEMPO)
    pedido_activo = models.BooleanField(default=True)
    fecha_creacion_pedido = models.DateField()
    fecha_etapa_precompra = models.DateField(null=True, blank=True)
    fecha_etapa_reserva = models.DateField(null=True, blank=True)
    fecha_listo_para_entregar = models.DateField(null=True, blank=True)
    cliente_no_encontrado = models.BooleanField(default=False)
    fecha_real_etapa_precompra = models.DateField(null=True, blank=True)
    fecha_real_etapa_reserva = models.DateField(null=True, blank=True)
    fecha_real_etapa_listo_para_entregar = models.DateField(null=True, blank=True)
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE, default=1)

    def calcular_dias_laborales(fecha_inicio, fecha_fin):
        dias_totales = (fecha_fin - fecha_inicio).days + 1  # +1 para incluir ambos días en el rango
        dias_laborales = 0
        for single_date in (fecha_inicio + datetime.timedelta(n) for n in range(dias_totales)):
            if single_date.weekday() < 5:  # Lunes a Viernes son días laborales (0-4)
                dias_laborales += 1

        return dias_laborales

    def total_pedidos_vendedor(vendedor_id):
        return Pedido.objects.filter(vendedor_id=vendedor_id).count()

    def sumar_y_contar_por_etapa(etapa, vendedor_id):
        pedidos_vendedor = Pedido.objects.filter(vendedor_id=vendedor_id)
        pedidos_etapa = pedidos_vendedor.filter(etapa_pedido=etapa)
        total_pedidos_etapa = pedidos_etapa.count()
        atrasados = pedidos_etapa.filter(estado_pedido=Pedido.ATRASADO).count()
        a_tiempo = pedidos_etapa.filter(estado_pedido=Pedido.A_TIEMPO).count()
        cancelados = pedidos_etapa.filter(estado_pedido=Pedido.CANCELADO).count()
        return total_pedidos_etapa, atrasados, a_tiempo, cancelados

    @staticmethod
    def calcular_tiempo_entre_fechas(fecha_inicio, fecha_fin):
        if fecha_inicio and fecha_fin:
            diferencia = fecha_fin - fecha_inicio
            return diferencia.days
        else:
            return 0

    def cambiar_estado(self):
        # Obtener los plazos para cada etapa desde TiempoEtapa
        plazo_precompra = 2
        plazo_reserva = 4
        plazo_listo_para_entregar = 2

        # Calcular las fechas máximas para cada etapa en función de la fecha de creación
        fecha_maxima_etapa_precompra = self.fecha_creacion_pedido + timedelta(days=plazo_precompra)

        if self.fecha_etapa_precompra is not None:
            fecha_maxima_etapa_reserva = self.fecha_etapa_precompra + timedelta(days=plazo_reserva)

        else:
            # Manejar el caso cuando la fecha real de la etapa de precompra no está definida
            fecha_maxima_etapa_reserva = None

        if self.fecha_etapa_reserva is not None:
            fecha_maxima_etapa_listo_para_entregar = self.fecha_etapa_reserva + timedelta(
                days=plazo_listo_para_entregar)
        else:
            # Manejar el caso cuando la fecha real de la etapa de reserva no está definida
            fecha_maxima_etapa_listo_para_entregar = None

        # Calcular los tiempos entre fechas reales y máximas
        tiempo_pedidoPC = self.calcular_tiempo_entre_fechas(fecha_maxima_etapa_precompra,
                                                            self.fecha_etapa_precompra)
        tiempo_pedidoR = self.calcular_tiempo_entre_fechas(fecha_maxima_etapa_reserva, self.fecha_etapa_reserva)
        tiempo_pedidoAT = self.calcular_tiempo_entre_fechas(fecha_maxima_etapa_listo_para_entregar,
                                                            self.fecha_listo_para_entregar)

        if self.pedido_activo:
            if self.etapa_pedido == "PC":
                if tiempo_pedidoPC > 0:
                    self.estado_pedido = self.ATRASADO
                else:
                    self.estado_pedido = self.A_TIEMPO
            elif self.etapa_pedido == "R":
                if tiempo_pedidoR > 0:
                    self.estado_pedido = self.ATRASADO
                else:
                    self.estado_pedido = self.A_TIEMPO
            elif self.etapa_pedido == "LE":
                if tiempo_pedidoAT > 0:
                    self.estado_pedido = self.ATRASADO
                else:
                    self.estado_pedido = self.A_TIEMPO
        else:
            self.estado_pedido = self.CANCELADO

        self.save()

    def calcular_fecha_entrega(self, dias_laborales):
        fecha_inicio = self.fecha_listo_para_entregar
        dias_contados = 0
        while dias_laborales > 0:
            if fecha_inicio.weekday() < 5:  # Lunes a Viernes son considerados días laborales
                dias_laborales -= 1
            # Moverse al siguiente día
            fecha_inicio += datetime.timedelta(days=1)
            dias_contados += 1
        return self.fecha_listo_para_entregar + datetime.timedelta(days=dias_contados)

    def actualizar_etapa(self):
        # Secuencia de etapas en orden
        etapas = [self.LISTO_PARA_ENTREGAR, self.REPARTIDOR_ASIGNADO, self.EMBARCADO,
                  self.PAQUETE_NO_ENTREGADO, self.PAQUETE_ENTREGADO]
        if self.etapa_pedido in etapas:
            # Obtener el índice de la etapa actual
            index_actual = etapas.index(self.etapa_pedido)
            # Verificar si no es la última etapa o es PAQUETE_NO_ENTREGADO
            if self.etapa_pedido != self.PAQUETE_ENTREGADO and index_actual < len(etapas) - 1:
                # Avanzar a la siguiente etapa
                self.etapa_pedido = etapas[index_actual + 1]
            self.save()
        else:
            pass

    def marcar_cliente_no_encontrado(self):
        self.cliente_no_encontrado = True
        self.estado_pedido = self.CLIENTE_NO_ENCONTRADO  # Opcional: Actualizar también el estado del pedido
        self.save()

    def actualizar_estado_pedido(self, anios=0, meses=0, semanas=0, dias=0):
        # Calcular la cantidad total de días (aproximación para meses)
        días_totales = dias + semanas * 7 + meses * 30 + anios * 365

        # Si no se proporcionan parámetros, usar la fecha actual; de lo contrario, agregar los días totales a 'fecha_listo_para_entregar'
        if anios == meses == semanas == dias == 0:
            fecha_referencia = timezone.now().date()
        else:
            fecha_referencia = self.fecha_listo_para_entregar + timedelta(days=días_totales)

        dias_transcurridos = self.calcular_dias_laborales(self.fecha_listo_para_entregar, fecha_referencia)

        etapa_dias_maximos = {
            self.LISTO_PARA_ENTREGAR: 1,
            self.REPARTIDOR_ASIGNADO: 2,
            self.EMBARCADO: 5,
            self.PAQUETE_NO_ENTREGADO: 8,
        }

        # Si el pedido ya fue entregado o no fue encontrado, conservar el estado
        if self.etapa_pedido in [self.PAQUETE_ENTREGADO, self.PAQUETE_NO_ENTREGADO]:
            if self.cliente_no_encontrado:
                self.estado_pedido = self.CLIENTE_NO_ENCONTRADO
            else:
                dias_maximos = etapa_dias_maximos.get(self.etapa_pedido, 0)
                if dias_transcurridos <= dias_maximos:
                    self.estado_pedido = self.A_TIEMPO
                else:
                    self.estado_pedido = self.ATRASADO
        else:
            dias_maximos = etapa_dias_maximos.get(self.etapa_pedido, 0)
            if dias_transcurridos <= dias_maximos:
                self.estado_pedido = self.A_TIEMPO
            else:
                self.estado_pedido = self.ATRASADO

        self.save()
