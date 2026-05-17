# Create your models here.
import calendar
from datetime import date
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from .utils import ultimo_dia_mes

class Estudiante(models.Model):
    codigo = models.CharField(max_length=8)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    nivelogrado = models.CharField(max_length=50)
    seccion = models.CharField(max_length=10, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.codigo} {self.nombres} {self.apellidos} - {self.nivelogrado}"

class Matricula(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    anio_lectivo = models.IntegerField()
    fecha_matricula = models.DateField(auto_now_add=True)

    # Rubros iniciales
    matricula = models.DecimalField(max_digits=8, decimal_places=2)
    mobiliario = models.DecimalField(max_digits=8, decimal_places=2)
    papeleria = models.DecimalField(max_digits=8, decimal_places=2)
    tecnologia = models.DecimalField(max_digits=8, decimal_places=2)
    seguro_escolar = models.DecimalField(max_digits=8, decimal_places=2)
    colegiatura_mensual = models.DecimalField(max_digits=8, decimal_places=2)

    def generar_pendientes(self):
        # Rubros iniciales
        rubros = [
            ("Matrícula", self.matricula),
            ("Mobiliario", self.mobiliario),
            ("Papelería", self.papeleria),
            ("Tecnología", self.tecnologia),
            ("Seguro Escolar", self.seguro_escolar),
        ]
        for concepto, monto in rubros:
            PendientePago.objects.create(
                estudiante=self.estudiante,
                concepto=concepto,
                monto=monto,
                recargo=0,
                pagado=False,
                fecha_vencimiento=self.fecha_matricula  # vencimiento inicial
            )

        # Colegiaturas mensuales
        for mes in range(1, 13):
            fecha_vencimiento = ultimo_dia_mes(self.anio_lectivo, mes)
            PendientePago.objects.create(
                estudiante=self.estudiante,
                concepto=f"Colegiatura {mes}/{self.anio_lectivo}",
                monto=self.colegiatura_mensual,
                recargo=0,
                pagado=False,
                fecha_vencimiento=fecha_vencimiento
            )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Generar pendientes solo si no existen
        if not PendientePago.objects.filter(estudiante=self.estudiante, concepto__icontains="Colegiatura").exists():
            self.generar_pendientes()

    def total_matricula(self):
        return self.matricula + self.mobiliario + self.papeleria + self.tecnologia + self.seguro_escolar

    def __str__(self):
        return f"Matrícula {self.estudiante.nombres} {self.estudiante.apellidos} - {self.anio_lectivo}"

class Colegiatura(models.Model):
    matricula = models.ForeignKey(Matricula, on_delete=models.CASCADE)
    mes = models.CharField(max_length=20)  # Ej: "Enero", "Febrero"
    monto = models.DecimalField(max_digits=8, decimal_places=2)
    pagada = models.BooleanField(default=False)
    fecha_pago = models.DateField(blank=True, null=True)

    def __str__(self):
        estado = "Pagada" if self.pagada else "Pendiente"
        return f"{self.mes} - {self.matricula.estudiante.nombres} ({estado})"

class PendientePago(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    concepto = models.CharField(max_length=100) # Ej: Matrícula, Mobiliario, Papelería, Colegiatura, Seguro Escolar, Otros
    monto = models.DecimalField(max_digits=8, decimal_places=2)
    # recibo = models.ForeignKey("Pago", on_delete=models.SET_NULL, null=True, blank=True)
    recargo = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    pagado = models.BooleanField(default=False)
    fecha_pago = models.DateField(null=True, blank=True)
    fecha_vencimiento = models.DateField(null=True, blank=True)  # ← nuevo campo

    def __str__(self):
        return f"{self.estudiante} - {self.concepto}"

    # def __str__(self):
    #     estado = "Pagado" if self.pagado else "Pendiente"
    #     return f"{self.concepto} - {self.estudiante.nombres} ({estado})"

class Pago(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    recibo_numero = models.CharField(max_length=20, unique=True)
    fecha_pago = models.DateField(auto_now_add=True)
    responsable = models.CharField(max_length=100)
    observacion = models.TextField(blank=True, null=True)

    # Relación con pendientes (usar cadena para evitar referencia antes de definir la clase)
    pendientes = models.ManyToManyField('PendientePago', related_name='pagos')
    
    def total_pago(self):
        return sum(p.monto + p.recargo for p in self.pendientes.all())
    
    def __str__(self):
        return f"Recibo {self.recibo_numero} - {self.estudiante.nombres}"

class Reporte(models.Model):
    """
    Modelo ficticio para habilitar la sección de Reportes en el Admin.
    No crea tabla en la base de datos porque managed=False.
    """
    class Meta:
        verbose_name = "Reporte"
        verbose_name_plural = "Reportes"
        managed = False  # Django no intentará crear tabla en la BD
