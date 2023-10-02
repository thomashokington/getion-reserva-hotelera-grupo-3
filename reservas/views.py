

from django.shortcuts import render, redirect,  get_object_or_404
from .models import Habitacion, Reserva, TipoDeHabitacion
from reservas.forms import BusquedaHabitacionForm, CrearReservaForm
from django.db.models import Q
from django.db.models import F
from .utils import calcular_precio_total
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm

def registro(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)  # Usa el formulario personalizado
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('inicio_sesion')
    else:
        form = CustomUserCreationForm()  # Usa el formulario personalizado
    return render(request, 'registro.html', {'form': form})

def inicio_sesion(request):  # Cambia el nombre de la vista a 'inicio_sesion'
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('buscar_habitaciones')
    else:
        form = AuthenticationForm()
    return render(request, 'inicio_sesion.html', {'form': form})

# ...

@login_required
def crear_reserva(request, numero_habitacion):
    habitacion = get_object_or_404(Habitacion, numero=numero_habitacion)

    if request.method == 'POST':
        form = CrearReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.habitacion = habitacion
            reserva.cliente = request.user  # Asigna el cliente actual (usuario autenticado)
            reserva.precio_total = calcular_precio_total(reserva.fecha_entrada, reserva.fecha_salida, habitacion.precio_base)

            # Calcular el monto a pagar (30% del precio total)
            monto_pagar = reserva.precio_total * 0.3
            reserva.monto_pagar = monto_pagar

            # Guardar la reserva
            reserva.save()

            # Redirigir a la vista de confirmación de reserva
            return redirect('confirmar_reserva', reserva_id=reserva.id)
    else:
        form = CrearReservaForm(initial={'cliente': request.user})  # Inicializa con el cliente actual

    return render(request, 'crear_reserva.html', {'form': form, 'habitacion': habitacion})


def confirmar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    return render(request, 'confirmar_reserva.html', {'reserva': reserva})

def detalle_reserva(request, reserva_id):
    reserva = Reserva.objects.get(id=reserva_id)
    return render(request, 'detalle_reserva.html', {'reserva': reserva})

def buscar_habitaciones(request):
    if request.method == 'POST':
        form = BusquedaHabitacionForm(request.POST)
        if form.is_valid():
            tipo_habitacion = form.cleaned_data['tipo_habitacion']
            capacidad_minima = form.cleaned_data['capacidad']
            fecha_entrada = form.cleaned_data['fecha_entrada']
            fecha_salida = form.cleaned_data['fecha_salida']

            # Inicializamos un filtro vacío
            filtro_habitaciones = Q()

            # Si se selecciona un tipo de habitación específico, aplicamos el filtro
            if tipo_habitacion:
                filtro_habitaciones &= Q(tipo_habitacion=tipo_habitacion)

            # Filtrar habitaciones disponibles en función de las fechas, capacidad y tipo de habitación
            habitaciones_disponibles = Habitacion.objects.filter(
                disponible=True,  # Solo habitaciones disponibles
                tipo_habitacion__capacidad__gte=capacidad_minima
            )

            # Filtrar las habitaciones disponibles según las fechas
            if fecha_entrada and fecha_salida:
                reservas_superpuestas = Reserva.objects.filter(
                    Q(habitacion__in=habitaciones_disponibles) &
                    Q(fecha_entrada__lte=fecha_salida, fecha_salida__gte=fecha_entrada)
                )

                # Obtener una lista de habitaciones no disponibles durante esas fechas
                habitaciones_no_disponibles = reservas_superpuestas.values_list('habitacion__id', flat=True)

                # Excluir las habitaciones no disponibles
                habitaciones_disponibles = habitaciones_disponibles.exclude(id__in=habitaciones_no_disponibles)

            # Aplicar el filtro por tipo de habitación si es necesario
            if filtro_habitaciones:
                habitaciones_disponibles = habitaciones_disponibles.filter(filtro_habitaciones).distinct()

            # Obtener los tipos de habitación de las habitaciones disponibles
            tipos_disponibles = TipoDeHabitacion.objects.filter(
                habitacion__in=habitaciones_disponibles
            )

            return render(request, 'resultado_busqueda.html', {'habitaciones': habitaciones_disponibles})
    else:
        form = BusquedaHabitacionForm()

    return render(request, 'buscar_habitaciones.html', {'form': form})

def homepage(request):
    
    return redirect('registro')

def detalle_habitacion(request, numero_habitacion):
    habitacion = Habitacion.objects.get(numero=numero_habitacion)
    return render(request, 'detalle_habitacion.html', {'habitacion': habitacion})
