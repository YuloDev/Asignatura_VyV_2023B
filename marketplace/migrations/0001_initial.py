# Generated by Django 5.0.1 on 2024-03-03 05:54

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
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('record', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Promocion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_inicio', models.DateField()),
                ('tipo_promocion', models.CharField(choices=[('GD', 'Gold'), ('PG', 'Platinum'), ('BS', 'Basic')], max_length=2)),
                ('costo', models.CharField(choices=[('GD', 50), ('PG', 35), ('BS', 20)], default='BS', max_length=2)),
                ('dias_duracion', models.IntegerField()),
                ('cantidad_productos', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Vendedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20)),
                ('apellido', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('unidades_vendidas', models.IntegerField()),
                ('promocion', models.BooleanField(default=False)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketplace.categoria')),
                ('vendedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='productos', to='marketplace.vendedor')),
            ],
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado_pedido', models.CharField(choices=[('AT', 'A tiempo'), ('A', 'Atrasado'), ('CNE', 'Cliente no encontrado')], default='AT', max_length=3)),
                ('etapa_pedido', models.CharField(choices=[('LPE', 'Listo para entregar'), ('RA', 'Repartidor asignado'), ('E', 'Embarcado'), ('PNE', 'Paquete no entregado'), ('PE', 'Paquete entregado')], default='LPE', max_length=3)),
                ('fecha_listo_para_entregar', models.DateField()),
                ('cliente_no_encontrado', models.BooleanField(default=False)),
                ('vendedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketplace.vendedor')),
            ],
        ),
    ]
