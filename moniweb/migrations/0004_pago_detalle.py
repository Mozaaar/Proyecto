# Generated by Django 5.1.3 on 2024-11-16 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moniweb', '0003_remove_envio_id_guia_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pago',
            name='detalle',
            field=models.TextField(blank=True, null=True),
        ),
    ]
