from django.contrib import admin

# Register your models here.
from .models import Vendedor, Producto, Pedido, Meta, Metrica

admin.site.register(Vendedor)
admin.site.register(Producto)
admin.site.register(Pedido)
admin.site.register(Meta)
admin.site.register(Metrica)
