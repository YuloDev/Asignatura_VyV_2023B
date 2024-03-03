from django.contrib import admin

# Register your models here.
from .models import Vendedor, Producto, Promocion, Pedido

admin.site.register(Vendedor)
admin.site.register(Producto)
admin.site.register(Promocion)
admin.site.register(Pedido)