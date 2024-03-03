# Generated by Django 5.0.1 on 2024-03-02 16:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PedidoG3',
            fields=[
                ('pedidoID', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_listo_para_entregar', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='ProductoG3',
            fields=[
                ('productoID', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('precio', models.FloatField()),
                ('costo', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='VendedorG3',
            fields=[
                ('vendedorID', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Pedido_ProductoG3',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketplace.pedidog3')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketplace.productog3')),
            ],
        ),
        migrations.AddField(
            model_name='productog3',
            name='vendedor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketplace.vendedorg3'),
        ),
        migrations.AddField(
            model_name='pedidog3',
            name='vendedor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketplace.vendedorg3'),
        ),
        migrations.CreateModel(
            name='MetricaG3',
            fields=[
                ('metricaID', models.AutoField(primary_key=True, serialize=False)),
                ('tipo_de_metrica', models.CharField(max_length=100)),
                ('valor', models.FloatField()),
                ('anio', models.IntegerField()),
                ('mes', models.IntegerField()),
                ('vendedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketplace.vendedorg3')),
            ],
        ),
        migrations.CreateModel(
            name='MetaG3',
            fields=[
                ('metaID', models.AutoField(primary_key=True, serialize=False)),
                ('tipo_de_metrica', models.CharField(max_length=100)),
                ('valor', models.FloatField()),
                ('anio', models.IntegerField()),
                ('mes', models.IntegerField()),
                ('vendedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketplace.vendedorg3')),
            ],
        ),
    ]