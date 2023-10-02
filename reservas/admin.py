from django.contrib import admin

from .models import Hotel, TipoDeHabitacion, Habitacion, Cliente, Reserva


admin.site.register(Hotel)
admin.site.register(TipoDeHabitacion)
admin.site.register(Habitacion)
admin.site.register(Cliente)
admin.site.register(Reserva)


