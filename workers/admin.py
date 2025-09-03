from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from unfold.admin import ModelAdmin
from unfold.decorators import action
from unfold.enums import ActionVariant
from unfold.contrib.import_export.forms import ExportForm
from import_export.admin import ImportExportMixin

from organizations.filters import OrganizationFilter

from .forms import WorkerImportForm, WorkerConfirmImportForm
from .resources import WorkerResource
from .models import Worker, DocType
from .tasks import update_workers_from_onec
from .inlines import * 


@admin.register(Worker) 
class WorkerAdmin(ImportExportMixin, ModelAdmin):
    actions_list = ['update_from_1c']
    search_fields = ['passport', 'fio']
    list_display = ['fio', 'passport']
    inlines = [WorkerDocInline]
    list_filter = [
        OrganizationFilter,
    ]
    list_filter_submit = True
    list_filter_sheet = False
    resource_classes = [WorkerResource]
    export_form_class = ExportForm
    import_form_class = WorkerImportForm
    confirm_form_class = WorkerConfirmImportForm

    def has_add_permission(self, request):
        return False
    
    def get_confirm_form_initial(self, request, import_form):
        initial = super().get_confirm_form_initial(request, import_form)
        initial['org'] = request.POST.get('org')
        return initial

    @action(
        permissions=['update_from_1c'],
        description='Обновить данные компаний из 1С',
        url_path='update_from_1c',
        icon='sync',
        variant=ActionVariant.SUCCESS
    )
    def update_from_1c(self, request):
        try:
            update_workers_from_onec()
            self.message_user(request, "Данные обновлены", level=20)
        except Exception as e:
            self.message_user(request, f"Произошла ошибка при обновлении: {e}", level=40)
        return redirect(
          reverse_lazy("admin:workers_worker_changelist")
        ) 
    
    def has_update_from_1c_permission(self, request, *args, **kwargs):
        return request.user.has_perm('workers.add_worker')


@admin.register(DocType)
class DocTypeAdmin(ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name', 'slug']