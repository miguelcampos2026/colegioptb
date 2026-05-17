# Register your models here.
from django.urls import path
from django.contrib import admin
from django.urls import reverse
from django.shortcuts import render
from django.utils.html import format_html

# Creamos un AdminSite personalizado
class ReportesAdminSite(admin.AdminSite):
    site_header = "Administración Colegio Primer Templo Bíblico"
    site_title = "Panel Administrativo"
    index_title = "Bienvenido al Panel"

    def index(self, request, extra_context=None):
        # Generamos el link al menú de reportes
        reportes_url = reverse("reportes_menu")  # apunta a la vista de tu menú
        extra_context = extra_context or {}
        extra_context["reportes_link"] = format_html(
            '<p><a href="{}" class="button" style="background:#007BFF; color:white; padding:8px 12px; border-radius:5px; text-decoration:none;">📊 Reportes Administrativos</a></p>',
            reportes_url
        )
        return super().index(request, extra_context=extra_context)

class ReportesAdmin(admin.ModelAdmin):
    change_list_template = "admin/change_list.html"

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['reportes_link'] = format_html(
            '<a href="/reportes/" class="button">📊 Ir al Menú de Reportes Administrativos</a>'
        )
        return super().changelist_view(request, extra_context=extra_context)
