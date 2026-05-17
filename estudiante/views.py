# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import now
from .models import Pago, PendientePago
from django.http import HttpResponse
from datetime import datetime, date
from .utils import obtener_fecha_corte

def saludo(request):
    return HttpResponse("Hola, bienvenido al sistema del colegio.")

def despedida(request):
    return HttpResponse("Hasta pronto, gracias por tu visita.")

def recibo_view(request, pago_id):
    # Busca el pago por su ID
    pago = get_object_or_404(Pago, id=pago_id)
    # Renderiza la plantilla con los datos del pago
    return render(request, "estudiante/recibo.html", {"pago": pago})

def reporte_pendientes(request):
    fecha_consulta = obtener_fecha_corte(request.GET.get("fecha"))
    pendientes = PendientePago.objects.filter(
        pagado=False,
        fecha_vencimiento__lte=fecha_consulta
    ).select_related("estudiante")

    # pendientes = PendientePago.objects.filter(pagado=False).select_related("estudiante")
    return render(request, "estudiante/reporte_pendientes.html", {"pendientes": pendientes})

def reporte_morosidad(request):
    # Obtener fecha de corte desde el formulario

    fecha_corte = obtener_fecha_corte(request.GET.get("fecha"))
    # usar fecha_corte en tus filtros

    fecha_consulta = request.GET.get("fecha")
    if fecha_consulta:
        fecha_consulta = datetime.strptime(fecha_consulta, "%Y-%m-%d").date()
    else:
        fecha_consulta = date.today()

    # Filtrar colegiaturas vencidas
    pendientes = PendientePago.objects.filter(
        pagado=False,
        concepto__icontains="Colegiatura",
        fecha_vencimiento__lt=fecha_consulta
    ).select_related("estudiante")

    # Agrupar por estudiante
    estudiantes = {}
    for p in pendientes:
        if p.estudiante.id not in estudiantes:
            estudiantes[p.estudiante.id] = {
                "nombres": p.estudiante.nombres,
                "apellidos": p.estudiante.apellidos,
                "pendientes": [],
                "total_vencido": 0,
                "meses_pendientes": 0,
            }
        estudiantes[p.estudiante.id]["pendientes"].append(p)
        estudiantes[p.estudiante.id]["total_vencido"] += p.monto
        estudiantes[p.estudiante.id]["meses_pendientes"] += 1

    return render(request, "estudiante/reporte_morosidad.html", {
        "estudiantes": estudiantes.values(),
        "fecha_consulta": fecha_consulta,
    })
