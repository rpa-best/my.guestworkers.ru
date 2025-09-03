from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class Roles(TextChoices):
    OWNER = ('owner', _('Владелец'))
    CLIENT = ('client', _('Клиент'))
    WORKER = ('worker', _('Сотрудник'))



class Statuses(TextChoices):
    CHECKING = ('checking', _('На проверка'))
    DONE = ('done', _('Праверено'))
