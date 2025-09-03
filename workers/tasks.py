import datetime
from django.utils.translation import gettext_lazy as _
from organizations.choices import Roles, Statuses
from organizations.models import Organization, WorkerToOrganization
from organizations.validators import inn_check_api_validator
from .ftp import get_workers
from .constants import DEFAULT_DOC_TYPES
from .models import Worker, WorkerDoc


def update_workers_from_onec():
    fio = 'ФИО'
    passport = 'Серия, номер паспорта'
    inn = 'ИНН подразделения'
    org_name = 'подразделение'
    workers_data = get_workers()
    passports = []
    for row in workers_data:
        worker_fio = row.get(fio, "")
        worker_passport: str = row.get(passport)
        worker, _ = Worker.objects.get_or_create(passport=worker_passport, defaults={
            'fio': worker_fio
        })
        for doc in DEFAULT_DOC_TYPES:
            value = row.get(doc["name"])
            WorkerDoc.objects.update_or_create(
                {
                    "expired_date": datetime.datetime.strptime(value, "%d.%m.%Y") if value else None
                }, worker=worker, type_id=doc['slug']
            )
        worker_inn = row.get(inn)
        if not Organization.objects.filter(inn=worker_inn).exists():
            try:
                org_data = inn_check_api_validator(worker_inn)
            except Exception:
                org_data = {
                    "c": row.get(org_name, worker_inn),
                }
            worker_org = Organization.objects.create(
                inn=worker_inn,
                address = org_data.get('a'),
                name = org_data.get('c') if org_data.get('c') else row.get(org_name, worker_inn),
                ogrn = org_data.get('o'),
                kpp = org_data.get('p'),
            )
        else:
            worker_org = Organization.objects.get(inn=worker_inn)
        WorkerToOrganization.objects.get_or_create(
            {
                "status": Statuses.DONE,
                "role": Roles.WORKER,
            }, org=worker_org, worker=worker
        )
        passports.append(worker.passport)
    # User.objects.exclude(Q(passport__in=passports) | Q(is_superuser=True) | Q(usertoorganization__role__in=[ROLE_OWNER, ROLE_CLIENT]) | Q(type=USER_TYPE_CANDIDATE)).delete()