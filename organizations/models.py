from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords
from .choices import Statuses, Roles


class Organization(models.Model):
    name = models.CharField("Название", max_length=255, blank=True, null=True)
    inn = models.CharField("ИНН", max_length=20, primary_key=True)
    bik = models.CharField("ВИК", max_length=255, blank=True, null=True)
    address = models.CharField("Адрес", max_length=255, blank=True, null=True)
    phone = models.CharField("Телефон", max_length=20, blank=True, null=True)
    ogrn = models.CharField("ОГРН", max_length=20, blank=True, null=True)
    kpp = models.CharField("КПП", max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True, verbose_name="Почта")
    phone_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Контактное лицо")
    gen_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Генеральный директор")
    r_s = models.CharField(max_length=255, blank=True, null=True, verbose_name="р/с")
    k_s = models.CharField(max_length=255, blank=True, null=True, verbose_name="к/с")
    has_skud = models.BooleanField(default=False, verbose_name="СКУД")

    history = HistoricalRecords()

    class Meta:
        verbose_name = "Организация"
        verbose_name_plural = "Организации"

    def __str__(self) -> str:
        return self.name if self.name else self.inn
    
class WorkerToOrganization(models.Model):
    org = models.ForeignKey(Organization, models.CASCADE, verbose_name=_('Организация'))
    worker = models.ForeignKey('workers.Worker', models.CASCADE, verbose_name=_('Пользовател'))
    status = models.CharField(max_length=20, choices=Statuses.choices, null=True, verbose_name=_('Статус'))
    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.WORKER, verbose_name=_('Роль'))
    
    class Meta:
        unique_together = (("org", "worker"),)
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    def __str__(self) -> str:
        return str(self.worker)
    

class OrganizationDoc(models.Model):
    org = models.ForeignKey(Organization, models.CASCADE)
    file = models.FileField(upload_to="orgdocs/")
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL, verbose_name=_('Пользовател'), blank=True, null=True)

    class Meta:
        verbose_name = "Ведомость"
        verbose_name_plural = "Ведомости"


class OrganizationTabel(models.Model):
    org = models.ForeignKey(Organization, models.CASCADE)
    worker = models.ForeignKey('workers.Worker', models.CASCADE)
    date = models.DateField()
    value = models.FloatField()
    editable = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Табель"
        verbose_name_plural = "Табели"


class DocumentType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Document(models.Model):
    date = models.DateField()
    org = models.ForeignKey(Organization, models.CASCADE)
    type = models.ForeignKey(DocumentType, models.CASCADE)
    file = models.FileField(upload_to="doc/")