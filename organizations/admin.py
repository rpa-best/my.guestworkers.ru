from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Organization, DocumentType, WorkerToOrganization
from .forms import OrganizationCreateForm
from .inlines import *


@admin.register(Organization)
class OrganizationAdmin(ModelAdmin):
    list_display = ['inn', 'name']
    search_fields = ['inn', 'name']
    inlines = [
        WorkerToOrganizationInline,
        OrganizationDocInline, 
        OrganizationTabelInline, 
        DocumentInline
    ]

    def get_form(self, request, obj = None, change = False, **kwargs):
        if not obj:
            kwargs.update(form=OrganizationCreateForm)
        return super().get_form(request, obj, change, **kwargs)


@admin.register(DocumentType)
class DocumentTypeAdmin(ModelAdmin):
    list_display = ['name']