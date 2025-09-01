import os
from django.http.response import JsonResponse
from django.http.request import HttpRequest
from .logger import logger
from .tasks import update_contact


def bitrix_webhook(request: HttpRequest, *args, **kwargs):
    token = request.POST.get("auth", {}).get("application_token")
    if token != os.getenv("BITRIX_TOKEN"):
        return JsonResponse({'status': 'error'}) 
    logger.debug(str(f'Request data: {request.POST}'))
    event = request.POST.get('event')
    contact_id = request.POST.get("data", {}).get("FIELDS", {}).get("ID")
    if event == 'ONCRMCONTACTUPDATE' and contact_id:
        logger.info(f"Контакт {contact_id} был обновлён")
        update_contact.delay(contact_id)
    return JsonResponse({'status': 'ok'})
