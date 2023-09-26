

from django import forms
from django.core.exceptions import ValidationError
from .models import TipoDeHabitacion, Habitacion, Reserva

class BusquedaHabitacionForm(forms.Form):
    tipo_habitacion = forms.ModelChoiceField(
        queryset=TipoDeHabitacion.objects.all(),
        empty_label="Cualquier tipo",
        required=False
    )
    fecha_entrada = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    fecha_salida = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    capacidad = forms.IntegerField(min_value=1, label='Capacidad mínima')

class CrearReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['cliente', 'habitacion', 'fecha_entrada', 'fecha_salida']
    
    def clean(self):
        cleaned_data = super().clean()
        fecha_entrada = cleaned_data.get('fecha_entrada')
        fecha_salida = cleaned_data.get('fecha_salida')
        habitacion = cleaned_data.get('habitacion')

        if fecha_entrada and fecha_salida and habitacion:
            if fecha_entrada >= fecha_salida:
                raise ValidationError('La fecha de entrada debe ser anterior a la fecha de salida.')

            # Agrega más validaciones según tus necesidades

        return cleaned_data