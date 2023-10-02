

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User

class Hotel(models.Model):
    nombre = models.CharField(max_length=255)
    ubicacion = models.CharField(max_length=255)
    descripcion = models.TextField()
    estrellas = models.IntegerField()

    def __str__(self):
        return self.nombre

    # ...

class TipoDeHabitacion(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    precio_base = models.DecimalField(max_digits=10, decimal_places=2)
    capacidad = models.IntegerField()

    def __str__(self):
        return self.nombre

    # ...

class Habitacion(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    tipo_habitacion = models.ForeignKey(TipoDeHabitacion, on_delete=models.CASCADE)
    numero = models.CharField(max_length=20)
    # Elimina los campos fecha_disponible_inicio y fecha_disponible_fin
    disponible = models.BooleanField(default=True)  # Cambia esto a un campo booleano para disponibilidad

    def __str__(self):
        return self.numero
    # ...




class Cliente(models.Model):
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    correo = models.EmailField(max_length=255)
    telefono = models.CharField(max_length=20)

    # ...
class Reserva(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE)
    fecha_entrada = models.DateField()
    fecha_salida = models.DateField()
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)

@receiver(pre_save, sender=Reserva)
def actualizar_disponibilidad(sender, instance, **kwargs):
    habitacion = instance.habitacion
    fecha_entrada = instance.fecha_entrada
    fecha_salida = instance.fecha_salida

    if habitacion and fecha_entrada and fecha_salida:
        # Obtén todas las reservas que se superponen con las fechas de la nueva reserva
        reservas_superpuestas = Reserva.objects.filter(
            habitacion=habitacion,
            fecha_entrada__lte=fecha_salida,
            fecha_salida__gte=fecha_entrada
        )

        # Si hay reservas superpuestas, marca la habitación como no disponible
        if reservas_superpuestas.exists():
            habitacion.disponible = False
        else:
            # Si no hay reservas superpuestas, marca la habitación como disponible
            habitacion.disponible = True

        # Guarda los cambios en la disponibilidad de la habitación
        habitacion.save()


@receiver(pre_save, sender=Reserva)
def calcular_precio_total(sender, instance, **kwargs):
    habitacion = instance.habitacion
    fecha_entrada = instance.fecha_entrada
    fecha_salida = instance.fecha_salida
    if habitacion and fecha_entrada and fecha_salida:
       
        precio_total = calcular_precio_total(fecha_entrada, fecha_salida, habitacion.precio_base)
        instance.precio_total = precio_total