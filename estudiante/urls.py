from django.urls import path
from . import views

app_name = "estudiante"

urlpatterns = [
    path("saludo/", views.saludo, name="saludo"),
    path("despedida/", views.despedida, name="despedida"),
    path("recibo/<int:pago_id>/", views.recibo_view, name="recibo"),
    path("pendientes/", views.reporte_pendientes, name="reporte_pendientes_estudiante"),
    path("morosidad/", views.reporte_morosidad, name="reporte_morosidad_estudiante"),
]
