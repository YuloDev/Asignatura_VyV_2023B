from datetime import timedelta
from django.db import models
from django.utils import timezone
import datetime

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
    costo = models.CharField(max_length=2, choices=COSTO,default='BS')
    dias_duracion = models.IntegerField()
    cantidad_productos = models.IntegerField()


class Vendedor(models.Model):
    nombre = models.CharField(max_length=20)

    # def __str__(self):
    #     return self.nombre

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

    def contar_pedidos_por_estado(self,estado):
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

def calcular_dias_laborales(fecha_inicio, fecha_fin):
    dias_totales = (fecha_fin - fecha_inicio).days + 1  # +1 para incluir ambos días en el rango
    dias_laborales = 0
    for single_date in (fecha_inicio + datetime.timedelta(n) for n in range(dias_totales)):
        if single_date.weekday() < 5:  # Lunes a Viernes son días laborales (0-4)
            dias_laborales += 1

    return dias_laborales

class Pedido(models.Model):

    LISTO_PARA_ENTREGAR = 'LPE'
    REPARTIDOR_ASIGNADO = 'RA'
    EMBARCADO = 'E'
    PAQUETE_NO_ENTREGADO = 'PNE'
    PAQUETE_ENTREGADO = 'PE'
    A_TIEMPO = 'AT'
    ATRASADO = 'A'
    CLIENTE_NO_ENCONTRADO = 'CNE'

    ETAPA = (
        (LISTO_PARA_ENTREGAR, 'Listo para entregar'),
        (REPARTIDOR_ASIGNADO, 'Repartidor asignado'),
        (EMBARCADO, 'Embarcado'),
        (PAQUETE_NO_ENTREGADO, 'Paquete no entregado'),
        (PAQUETE_ENTREGADO, 'Paquete entregado'),
    )

    ESTADO = (
        (A_TIEMPO, 'A tiempo'),
        (ATRASADO, 'Atrasado'),
        (CLIENTE_NO_ENCONTRADO, 'Cliente no encontrado'),
    )

    estado_pedido = models.CharField(max_length=3, choices=ESTADO, default='AT')
    etapa_pedido = models.CharField(max_length=3, choices=ETAPA, default='LPE')
    fecha_listo_para_entregar = models.DateField()
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE)
    cliente_no_encontrado = models.BooleanField(default=False)

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

        dias_transcurridos = calcular_dias_laborales(self.fecha_listo_para_entregar, fecha_referencia)

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




