from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords


class Worker(models.Model):
    passport = models.CharField(max_length=255, verbose_name="Паспорт", unique=True)
    fio = models.CharField(max_length=255, verbose_name="ФИО")

    def __str__(self) -> str:
        return self.fio
    
    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
        

class DocType(models.Model):
    slug = models.SlugField(primary_key=True)
    name = models.CharField(_('name'), max_length=255, unique=True)
    main = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = "Тип документа"
        verbose_name_plural = "Тип документов"


class WorkerDoc(models.Model):
    worker = models.ForeignKey(Worker, models.CASCADE, verbose_name="Пользовател")
    type = models.ForeignKey(DocType, models.SET_NULL, null=True, to_field="slug", verbose_name="Тип документа")
    create_date = models.DateField(auto_now_add=True, verbose_name="Дата создание")
    start_date = models.DateField(null=True, blank=True, verbose_name="Дата начало")
    expired_date = models.DateField(null=True, blank=True, verbose_name="Дата окончание")
    file = models.FileField(upload_to="user-docs", null=True, blank=True, verbose_name="Файл")
    history = HistoricalRecords()
    
    class Meta:
        unique_together = (("type", "worker"),)
        verbose_name = "Документа сотрудника"
        verbose_name_plural = "Документы сотрудника"