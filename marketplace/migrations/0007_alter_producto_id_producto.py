# Generated by Django 5.0.1 on 2024-03-02 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0006_alter_producto_id_producto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='id_producto',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
