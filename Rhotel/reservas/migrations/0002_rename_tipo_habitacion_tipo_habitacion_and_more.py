# Generated by Django 4.2.5 on 2023-09-26 01:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='habitacion',
            old_name='tipo',
            new_name='tipo_habitacion',
        ),
        migrations.AlterField(
            model_name='hotel',
            name='estrellas',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='tipodehabitacion',
            name='capacidad',
            field=models.IntegerField(),
        ),
    ]