from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.http.response import HttpResponse
from unfold.admin import ModelAdmin
from unfold.decorators import action
from unfold.enums import ActionVariant
from organizations.filters import WorkerOrganizationFilter
from .api import Api
from .models import WorkerInvoice
from .forms import WorkerInvoiceCreateForm, WorkerInvoiceReadOnlyForm


@admin.register(WorkerInvoice)
class WorkerInvoiceAdmin(ModelAdmin):
    form = WorkerInvoiceCreateForm
    list_display = ['id', 'worker', 'created_at']
    actions_row = ['download']
    actions_detail = ['download']
    list_filter = [WorkerOrganizationFilter]
    list_filter_submit = True
    list_filter_sheet = False

    def get_form(self, request, obj, *args, **kwargs):
        kwargs['form'] = WorkerInvoiceCreateForm if not obj else WorkerInvoiceReadOnlyForm
        return super().get_form(request, obj, *args, **kwargs)
    
    def get_exclude(self, request, obj=None, *args, **kwargs):
        if obj:
            return ['worker']
        return super().get_exclude(request, obj, *args, **kwargs)
    
    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        if object_id:
            extra_context = extra_context or {}
            extra_context["show_save"] = False
            extra_context["show_save_and_continue"] = False
            extra_context["show_save_and_add_another"] = False
        return super().changeform_view(request, object_id, form_url, extra_context)

    @action(
        description='Скачать направление',
        url_path='download',
        icon='download',
        variant=ActionVariant.SUCCESS
    )
    def download(self, request, object_id):
        response = Api().get_direction_order(object_id)
        if not response.ok: 
            self.message_user(request, f"Произошла ошибка при скачивании: {response.text}", level=40)
            return redirect(
                reverse_lazy('admin:mprofid_workerinvoice_change', args=[object_id])
            )
        pdf_bytes = response.content
        response = HttpResponse(
            pdf_bytes,
            content_type='application/pdf'
        )
        response['Content-Disposition'] = f'attachment; filename="report-{object_id}.pdf"'
        return response
    
