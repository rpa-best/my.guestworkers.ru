from django import forms
from unfold.widgets import UnfoldAdminSelect2Widget
from unfold.contrib.import_export.forms import ImportForm
from import_export.forms import ConfirmImportForm
from organizations.models import Organization


class WorkerImportForm(ImportForm):
    org = forms.ModelChoiceField(
        label='Компания',
        queryset=Organization.objects,
        widget=UnfoldAdminSelect2Widget()
    )


class WorkerConfirmImportForm(ConfirmImportForm):
    org = forms.ModelChoiceField(
        label='Компания',
        queryset=Organization.objects,
        widget=UnfoldAdminSelect2Widget()
    )
