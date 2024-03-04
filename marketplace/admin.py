from django.contrib import admin

# Register your models here.
from .models import Vendedor, Producto, Pedido, DetalleDePedido, Meta, Metrica, Categoria

admin.site.register(Categoria)
admin.site.register(Vendedor)
admin.site.register(Producto)
admin.site.register(Pedido)
admin.site.register(DetalleDePedido)
admin.site.register(Meta)
admin.site.register(Metrica)