from unfold.admin import TabularInline
from .models import WorkerToOrganization, OrganizationDoc, OrganizationTabel, Document

class WorkerToOrganizationInline(TabularInline):
    model = WorkerToOrganization
    extra = 0
    tab = True
    autocomplete_fields = ['worker']


class OrganizationDocInline(TabularInline):
    model = OrganizationDoc
    extra = 0
    tab = True
    readonly_fields = ['user']

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)


class OrganizationTabelInline(TabularInline):
    model = OrganizationTabel
    extra = 0
    tab = True
    exclude = ['editable']


class DocumentInline(TabularInline):
    model = Document
    extra = 0
    tab = True
