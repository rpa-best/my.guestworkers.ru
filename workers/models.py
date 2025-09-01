from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords

SOON_EXPIRE_LIMIT = timezone.timedelta(days=5)
UPLOAD_KWARGS_PASSPORT = 'Серия, номер паспорта'
UPLOAD_KWARGS = (
    ('first_name', 'Имя', 'Пётр'),
    ('last_name', 'Фамилия', 'Петров'),
    ('surname', 'Отчество', 'Петрович'),
    ('passport', UPLOAD_KWARGS_PASSPORT, "99 99 999999"),
)
DEFAULT_DOC_TYPES = [
    {'slug': 'chek_do', 'name': 'Чек до '},
    {'slug': 'polis_oms_do', 'name': 'Полис ОМС до'},
    {'slug': 'polis_dms_do', 'name': 'Полис ДМС до'},
    {'slug': 'projivanie_do', 'name': 'Разрешение на временное проживание до'},
    {'slug': 'jitelstvo_o', 'name': 'Вид на жительство до'},
    {'slug': 'potent_do', 'name': 'патент до'},
]
DOC_STATUS_NORM = "norm"
DOC_STATUS_EXPIRED = "expired"
DOC_STATUS_SOON_EXPIRED = "soon_expired"
DOC_STATUS = (
    (DOC_STATUS_EXPIRED, DOC_STATUS_EXPIRED),
    (DOC_STATUS_SOON_EXPIRED, DOC_STATUS_SOON_EXPIRED),
    (DOC_STATUS_NORM, DOC_STATUS_NORM),
)


class Worker(models.Model):
    passport = models.CharField(max_length=255, verbose_name="Паспорт", unique=True)
    fio = models.CharField(max_length=255, verbose_name="ФИО")

    def __str__(self) -> str:
        return self.fio

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
        unique_together = (("type", "user"),)
        verbose_name = "Документа сотрудника"
        verbose_name_plural = "Документы сотрудника"