from django.db import models
from django.utils import timezone
import datetime
#######################################################################################################################
# Vendedor class
class Vendedor(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

    ###Listar pedidos
    def listar_pedidos(self):
        # Utiliza el acceso inverso para obtener todos los pedidos relacionados
        return self.pedido_set.all()

    def listar_pedidos_listo_para_entregar(self):
        return self.pedido_set.filter(etapa_pedido=Pedido.LISTO_PARA_ENTREGAR)

    def listar_pedidos_repartidor_asignado(self):
        return self.pedido_set.filter(etapa_pedido=Pedido.REPARTIDOR_ASIGNADO)

    def listar_pedidos_embarcado(self):
        return self.pedido_set.filter(etapa_pedido=Pedido.EMBARCADO)

    def listar_pedidos_en_camino(self):
        return self.pedido_set.filter(etapa_pedido=Pedido.EN_CAMINO)

    def listar_pedidos_paquete_no_entregado(self):
        return self.pedido_set.filter(etapa_pedido=Pedido.PAQUETE_NO_ENTREGADO)

    def listar_pedidos_paquete_entregado(self):
        return self.pedido_set.filter(etapa_pedido=Pedido.PAQUETE_ENTREGADO)
########################################################################################################################
#Contar pedidos
    def contar_pedidos_por_etapa(self, etapa):
        # Cuenta los pedidos por estado en una etapa específica
        return self.pedido_set.filter(etapa_pedido=etapa).count()
    def contar_pedidos_listo_para_entregar(self, etapa):
        return self.contar_pedidos_por_etapa(Pedido.LISTO_PARA_ENTREGAR).count()

    def contar_pedidos_repartido_asignado(self, etapa):
        return self.contar_pedidos_por_etapa(Pedido.REPARTIDOR_ASIGNADO).count()

    def contar_pedidos_embarcado(self, etapa):
        return self.contar_pedidos_por_etapa(Pedido.EMBARCADO).count()
    def contar_pedidos_en_camino(self, etapa):
        return self.contar_pedidos_por_etapa(Pedido.EN_CAMINO).count()
    def contar_pedidos_paquete_no_entregado(self, etapa):
        return self.contar_pedidos_por_etapa(Pedido.PAQUETE_NO_ENTREGADO).count()
    def contar_pedidos_paquete_entregado(self, etapa):
        return self.contar_pedidos_por_etapa(Pedido.PAQUETE_ENTREGADO).count()

    def contar_pedidos_por_estado_en_etapa(self, etapa, estado):
        # Cuenta los pedidos por estado en una etapa específica
        return self.pedido_set.filter(etapa_pedido=etapa, estado_pedido=estado).count()

    def contar_pedidos_a_tiempo_listo_para_entregar(self):
        return self.contar_pedidos_por_estado_en_etapa(Pedido.LISTO_PARA_ENTREGAR, Pedido.A_TIEMPO)

    def contar_pedidos_atrasados_listo_para_entregar(self):
        return self.contar_pedidos_por_estado_en_etapa(Pedido.LISTO_PARA_ENTREGAR, Pedido.ATRASADO)



########################################################################################################################
# Pedido class
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
    EN_CAMINO = 'EC'
    PAQUETE_NO_ENTREGADO = 'PNE'
    PAQUETE_ENTREGADO = 'PE'
    A_TIEMPO = 'AT'
    ATRASADO = 'A'
    CLIENTE_NO_ENCONTRADO = 'CNE'

    ETAPA = (
        (LISTO_PARA_ENTREGAR, 'Listo para entregar'),
        (REPARTIDOR_ASIGNADO, 'Repartidor asignado'),
        (EMBARCADO, 'Embarcado'),
        (EN_CAMINO, 'En camino'),
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
    fecha_creacion_pedido = models.DateField()
    fecha_entrega_cliente_estimada = models.DateField(blank=True, null=True)
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.pk:  # Verificar si es una nueva instancia
            self.fecha_entrega_cliente_estimada = self.calcular_fecha_entrega(8)
        super(Pedido, self).save(*args, **kwargs)

    def calcular_fecha_entrega(self, dias_laborales):
        fecha_inicio = self.fecha_creacion_pedido
        dias_contados = 0
        while dias_laborales > 0:
            if fecha_inicio.weekday() < 5:  # Lunes a Viernes son considerados días laborales
                dias_laborales -= 1
            # Moverse al siguiente día
            fecha_inicio += datetime.timedelta(days=1)
            dias_contados += 1
        return self.fecha_creacion_pedido + datetime.timedelta(days=dias_contados)

    def actualizar_etapa(self):
        # Secuencia de etapas en orden
        etapas = [self.LISTO_PARA_ENTREGAR, self.REPARTIDOR_ASIGNADO, self.EMBARCADO, self.EN_CAMINO,
                  self.PAQUETE_NO_ENTREGADO, self.PAQUETE_ENTREGADO]
        if self.etapa_pedido in etapas:
            # Obtener el índice de la etapa actual
            index_actual = etapas.index(self.etapa_pedido)
            # Verificar si no es la última etapa o es PAQUETE_NO_ENTREGADO
            if self.etapa_pedido == self.PAQUETE_NO_ENTREGADO:
                self.etapa_pedido = self.EN_CAMINO
            elif self.etapa_pedido != self.PAQUETE_ENTREGADO and index_actual < len(etapas) - 1:
                # Avanzar a la siguiente etapa
                self.etapa_pedido = etapas[index_actual + 1]
            self.save()
        else:
            pass

    def actualizar_estado_pedido(self):
        hoy = timezone.now().date()
        dias_transcurridos = calcular_dias_laborales(self.fecha_creacion_pedido, hoy)

        etapa_dias_maximos = {
            self.LISTO_PARA_ENTREGAR: 1,
            self.REPARTIDOR_ASIGNADO: 2,
            self.EMBARCADO: 5,
            self.EN_CAMINO: 8,
        }

        # Si el pedido ya fue entregado o no fue encontrado, conservar el estado
        if self.etapa_pedido in [self.PAQUETE_ENTREGADO, self.PAQUETE_NO_ENTREGADO]:
            if self.etapa_pedido == self.PAQUETE_NO_ENTREGADO:
                self.estado_pedido = self.CLIENTE_NO_ENCONTRADO
            # No se actualiza el estado si es PAQUETE_ENTREGADO
        else:
            dias_maximos = etapa_dias_maximos.get(self.etapa_pedido, 0)
            if dias_transcurridos <= dias_maximos:
                self.estado_pedido = self.A_TIEMPO
            else:
                self.estado_pedido = self.ATRASADO

        self.save()