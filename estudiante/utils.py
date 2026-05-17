import calendar
from datetime import date
from django.utils.timezone import now

def ultimo_dia_mes(anio: int, mes: int) -> date:
    """
    Devuelve el último día del mes para un año y mes dados.
    Ejemplo: ultimo_dia_mes(2026, 2) -> 2026-02-28
    """
    ultimo_dia = calendar.monthrange(anio, mes)[1]
    return date(anio, mes, ultimo_dia)

def obtener_fecha_corte(fecha_str: str = None) -> date:
    """
    Devuelve la fecha de corte para reportes.
    - Si se recibe un string en formato YYYY-MM-DD, lo convierte a date.
    - Si no se recibe nada, devuelve la fecha actual.
    """
    if fecha_str:
        try:
            anio, mes, dia = map(int, fecha_str.split("-"))
            return date(anio, mes, dia)
        except ValueError:
            # Si el formato es incorrecto, usar fecha actual
            return now().date()
    return now().date()
