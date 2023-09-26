

from django.shortcuts import render, redirect
from .models import Habitacion, Reserva, TipoDeHabitacion
from reservas.forms import BusquedaHabitacionForm, CrearReservaForm
from django.db.models import Q
from django.db.models import F
from .utils import calcular_precio_total
from django.shortcuts import redirect




def crear_reserva(request, habitacion_id):
    habitacion = Habitacion.objects.get(id=habitacion_id)

    if request.method == 'POST':
        form = CrearReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.habitacion = habitacion
            reserva.precio_total = calcular_precio_total(reserva.fecha_entrada, reserva.fecha_salida, habitacion.precio_base)

            # Calcular el monto a pagar (30% del precio total)
            monto_pagar = reserva.precio_total * 0.3
            reserva.monto_pagar = monto_pagar

            # Guardar la reserva
            reserva.save()

            # Aquí puedes redirigir a una página de pago o confirmación de reserva
            return redirect('confirmar_reserva', reserva.id)
    else:
        form = CrearReservaForm()

    return render(request, 'crear_reserva.html', {'form': form, 'habitacion': habitacion})
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
    
    return redirect('reservas/buscar_habitaciones/')