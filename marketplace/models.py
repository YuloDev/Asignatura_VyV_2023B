from django.db import models
from datetime import datetime
from datetime import timedelta


# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    record = models.IntegerField(default=0)

    def producto_supera_record(self, unidades_vendidas):
        if unidades_vendidas > self.record:
            self.record = unidades_vendidas
            self.save()
            return True
        else:
            return False


class Promocion(models.Model):
    TIPO_PROMOCION = (
        ('GD', 'Gold'),
        ('PG', 'Platinum'),
        ('BS', 'Basic'),
    )
    COSTO = (
        ('GD', 50),
        ('PG', 35),
        ('BS', 20),
    )

    fecha_inicio = models.DateField()
    tipo_promocion = models.CharField(max_length=2, choices=TIPO_PROMOCION)
    costo = models.CharField(max_length=2, choices=COSTO, default='BS')
    dias_duracion = models.IntegerField()
    cantidad_productos = models.IntegerField()


class Vendedor(models.Model):
    nombre = models.CharField(max_length=20)
    apellido = models.CharField(max_length=20)

    def agregar_producto(self, producto):
        self.productos.add(producto)
        self.save()

    def obtener_productos(self):
        return self.productos.all()

    def pagar_promocion(self, monto, producto):
        producto.promocion = True
        producto.save()

    def tiene_promocion_activa(self):
        return any(producto.promocion for producto in self.obtener_productos())


class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    unidades_vendidas = models.IntegerField()
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE, related_name='productos')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    promocion = models.BooleanField(default=False)

    def asignar_categoria(self, categoria):
        self.categoria = categoria
        self.save()

    def unidades_vendidas_ha_superado_record(self):
        return self.categoria.producto_supera_record(self.unidades_vendidas)

    def agregar_promocion(self):
        self.promocion = True
        self.save()

    def tiene_promocion(self):
        return self.promocion


######################################################
# GRUPO 4
class Pedido(models.Model):
    A_TIEMPO = 'AT'
    ATRASADO = 'A'
    CANCELADO = 'C'

    PRECOMPRA = 'PC'
    RESERVA = 'R'
    LISTO_PARA_ENTREGAR = 'LE'

    ETAPA = (
        (PRECOMPRA, 'precompra'),
        (RESERVA, 'reserva'),
        (LISTO_PARA_ENTREGAR, 'listo_para_entregar'),
    )

    ESTADO = (
        (A_TIEMPO, 'a_tiempo'),
        (ATRASADO, 'atrasado'),
        (CANCELADO, 'cancelado'),
    )

    etapa_pedido = models.CharField(max_length=20, choices=ETAPA, default=PRECOMPRA)
    estado_pedido = models.CharField(max_length=20, choices=ESTADO, default=A_TIEMPO)
    pedido_activo = models.BooleanField(default=True)
    fecha_creacion_pedido = models.DateField()
    fecha_real_etapa_precompra = models.DateField(null=True, blank=True)
    fecha_real_etapa_reserva = models.DateField(null=True, blank=True)
    fecha_real_etapa_listo_para_entregar = models.DateField(null=True, blank=True)

    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE, default=1)

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

        if self.fecha_real_etapa_precompra is not None:
            fecha_maxima_etapa_reserva = self.fecha_real_etapa_precompra + timedelta(days=plazo_reserva)
        else:
            # Manejar el caso cuando la fecha real de la etapa de precompra no está definida
            fecha_maxima_etapa_reserva = None

        if self.fecha_real_etapa_reserva is not None:
            fecha_maxima_etapa_listo_para_entregar = self.fecha_real_etapa_reserva + timedelta(
                days=plazo_listo_para_entregar)
        else:
            # Manejar el caso cuando la fecha real de la etapa de reserva no está definida
            fecha_maxima_etapa_listo_para_entregar = None

        # Calcular los tiempos entre fechas reales y máximas
        tiempo_pedidoPC = self.calcular_tiempo_entre_fechas(fecha_maxima_etapa_precompra,
                                                            self.fecha_real_etapa_precompra)
        tiempo_pedidoR = self.calcular_tiempo_entre_fechas(fecha_maxima_etapa_reserva, self.fecha_real_etapa_reserva)
        tiempo_pedidoAT = self.calcular_tiempo_entre_fechas(fecha_maxima_etapa_listo_para_entregar,
                                                            self.fecha_real_etapa_listo_para_entregar)

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
