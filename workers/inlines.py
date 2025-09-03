from unfold.admin import TabularInline
from .models import WorkerDoc


class WorkerDocInline(TabularInline):
    model = WorkerDoc
    extra = 0
    tab = True
