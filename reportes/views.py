# Create your views here.
from django.shortcuts import render
from datetime import datetime, date
from estudiante.models import PendientePago, Pago  # si PendientePago está en esta app, si no importa desde estudiante.models
from django.utils.timezone import now
from django.db.models import Sum

# Menú principal
def reportes_menu(request):
    return render(request, "reportes/reportes_menu.html")

# Reporte de Pagos Pendientes
def reporte_pendientes(request):
    fecha_consulta = request.GET.get("fecha")
    if fecha_consulta:
        from datetime import datetime
        fecha_consulta = datetime.strptime(fecha_consulta, "%Y-%m-%d").date()
    else:
        fecha_consulta = now().date()

    pendientes = PendientePago.objects.filter(
        pagado=False,
        fecha_vencimiento__lte=fecha_consulta
    ).select_related("estudiante")

    estudiantes = {}
    for p in pendientes:
        if p.estudiante.id not in estudiantes:
            estudiantes[p.estudiante.id] = {
                "nombres": p.estudiante.nombres,
                "apellidos": p.estudiante.apellidos,
                "pendientes": []
            }
        estudiantes[p.estudiante.id]["pendientes"].append(p)

    return render(request, "reportes/reporte_pendientes.html", {
        "estudiantes": estudiantes.values(),
        "fecha_consulta": fecha_consulta,
    })

# Reporte de Pagos Mensuales
def reporte_pagos_mensuales(request):
    hoy = now().date()
    pagos = Pago.objects.filter(fecha_pago__month=hoy.month, fecha_pago__year=hoy.year)
    return render(request, "reportes/reporte_pagos_mensuales.html", {
        "pagos": pagos,
        "mes": hoy.month
    })

# Reporte Balance General
def reporte_balance_general(request):
    balance = Pago.objects.aggregate(total_ingresos=Sum("total_pago"))
    return render(request, "reportes/reporte_balance.html", {"balance": balance})

def reporte_morosidad(request):
    fecha_consulta = request.GET.get("fecha")
    if fecha_consulta:
        fecha_consulta = datetime.strptime(fecha_consulta, "%Y-%m-%d").date()
    else:
        fecha_consulta = date.today()

    pendientes = PendientePago.objects.filter(
        pagado=False,
        concepto__icontains="Colegiatura",
        fecha_vencimiento__lt=fecha_consulta
    ).select_related("estudiante")

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
