from django.contrib import admin

# Register your models here.
from .models import Categoria, Vendedor, Producto, Promocion, Pedido

admin.site.register(Categoria)
admin.site.register(Vendedor)
admin.site.register(Producto)
admin.site.register(Promocion)

admin.site.register(Pedido)