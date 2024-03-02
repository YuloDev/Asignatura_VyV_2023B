from enum import Enum

from django.db import models
from django.db.models import JSONField

from modelo.ModeloFeedback import Cliente, Servicio


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
    costo = models.CharField(max_length=2, choices=COSTO,default='BS')
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


class Cliente(models.Model):
    cedula = models.CharField(max_length=10, primary_key=True, unique=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    correo = models.EmailField(max_length=50)
    telefono = models.CharField(max_length=10)

    def calificar_producto(self, estrellas, causas, producto):
        calificacion = Calificacion(estrellas, causas)
        producto.agregar_calificacion(calificacion)

class Producto(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(null=True)
    unidades_vendidas = models.IntegerField()
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE, related_name='productos')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    promocion = models.BooleanField(default=False)
    calificaciones = JSONField(default=dict)

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

    def feedback_producto_esta_dado(self):
        return True

    def aumentar_estrella(self, calificacion_cliente):
        for estrellas, calificacion_total in self.calificaciones.items():
            if estrellas == calificacion_cliente:
                self.calificaciones[estrellas] += 1
                break

    def agregar_calificacion(self, calificacion):
        self.calificaciones_recibidas.append(calificacion)
        self.aumentar_estrella(calificacion.estrellas)

    def obtener_porcentajes_de_calificaciones(self):
        porcentajes_por_estrella = list()
        calificaciones_totales = 0
        for i in self.calificaciones:
            calificaciones_totales += self.calificaciones[i]

        for i in range(1, 6, 1):
            if i in self.calificaciones:
                porcentaje_calculado = (self.calificaciones[i] / calificaciones_totales) * 100
                porcentaje_calculado = round(porcentaje_calculado)
                porcentajes_por_estrella.append(str(porcentaje_calculado) + "%")

        porcentajes_por_estrella.reverse()

        return porcentajes_por_estrella

    def obtener_causas_de_cada_estrella(self):
        causas = {1: "", 2: "", 3: "", 4: "", 5: ""}
        causas_temp = {1: list(), 2: list(), 3: list(), 4: list(), 5: list()}

        for calificacion in self.calificaciones_recibidas:
            causas_temp[calificacion.estrellas].extend(calificacion.causas)

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
            total_estrellas += clave * self.calificaciones[clave]

        promedio_general = round(total_estrellas / total_calificaciones)
        print(promedio_general)
        return promedio_general

class Pedido(models.Model):
    id_pedido = models.AutoField(primary_key=True, unique=True)
    estado_pedido = models.CharField(max_length=50)
    lista_de_productos = models.ManyToManyField(Producto)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='pedidos')

class Servicio(models.Model):

    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="Servicio")
    puntuaciones_calificaciones = JSONField(default=dict)

    def aumentar_estrella(self, calificacion_cliente):
        for calificacion in self.puntuaciones_calificaciones:
            if calificacion["estrellas"] == calificacion_cliente:
                calificacion["cantidad"] += 1
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
            calificacion["porcentaje"] = str(porcentaje_calculado) + "%"

    def obtener_porcentajes_de_calificaciones(self):
        porcentajes_por_estrella = list()
        total_estrellas = sum(calificacion["cantidad"] for calificacion in self.puntuaciones_calificaciones)
        for calificacion in self.puntuaciones_calificaciones:
            porcentaje_calculado = (calificacion["cantidad"] / total_estrellas) * 100
            porcentaje_calculado = round(porcentaje_calculado)
            porcentajes_por_estrella.append(str(porcentaje_calculado) + "%")
        return porcentajes_por_estrella

    def obtener_causas_de_cada_estrella(self, calificaciones_recibidas):
        causas = {1: "", 2: "", 3: "", 4: "", 5: ""}
        causas_temp = {1: list(), 2: list(), 3: list(), 4: list(), 5: list()}

        for calificacion in calificaciones_recibidas:
            causas_temp[calificacion.estrellas].extend(calificacion.causas)

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
        print(promedio_general)
        return promedio_general

class Calificacion(models.Model):
    estrellas = models.IntegerField(default=1)
    causas = models.TextField(default="")
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, default=None)
    id_servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, default=None)




class Causas(Enum):
    BUENOS_ACABADOS = "Buenos acabados"
    CONCUERDA_DESCRIPCION = "Concuerda con la descripción"
    BUENA_CALIDAD = "Buena calidad de materiales"
    BUEN_FUNCIONAMIENTO = "Buen funcionamiento"
    NO_CONCUERDA_DESC = "No concuerda con la descripción"
    MALA_CALIDAD = "Mala calidad de materiales"
    MALOS_ACABADOS = "Malos acabados"
    MAL_FUNCIONAMIENTO = "Mal funcionamiento"


