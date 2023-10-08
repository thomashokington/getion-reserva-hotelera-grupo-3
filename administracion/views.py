from django.shortcuts import render, redirect, get_object_or_404
from .forms import CrearHabitacionForm
from reservas.models import Habitacion


# Create your views here.

def crear_habitacion(request):
    if request.method == 'POST':
        try:
            form = CrearHabitacionForm(request.POST)
            new_task=form.save(commit=False)
            new_task.save()
            return redirect ('panel_admin')

        except:
            return render(request, 'crear_habitacion.html', {'form': CrearHabitacionForm, 'error':'Número de habitacion ocupado'}) 
        

    

    return render(request, 'crear_habitacion.html', {'form': CrearHabitacionForm}) 

def panel_admin(request):

    return render(request, 'panel_administracion.html')

def det_habitacion(request, hab_id):
    if request.method == 'GET':
        habitacion= get_object_or_404(Habitacion, numero=hab_id)
        form=CrearHabitacionForm(instance=habitacion)
    else:
        habitacion= get_object_or_404(Habitacion, numero=hab_id)
        form=CrearHabitacionForm(request.POST, instance=habitacion)
        form.save()
        return redirect('mostrar_habitacion')

    return render(request, 'det_habitacion.html', {'habitacion':habitacion, 'form':form})

def mostrar_habitacion(request):
    habitaciones=Habitacion.objects.all()

    return render(request, 'mostrar_habitacion.html', {'habitaciones':habitaciones})