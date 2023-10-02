

from django import forms
from django.core.exceptions import ValidationError
from .models import TipoDeHabitacion, Habitacion, Reserva
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class BusquedaHabitacionForm(forms.Form):
    tipo_habitacion = forms.ModelChoiceField(
        queryset=TipoDeHabitacion.objects.all(),
        empty_label="Cualquier tipo",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    fecha_entrada = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})) 
    fecha_salida = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    capacidad = forms.IntegerField(min_value=1, label='Capacidad mínima', widget=forms.TextInput(attrs={'class': 'form-control'}))

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

            

        return cleaned_data
    
class CustomUserCreationForm(UserCreationForm):
    correo = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    nombre = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    apellido = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'correo', 'nombre', 'apellido']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Elimina los mensajes de ayuda para las contraseñas
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''