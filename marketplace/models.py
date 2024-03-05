import json
from enum import Enum

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import JSONField
from django.template.defaultfilters import default
from datetime import datetime
from datetime import timedelta
from django.utils import timezone
import datetime


# Create your models here.


class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    record_ventas = models.IntegerField()

    def __str__(self):
        return self.nombre

    def supera_record(self, cantidad):
        return cantidad > self.record_ventas

    def actualizar_record(self, nuevo_record):
        self.record_ventas = nuevo_record


class Promocion(models.Model):
    id_promocion = models.AutoField(primary_key=True)
    paquete = models.CharField(max_length=30)
    costo = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    dias_duracion = models.IntegerField(default=0)


class Cliente(models.Model):
    cedula = models.CharField(max_length=10, primary_key=True, unique=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    correo = models.EmailField(max_length=50)
    telefono = models.CharField(max_length=10)
    preferencias = models.CharField(max_length=200, blank=True)

    def calificar_producto(self, estrellas, causas, producto, calificaciones_recibidas):
        calificacion = Calificacion(estrellas=estrellas, causas=causas, id_producto=producto)
        calificacion.save()
        producto.agregar_calificacion(calificacion, calificaciones_recibidas)

    def calificar_servicio(self, pedido, estrellas, causas, calificaciones_recibidas):
        calificacion = Calificacion(estrellas=estrellas, causas=causas, id_servicio=pedido.servicio)
        print(causas)
        pedido.servicio.agregar_calificacion(calificacion, calificaciones_recibidas)
        calificacion.save()

    def obtener_productos_destacados_de_cliente(self):
        productos_destacados = []
        productos = Producto.obtener_productos_destacados()
        for producto in productos:
            if str(producto.categoria) in self.preferencias:
                productos_destacados.append(producto)
        return productos_destacados


class Vendedor(models.Model):
    vendedorID = models.AutoField(primary_key=True)
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

    def establecer_meta(self, meta):
        self.metas.add(meta)
        meta.save()

    def obtener_meta(self, tipo_de_metrica, anio, mes):
        return self.metas.filter(tipo_de_metrica=tipo_de_metrica, anio=anio, mes=mes).first()

    def obtener_ventas(self):
        return self.pedidos.all()

    def obtener_ventas_por_fecha(self, anio, mes):
        ventas_por_fecha = self.pedidos.filter(fecha_listo_para_entregar__year=anio,
                                               fecha_listo_para_entregar__month=mes)
        return ventas_por_fecha

    def obtener_cantidad_de_ventas_por_fecha(self, anio, mes):
        return self.obtener_ventas_por_fecha(anio, mes).count()

    def generar_reporte(self, anio, mes):
        reportes = self.reportes.filter(anio=anio, mes=mes)

        if reportes.exists():
            reporte = reportes.first()
        else:
            reporte = self.reportes.create(anio=anio, mes=mes)

        reporte.determinar_metricas_y_recomendaciones()
        return reporte


class Producto(models.Model):
    def __str__(self):
        return self.nombre

    id_producto = models.AutoField(primary_key=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50, default="")
    unidades_vendidas = models.IntegerField(default=0)
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE, null=True, related_name='productos')
    promocion = models.ForeignKey(Promocion, on_delete=models.CASCADE, null=True)
    calificaciones = JSONField(default=dict)
    precio = models.FloatField()
    costo = models.FloatField()
    supera_record = models.BooleanField(default=False)

    def ha_superado_record(self):
        return self.categoria.supera_record(self.unidades_vendidas)

    def tiene_promocion(self):
        return self.promocion

    def feedback_producto_esta_dado(self):
        return True

    def aumentar_estrella(self, calificacion_cliente):
        for estrellas, calificacion_total in self.calificaciones.items():
            if estrellas == str(calificacion_cliente):
                self.calificaciones[str(estrellas)] += 1
                print(self.calificaciones[str(estrellas)])
                self.save()
                break

    def agregar_calificacion(self, calificacion, calificaciones_recibidas):
        calificaciones_recibidas.append(calificacion)
        self.aumentar_estrella(calificacion.estrellas)

    def obtener_porcentajes_de_calificaciones(self):
        porcentajes_por_estrella = list()
        calificaciones_totales = 0
        for i in self.calificaciones:
            calificaciones_totales += int(self.calificaciones[i])

        for i in self.calificaciones:
            if i in self.calificaciones:
                porcentaje_calculado = (int(self.calificaciones[i]) / calificaciones_totales) * 100
                porcentaje_calculado = round(porcentaje_calculado)
                porcentajes_por_estrella.append(str(porcentaje_calculado))

        porcentajes_por_estrella.reverse()
        return porcentajes_por_estrella

    def obtener_causas_de_cada_estrella(self, calificaciones_recibidas):
        causas = {1: "", 2: "", 3: "", 4: "", 5: ""}
        causas_temp = {1: list(), 2: list(), 3: list(), 4: list(), 5: list()}

        for calificacion in calificaciones_recibidas:
            causas_temp[int(calificacion.estrellas)].extend(calificacion.causas)

        for estrella, lista_causas in causas_temp.items():
            contador_causas = {}
            for causa in lista_causas:
                if causa is not None:
                    if causa in contador_causas:
                        contador_causas[causa] += 1
                    else:
                        contador_causas[causa] = 1
            sorted_causas = sorted(contador_causas.items(), key=lambda x: x[1], reverse=True)
            causas[estrella] = ", ".join([f"{causa} ({cantidad})" for causa, cantidad in sorted_causas])
        return causas

    def obtener_promedio_general_del_producto(self):
        total_calificaciones = 0
        total_estrellas = 0
        for clave in self.calificaciones:
            total_calificaciones += self.calificaciones[clave]
            total_estrellas += int(clave) * int(self.calificaciones[clave])

        promedio_general = round(total_estrellas / total_calificaciones)
        print(promedio_general)
        return promedio_general

    def obtener_precio(self):  # Necesario?
        return self.precio

    def obtener_costo(self):  # Necesario?
        return self.costo

    @staticmethod
    def obtener_productos_destacados():
        for producto in Producto.objects.all():
            if producto.ha_superado_record():
                producto.supera_record = True
                producto.save()
        return Producto.objects.filter(supera_record=True)

    @staticmethod
    def actualizar_record_categorias():
        for producto in Producto.obtener_productos_destacados():
            categoria = Categoria.objects.get(nombre=producto.categoria)
            categoria.record_ventas = producto.unidades_vendidas
            categoria.save()

    @staticmethod
    def buscar_productos(busqueda):
        productos = Producto.objects.filter(nombre__icontains=busqueda)
        productos = productos.order_by('promocion__producto')
        if productos:
            return productos
        else:
            return ["No se han encontrado coincidencias"]


class Servicio(models.Model):
    puntuaciones_calificaciones = JSONField(default=dict)
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE, related_name='servicios', null=True, blank=True)

    def aumentar_estrella(self, calificacion_cliente):
        for calificacion in self.puntuaciones_calificaciones:
            if calificacion["estrellas"] == calificacion_cliente:
                calificacion["cantidad"] += 1
                self.save()
                break
        self.calcular_porcentajes()

    def agregar_calificacion(self, calificacion, calificaciones_recibidas):
        calificaciones_recibidas.append(calificacion)
        self.aumentar_estrella(calificacion.estrellas)

    def calcular_porcentajes(self):
        total_estrellas = sum(calificacion["cantidad"] for calificacion in self.puntuaciones_calificaciones)
        for calificacion in self.puntuaciones_calificaciones:
            porcentaje_calculado = (calificacion["cantidad"] / total_estrellas) * 100
            porcentaje_calculado = round(porcentaje_calculado)
            calificacion["porcentaje"] = str(porcentaje_calculado)

    def obtener_porcentajes_de_calificaciones(self):
        porcentajes_por_estrella = list()
        total_estrellas = sum(calificacion["cantidad"] for calificacion in self.puntuaciones_calificaciones)
        for calificacion in self.puntuaciones_calificaciones:
            porcentaje_calculado = (calificacion["cantidad"] / total_estrellas) * 100
            porcentaje_calculado = round(porcentaje_calculado)
            porcentajes_por_estrella.append(str(porcentaje_calculado))

        porcentajes_por_estrella.reverse()
        return porcentajes_por_estrella

    def obtener_causas_de_cada_estrella(self, calificaciones_recibidas):
        causas = {1: "", 2: "", 3: "", 4: "", 5: ""}
        causas_temp = {1: list(), 2: list(), 3: list(), 4: list(), 5: list()}

        for calificacion in calificaciones_recibidas:
            causas_temp[int(calificacion.estrellas)].extend(calificacion.causas)

        for estrella, lista_causas in causas_temp.items():
            contador_causas = {}
            for causa in lista_causas:
                if causa is not None:
                    if causa in contador_causas:
                        contador_causas[causa] += 1
                    else:
                        contador_causas[causa] = 1
            sorted_causas = sorted(contador_causas.items(), key=lambda x: x[1], reverse=True)
            causas[estrella] = ", ".join([f"{causa} ({cantidad})" for causa, cantidad in sorted_causas])
        return causas

    def obtener_promedio_general_del_servicio(self):
        total_calificaciones = 0
        total_estrellas = 0
        for calificacion in self.puntuaciones_calificaciones:
            total_calificaciones += calificacion["cantidad"]
            total_estrellas += calificacion["estrellas"] * calificacion["cantidad"]

        promedio_general = round(total_estrellas / total_calificaciones)
        return promedio_general


class Calificacion(models.Model):
    estrellas = models.IntegerField(default=1)
    causas = models.JSONField(default=list, null=True, blank=True)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True, blank=True)
    id_servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, null=True, blank=True)


class Causas(Enum):
    BUENOS_ACABADOS = "Buenos acabados"
    CONCUERDA_DESCRIPCION = "Concuerda con la descripción"
    BUENA_CALIDAD = "Buena calidad de materiales"
    BUEN_FUNCIONAMIENTO = "Buen funcionamiento"
    NO_CONCUERDA_DESC = "No concuerda con la descripción"
    MALA_CALIDAD = "Mala calidad de materiales"
    MALOS_ACABADOS = "Malos acabados"
    MAL_FUNCIONAMIENTO = "Mal funcionamiento"
    PAQUETE_DANIADO = "Paquete dañado"
    ENTREGA_TARDIA = "Entrega tardía"
    ENTREGA_A_TIEMPO = "Entrega a tiempo"
    ENTREGA_RAPIDA = "Entrega rápida"
    UBICACION_EQUIVOCADA = "Ubicación equivocada"
    ENTREGA_SIN_PERCANCES = "Entrega sin percances"


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
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE, default=1, related_name='pedidos')
    id_pedido = models.AutoField(primary_key=True, unique=True)
    lista_de_productos = models.ManyToManyField(Producto)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='pedidos')
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name='pedidos', default=None, null=True,
                                 blank=True)

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

    def obtener_ingreso_total(self):
        return sum(producto.obtener_precio_total() for producto in self.detalles.all())

    def obtener_costo_total(self):
        return sum(producto.obtener_costo_total() for producto in self.detalles.all())

    def obtener_beneficio_total(self):
        ingreso_total = self.obtener_ingreso_total()
        costo_total = self.obtener_costo_total()
        return ingreso_total - costo_total


class DetalleDePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    def obtener_precio_total(self):
        return self.producto.precio * self.cantidad

    def obtener_costo_total(self):
        return self.producto.costo * self.cantidad


class TipoDeMetrica(models.TextChoices):
    NUMERO_DE_VENTAS = "NV", _("Número de ventas")
    INGRESOS = "IS", _("Ingresos")
    COSTOS = "CS", _("Costos")
    BENEFICIO_POR_VENTA = "BV", _("Beneficio por venta")


class Meta(models.Model):
    metaID = models.AutoField(primary_key=True)
    tipo_de_metrica = models.CharField(max_length=2, choices=TipoDeMetrica)
    valor = models.FloatField(null=True)
    anio = models.IntegerField(null=True)
    mes = models.IntegerField(null=True)
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE, related_name='metas')

    def obtener_tipo_de_metrica(self):  # Necesario?
        return self.tipo_de_metrica

    def obtener_valor(self):  # Necesario?
        return self.valor

    def obtener_anio(self):  # Necesario?
        return self.anio

    def obtener_mes(self):  # Necesario?
        return self.mes

    def __str__(self):
        return f"{self.tipo_de_metrica} / {self.valor}"


class TipoDeComparacion(models.TextChoices):
    INFERIOR = 'IR', _('son inferiores')
    SUPERIOR = 'SR', _('superan')
    IGUAL = 'IL', _('igualan')


class Reporte(models.Model):
    reporteID = models.AutoField(primary_key=True)
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE, related_name='reportes')
    anio = models.IntegerField(null=True)
    mes = models.IntegerField(null=True)

    def determinar_metricas_y_recomendaciones(self):
        for tipo_de_metrica in TipoDeMetrica:
            metrica = self.obtener_metrica(tipo_de_metrica)
            metrica.save()

        recomendaciones = self.obtener_recomendaciones()

    def obtener_metrica(self, tipo_de_metrica):
        metrica = self.metricas.filter(tipo_de_metrica=tipo_de_metrica, reporte=self).first()

        if not metrica:
            metrica = self.metricas.create(tipo_de_metrica=tipo_de_metrica, anio=self.anio, mes=self.anio, reporte=self)
            metrica.save()

        metrica.calcular_metrica(self.vendedor.obtener_ventas_por_fecha(self.anio, self.mes))
        return metrica

    def obtener_comparacion_por_meta(self, tipo_de_metrica):
        metrica = self.obtener_metrica(tipo_de_metrica)
        meta = self.vendedor.obtener_meta(tipo_de_metrica, self.anio, self.mes)
        if meta is not None:
            if metrica.obtener_valor() < meta.obtener_valor():
                return TipoDeComparacion.INFERIOR.label
            elif metrica.obtener_valor() > meta.obtener_valor():
                return TipoDeComparacion.SUPERIOR.label
            else:
                return TipoDeComparacion.IGUAL.label

    def obtener_comparacion_por_mes_anterior(self, tipo_de_metrica):
        metrica_mes_actual = self.obtener_metrica(tipo_de_metrica)
        metrica_mes_anterior = self.obtener_metrica_mes_anterior(tipo_de_metrica)

        if metrica_mes_actual.obtener_valor() < metrica_mes_anterior.obtener_valor():
            return TipoDeComparacion.INFERIOR.label
        elif metrica_mes_actual.obtener_valor() > metrica_mes_anterior.obtener_valor():
            return TipoDeComparacion.SUPERIOR.label
        else:
            return TipoDeComparacion.IGUAL.label

    def obtener_metrica_mes_anterior(self, tipo_de_metrica):
        anio_anterior = self.anio if self.mes > 1 else self.anio - 1
        mes_anterior = self.mes - 1 if self.mes > 1 else 12

        metrica_mes_anterior = self.vendedor.generar_reporte(anio_anterior, mes_anterior).obtener_metrica(
            tipo_de_metrica)

        return metrica_mes_anterior

    def obtener_recomendaciones(self):
        recomendaciones = []

        for tipo_de_metrica in TipoDeMetrica:
            comparacion_meta = self.obtener_comparacion_por_meta(tipo_de_metrica)

            recomendacion_existente = self.recomendaciones.filter(
                contenido=f'{tipo_de_metrica}'
            ).first()

            if not recomendacion_existente:
                recomendacion_existente = self.recomendaciones.create(
                    contenido=''
                )
            recomendacion_existente.determinar_contenido(comparacion_meta, tipo_de_metrica)
            recomendacion_existente.save()
            recomendaciones.append(recomendacion_existente.obtener_contenido().label)
            self.save()

        return recomendaciones

    def obtener_porcentaje_de_avance(self, tipo_de_metrica):
        meta = self.vendedor.obtener_meta(tipo_de_metrica, self.anio, self.mes)
        metrica_actual = self.obtener_metrica(tipo_de_metrica)
        if meta is not None and meta.obtener_valor() != 0:
            porcentaje_de_avance = min(int(metrica_actual.obtener_valor() / meta.obtener_valor() * 100), 100)
        else:
            porcentaje_de_avance = 0

        return porcentaje_de_avance

    def __str__(self):
        return f"{self.vendedor} / {self.anio} / {self.mes}"


class Metrica(models.Model):
    metricaID = models.AutoField(primary_key=True)
    tipo_de_metrica = models.CharField(max_length=19, choices=TipoDeMetrica)
    valor = models.FloatField(null=True)
    anio = models.IntegerField(null=True)
    mes = models.IntegerField(null=True)
    reporte = models.ForeignKey(Reporte, on_delete=models.CASCADE, related_name='metricas')

    def calcular_metrica(self, ventas):
        beneficio_total = 0
        cantidad_ventas = 0
        ingresos_total = 0
        costos_total = 0

        for venta in ventas:
            cantidad_ventas += 1
            ingresos_total += venta.obtener_ingreso_total()
            costos_total += venta.obtener_costo_total()
            beneficio_total += venta.obtener_beneficio_total()

        if cantidad_ventas == 0:
            self.valor = 0
        elif self.tipo_de_metrica == TipoDeMetrica.NUMERO_DE_VENTAS:
            self.valor = cantidad_ventas
        elif self.tipo_de_metrica == TipoDeMetrica.INGRESOS:
            self.valor = ingresos_total
        elif self.tipo_de_metrica == TipoDeMetrica.COSTOS:
            self.valor = costos_total
        elif self.tipo_de_metrica == TipoDeMetrica.BENEFICIO_POR_VENTA and cantidad_ventas > 0:
            self.valor = beneficio_total / cantidad_ventas

        self.save()

    def obtener_valor(self):
        return self.valor

    def __str__(self):
        return f"{self.tipo_de_metrica} / {self.valor}"


class TipoDeRecomendacion(models.TextChoices):
    OFERTA_DE_PRODUCTOS = 'OFERTA_DE_PRODUCTOS', _('Crear oferta en los productos para generar más ventas.')
    MANTENER_PROMOCION_DE_PRODUCTOS = 'MANTENER_PROMOCION_DE_PRODUCTOS', _('Aumentar tu meta para el siguiente mes.')
    COMBO_DE_PRODUCTO = 'COMBO_DE_PRODUCTO', _('Crear combos o conjunto de productos similares.')
    PROMOCION_PRODUCTOS_ESTRELLA = 'PROMOCION_PRODUCTOS_ESTRELLA', _('Promocionar productos estrella.')
    NEGOCIAR_DESCUENTO = 'NEGOCIAR_DESCUENTO', _(
        'Negociar descuentos con proveedores o buscar alternativas más económicas.')
    OPTIMIZAR_PROCESOS = 'OPTIMIZAR_PROCESOS', _('Optimizar procesos internos para reducir costos operativos.')
    AJUSTAR_PRECIO_SOBRE_COSTO = 'AJUSTAR_PRECIO_SOBRE_COSTO', _(
        'Ajustar los precios de los productos con respecto a sus costos.')
    MANTENER_PRECIO_SOBRE_COSTO = 'MANTENER_PRECIO_SOBRE_COSTO', _(
        'Mantener los precios de los productos con respecto a sus costos.')


class Recomendacion(models.Model):
    contenido = models.CharField(max_length=31, choices=TipoDeRecomendacion)
    reporte = models.ForeignKey(Reporte, on_delete=models.CASCADE, related_name='recomendaciones')

    def determinar_contenido(self, comparacion_meta, tipo_de_metrica):
        recomendaciones_por_metrica = {
            TipoDeMetrica.NUMERO_DE_VENTAS: {
                'igual o superior': TipoDeRecomendacion.MANTENER_PROMOCION_DE_PRODUCTOS,
                'inferior': TipoDeRecomendacion.OFERTA_DE_PRODUCTOS
            },
            TipoDeMetrica.INGRESOS: {
                'igual o superior': TipoDeRecomendacion.PROMOCION_PRODUCTOS_ESTRELLA,
                'inferior': TipoDeRecomendacion.COMBO_DE_PRODUCTO
            },
            TipoDeMetrica.COSTOS: {
                'igual o superior': TipoDeRecomendacion.OPTIMIZAR_PROCESOS,
                'inferior': TipoDeRecomendacion.NEGOCIAR_DESCUENTO
            },
            TipoDeMetrica.BENEFICIO_POR_VENTA: {
                'igual o superior': TipoDeRecomendacion.MANTENER_PRECIO_SOBRE_COSTO,
                'inferior': TipoDeRecomendacion.AJUSTAR_PRECIO_SOBRE_COSTO
            }
        }

        recomendacion_al_superar_o_igualar_la_meta = recomendaciones_por_metrica[tipo_de_metrica]['igual o superior']
        recomendacion_al_no_superar_la_meta = recomendaciones_por_metrica[tipo_de_metrica]['inferior']

        if comparacion_meta == TipoDeComparacion.SUPERIOR.label or comparacion_meta == TipoDeComparacion.IGUAL.label:
            self.contenido = recomendacion_al_superar_o_igualar_la_meta
        else:
            self.contenido = recomendacion_al_no_superar_la_meta

    def obtener_contenido(self):
        return self.contenido

    def __str__(self):
        return f"{self.contenido}"
