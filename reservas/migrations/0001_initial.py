# Generated by Django 4.2.5 on 2023-09-25 20:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('apellido', models.CharField(max_length=255)),
                ('correo', models.EmailField(max_length=255)),
                ('telefono', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Habitacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(max_length=20)),
                ('disponible', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('ubicacion', models.CharField(max_length=255)),
                ('descripcion', models.TextField()),
                ('estrellas', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TipoDeHabitacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('descripcion', models.TextField()),
                ('precio_base', models.DecimalField(decimal_places=2, max_digits=10)),
                ('capacidad', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_entrada', models.DateField()),
                ('fecha_salida', models.DateField()),
                ('precio_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservas.cliente')),
                ('habitacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservas.habitacion')),
            ],
        ),
        migrations.AddField(
            model_name='habitacion',
            name='hotel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservas.hotel'),
        ),
        migrations.AddField(
            model_name='habitacion',
            name='tipo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservas.tipodehabitacion'),
        ),
    ]