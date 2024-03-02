from django.db import models

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