import requests
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class INNCheckValidator:
    """
        org.address = org['a']
        org.name = org['c']
        org.ogrn = org['o']
        org.kpp = org['p']
    """
    _base_url = 'https://egrul.nalog.ru'

    def _get_token(self, value):
        response = requests.post(self._base_url, json={
            "query": value
        })
        if not response.status_code == 200:
            raise ValidationError(_('Сервис недоступен'))
        return response.json().get('t')

    def __call__(self, value, return_list=False):
        token = self._get_token(value)
        response = requests.get(f"{self._base_url}/search-result/{token}")
        if not response.status_code == 200:
            raise ValidationError(_('Сервис недоступен'))
        orgs = response.json().get('rows')
        if not orgs:
            raise ValidationError(_("ИНН не найдень"))
        if len(orgs) > 1 and not return_list:
            raise ValidationError(_("Найден {count} организации с указинной инн".format(count=len(orgs))))
        return orgs[0] if not return_list else orgs


def inn_check_api_validator(value, return_list=False):
    validator = INNCheckValidator()
    try:
        return validator(value, return_list=return_list)
    except ValidationError as _exp:
        raise ValidationError(_exp.messages, getattr(_exp, 'code', None))