from django.db import models
from django.db.models import JSONField

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

class Calificacion(models.Model):
    def __init__(self, estrellas, causas):
        self.estrellas = estrellas
        self.causas = causas


class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(null=True)
    unidades_vendidas = models.IntegerField()
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE, related_name='productos')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    promocion = models.BooleanField(default=False)
    calificaciones = JSONField(default=dict)
    calificaciones_recibidas = models.ManyToManyField(Calificacion)

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

