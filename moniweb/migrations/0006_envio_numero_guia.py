# Generated by Django 5.1.3 on 2024-11-16 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moniweb', '0005_remove_envio_id_servicio_envio_id_factura'),
    ]

    operations = [
        migrations.AddField(
            model_name='envio',
            name='numero_guia',
            field=models.CharField(default=1, max_length=255),
        ),
    ]
