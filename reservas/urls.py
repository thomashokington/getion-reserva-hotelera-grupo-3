from django.urls import path
from . import views

urlpatterns = [
    
    path('buscar_habitaciones/', views.buscar_habitaciones, name='buscar_habitaciones'),
    path('crear_reserva/<int:habitacion_id>/', views.crear_reserva, name='crear_reserva'),
    path('', views.homepage, name='homepage'),

 
]