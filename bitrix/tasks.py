from celery import shared_task

from .api import get_contact


@shared_task
def update_contact(contact_id):
    contact = get_contact(contact_id)
    