from django.urls import path
from . import views

urlpatterns = [
    

    path('', views.panel_admin, name='panel_admin'),
    path('crear_habitacion/', views.crear_habitacion, name='crear_habitacion'),
    path('habitaciones', views.mostrar_habitacion, name='mostrar_habitacion'),
    path('det_habitacion/<int:hab_id>', views.det_habitacion, name='det_habitacion'),
  
 
]