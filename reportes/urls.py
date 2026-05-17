# reportes/urls.py
from django.urls import path
from . import views

app_name = "reportes"

urlpatterns = [
    path("", views.reportes_menu, name="menu"),
    path("pendientes/", views.reporte_pendientes, name="reporte_pendientes_admin"),
    path("pagos-mensuales/", views.reporte_pagos_mensuales, name="reporte_pagos_mensuales"),
    path("balance/", views.reporte_balance_general, name="reporte_balance_general"),
    path("morosidad/", views.reporte_morosidad, name="reporte_morosidad_admin"),
    # Aquí añadiremos más reportes
]
