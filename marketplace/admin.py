from django.contrib import admin

# Register your models here.
from .models import VendedorG3, ProductoG3, PedidoG3, Pedido_ProductoG3, MetaG3, MetricaG3

admin.site.register(VendedorG3)
admin.site.register(ProductoG3)
admin.site.register(PedidoG3)
admin.site.register(Pedido_ProductoG3)
admin.site.register(MetaG3)
admin.site.register(MetricaG3)
