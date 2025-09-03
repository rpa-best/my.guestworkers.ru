import datetime
from dateutil import parser
from import_export.resources import ModelResource
from import_export.fields import Field
from .constants import DEFAULT_DOC_TYPES
from .models import Worker, WorkerDoc, DocType


class WorkerResource(ModelResource):
    fio = Field(
        attribute='fio',
        column_name='ФИО',
    )
    passport = Field(
        attribute='passport',
        column_name='Серия, номер паспорта',
    )
    class Meta:
        model = Worker
        exclude = ['id']
        import_id_fields = ['passport']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for doc_type in DEFAULT_DOC_TYPES:
            self.fields[doc_type['slug']] = Field(
                attribute=doc_type['slug'],
                column_name=doc_type['name'],
            )

    def export_field(self, field: Field, instance, **kwargs):
        if field.attribute in ['fio', 'passport']:
            return super().export_field(field, instance, **kwargs)

        doc = WorkerDoc.objects.filter(worker=instance, type_id=field.attribute).first()
        if doc:
            return doc.expired_date
        return super().export_field(field, instance, **kwargs)

    def import_field(self, field: Field, instance, row, **kwargs):
        if field.attribute in ['fio', 'passport']:
            return super().import_field(field, instance, row, **kwargs)
        DocType.objects.get_or_create(slug=field.attribute, name=field.column_name)
        doc = WorkerDoc.objects.filter(worker=instance, type_id=field.attribute).first()

        if doc:
            value = row[field.column_name]
            value = parser.parse(value, dayfirst=True) if isinstance(value, str) else value
            doc.expired_date = value
            doc.save()
        return super().import_field(field, instance, row, **kwargs)
