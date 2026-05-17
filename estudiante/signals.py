from django.db.models.signals import m2m_changed
from django.utils.timezone import now
from .models import Pago, PendientePago

def actualizar_pendientes(sender, instance, action, pk_set, **kwargs):
    # Solo después de agregar pendientes al pago
    if action == "post_add":
        for pendiente_id in pk_set:
            pendiente = PendientePago.objects.get(pk=pendiente_id)
            pendiente.pagado = True
            pendiente.fecha_pago = now().date()
            pendiente.save()

# Conectar la señal al modelo Pago
m2m_changed.connect(actualizar_pendientes, sender=Pago.pendientes.through)
