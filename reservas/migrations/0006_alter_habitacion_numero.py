# Generated by Django 4.2.5 on 2023-10-08 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0005_alter_reserva_cliente'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habitacion',
            name='numero',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]