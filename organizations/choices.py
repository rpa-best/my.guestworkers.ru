from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class Roles(TextChoices):
    OWNER = ('owner', _('Owner'))
    CLIENT = ('client', _('Client'))
    WORKER = ('worker', _('Worker'))



class Statuses(TextChoices):
    CHECKING = ('checking', _('Checking'))
    DONE = ('done', _('Done'))