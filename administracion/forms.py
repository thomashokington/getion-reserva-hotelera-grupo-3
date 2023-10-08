from django import forms
from django.core.exceptions import ValidationError
from reservas.models import TipoDeHabitacion, Habitacion, Reserva


class CrearHabitacionForm(forms.ModelForm):
    class Meta:
        model = Habitacion
        fields = ['hotel', 'tipo_habitacion', 'numero']