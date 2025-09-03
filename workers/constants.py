from datetime import timedelta
SOON_EXPIRE_LIMIT = timedelta(days=5)
UPLOAD_KWARGS_PASSPORT = 'Серия, номер паспорта'
UPLOAD_KWARGS = (
    ('first_name', 'ФИО', 'Пётр Петров Петрович'),
    ('passport', UPLOAD_KWARGS_PASSPORT, "99 99 999999"),
)
DEFAULT_DOC_TYPES = [
    {'slug': 'chek_do', 'name': 'Чек до'},
    {'slug': 'polis_oms_do', 'name': 'Полис ОМС до'},
    {'slug': 'polis_dms_do', 'name': 'Полис ДМС до'},
    {'slug': 'projivanie_do', 'name': 'Разрешение на временное проживание до'},
    {'slug': 'jitelstvo_o', 'name': 'Вид на жительство до'},
    {'slug': 'potent_do', 'name': 'патент до'},
]
DOC_STATUS_NORM = "norm"
DOC_STATUS_EXPIRED = "expired"
DOC_STATUS_SOON_EXPIRED = "soon_expired"
DOC_STATUS = (
    (DOC_STATUS_EXPIRED, DOC_STATUS_EXPIRED),
    (DOC_STATUS_SOON_EXPIRED, DOC_STATUS_SOON_EXPIRED),
    (DOC_STATUS_NORM, DOC_STATUS_NORM),
)