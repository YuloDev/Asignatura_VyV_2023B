# Generated by Django 5.0.1 on 2024-03-03 18:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vendedor',
            name='apellido',
        ),
    ]
