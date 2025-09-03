from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_delete
from django.core.exceptions import ValidationError
from django.dispatch import receiver

from .api import Api


class WorkerInvoice(models.Model):
    id = models.BigIntegerField(primary_key=True, verbose_name='ID')
    worker = models.ForeignKey('workers.Worker', models.CASCADE, verbose_name=_('Сотрудник'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создания'))

    class Meta:
        verbose_name = "Инвойс"
        verbose_name_plural = "Инвойсы"

    @property
    def data(self):
        api = Api()
        response = api.get_order(self.id)
        if not response.ok:
            return {"id": self.id, "error": response.text}
        return response.json()
    
    def __str__(self):
        return f"Инвойс №-{self.id}"


@receiver(pre_delete, sender=WorkerInvoice)
def delete_worker_invoice(sender, instance: WorkerInvoice, **kwargs):
    api = Api()
    response = api.delete_order(instance.id)
    if not response.ok:
        raise ValidationError(f"Ошибка API: {response.text}")
