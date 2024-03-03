from django.db import models
from django.template.defaultfilters import default


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


class Vendedor(models.Model):
    id_vendedor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, default="")


class Promocion(models.Model):
    id_promocion = models.AutoField(primary_key=True)
    paquete = models.CharField(max_length=30)
    costo = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    dias_duracion = models.IntegerField(default=0)


class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50, default="")
    unidades_vendidas = models.IntegerField(default=0)
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE, null=True)
    promocion = models.ForeignKey(Promocion, on_delete=models.CASCADE, null=True)

    def ha_superado_record(self):
        return self.categoria.supera_record(self.unidades_vendidas)




