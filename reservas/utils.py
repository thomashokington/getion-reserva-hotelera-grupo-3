from datetime import date

def calcular_precio_total(fecha_entrada, fecha_salida, precio_base):
    # Calcula la duración de la estancia en días
    duracion_estancia = (fecha_salida - fecha_entrada).days

    # Calcula el precio total multiplicando la duración por el precio base
    precio_total = duracion_estancia * precio_base

    return precio_total
