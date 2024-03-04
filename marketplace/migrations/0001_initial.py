# Generated by Django 5.0.1 on 2024-03-04 00:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id_categoria', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('record_ventas', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('cedula', models.CharField(max_length=10, primary_key=True, serialize=False, unique=True)),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
                ('correo', models.EmailField(max_length=50)),
                ('telefono', models.CharField(max_length=10)),
                ('preferencias', models.CharField(blank=True, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Promocion',
            fields=[
                ('id_promocion', models.AutoField(primary_key=True, serialize=False)),
                ('paquete', models.CharField(max_length=30)),
                ('costo', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('dias_duracion', models.IntegerField(default=0)),
                ('fecha_inicio', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Reporte',
            fields=[
                ('reporteID', models.AutoField(primary_key=True, serialize=False)),
                ('anio', models.IntegerField(null=True)),
                ('mes', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Servicio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('puntuaciones_calificaciones', models.JSONField(default=dict)),
            ],
        ),
        migrations.CreateModel(
            name='Vendedor',
            fields=[
                ('vendedorID', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id_producto', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(default='', max_length=50)),
                ('unidades_vendidas', models.IntegerField(default=0, null=True)),
                ('calificaciones', models.JSONField(default=dict, null=True)),
                ('precio', models.FloatField(null=True)),
                ('costo', models.FloatField(null=True)),
                ('categoria', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='marketplace.categoria')),
                ('promocion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='marketplace.promocion')),
                ('vendedor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='productos', to='marketplace.vendedor')),
            ],
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('etapa_pedido', models.CharField(choices=[('PC', 'precompra'), ('R', 'reserva'), ('LE', 'listo_para_entregar'), ('RA', 'Repartidor asignado'), ('E', 'Embarcado'), ('PNE', 'Paquete no entregado'), ('PE', 'Paquete entregado')], default='PC', max_length=20, null=True)),
                ('estado_pedido', models.CharField(choices=[('AT', 'a_tiempo'), ('A', 'atrasado'), ('C', 'cancelado'), ('CNE', 'Cliente no encontrado')], default='AT', max_length=20, null=True)),
                ('pedido_activo', models.BooleanField(default=True)),
                ('fecha_creacion_pedido', models.DateField(null=True)),
                ('fecha_etapa_precompra', models.DateField(blank=True, null=True)),
                ('fecha_etapa_reserva', models.DateField(blank=True, null=True)),
                ('fecha_listo_para_entregar', models.DateField(blank=True, null=True)),
                ('cliente_no_encontrado', models.BooleanField(default=False)),
                ('fecha_real_etapa_precompra', models.DateField(blank=True, null=True)),
                ('fecha_real_etapa_reserva', models.DateField(blank=True, null=True)),
                ('fecha_real_etapa_listo_para_entregar', models.DateField(blank=True, null=True)),
                ('id_pedido', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pedidos', to='marketplace.cliente')),
                ('lista_de_productos', models.ManyToManyField(to='marketplace.producto')),
                ('servicio', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pedidos', to='marketplace.servicio')),
                ('vendedor', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='pedidos', to='marketplace.vendedor')),
            ],
        ),
        migrations.CreateModel(
            name='DetalleDePedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalles', to='marketplace.pedido')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketplace.producto')),
            ],
        ),
        migrations.CreateModel(
            name='Recomendacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contenido', models.CharField(choices=[('OFERTA_DE_PRODUCTOS', 'Crear oferta en los productos para generar más ventas.'), ('MANTENER_PROMOCION_DE_PRODUCTOS', 'Aumentar tu meta para el siguiente mes.'), ('COMBO_DE_PRODUCTO', 'Crear combos o conjunto de productos similares.'), ('PROMOCION_PRODUCTOS_ESTRELLA', 'Promocionar productos estrella.'), ('NEGOCIAR_DESCUENTO', 'Negociar descuentos con proveedores o buscar alternativas más económicas.'), ('OPTIMIZAR_PROCESOS', 'Optimizar procesos internos para reducir costos operativos.'), ('AJUSTAR_PRECIO_SOBRE_COSTO', 'Ajustar los precios de los productos con respecto a sus costos.'), ('MANTENER_PRECIO_SOBRE_COSTO', 'Mantener los precios de los productos con respecto a sus costos.')], max_length=31)),
                ('reporte', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recomendaciones', to='marketplace.reporte')),
            ],
        ),
        migrations.CreateModel(
            name='Metrica',
            fields=[
                ('metricaID', models.AutoField(primary_key=True, serialize=False)),
                ('tipo_de_metrica', models.CharField(choices=[('NV', 'Número de ventas'), ('IS', 'Ingresos'), ('CS', 'Costos'), ('BV', 'Beneficio por venta')], max_length=19)),
                ('valor', models.FloatField(null=True)),
                ('anio', models.IntegerField(null=True)),
                ('mes', models.IntegerField(null=True)),
                ('reporte', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='metricas', to='marketplace.reporte')),
            ],
        ),
        migrations.CreateModel(
            name='Calificacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estrellas', models.IntegerField(default=1)),
                ('causas', models.JSONField(blank=True, default=list, null=True)),
                ('id_producto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='marketplace.producto')),
                ('id_servicio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='marketplace.servicio')),
            ],
        ),
        migrations.AddField(
            model_name='servicio',
            name='vendedor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='servicios', to='marketplace.vendedor'),
        ),
        migrations.AddField(
            model_name='reporte',
            name='vendedor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reportes', to='marketplace.vendedor'),
        ),
        migrations.CreateModel(
            name='Meta',
            fields=[
                ('metaID', models.AutoField(primary_key=True, serialize=False)),
                ('tipo_de_metrica', models.CharField(choices=[('NV', 'Número de ventas'), ('IS', 'Ingresos'), ('CS', 'Costos'), ('BV', 'Beneficio por venta')], max_length=2)),
                ('valor', models.FloatField(null=True)),
                ('anio', models.IntegerField(null=True)),
                ('mes', models.IntegerField(null=True)),
                ('vendedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='metas', to='marketplace.vendedor')),
            ],
        ),
    ]
