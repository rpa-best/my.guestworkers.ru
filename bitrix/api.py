import os
import requests
from dataclasses import dataclass
from typing import Optional, List
from .logger import logger

BITRIX_WEBHOOK_URL = os.getenv('BITRIX_WEBHOOK_URL')  # "https://your-domain.bitrix24.ru/rest/1/xxxxxxxx/" ваш входящий вебхук


@dataclass
class ContactField:
    ID: Optional[str] = None
    VALUE_TYPE: Optional[str] = None
    VALUE: Optional[str] = None
    TYPE_ID: Optional[str] = None


@dataclass
class Contact:
    ID: Optional[str] = None
    POST: Optional[str] = None
    COMMENTS: Optional[str] = None
    HONORIFIC: Optional[str] = None
    NAME: Optional[str] = None
    SECOND_NAME: Optional[str] = None
    LAST_NAME: Optional[str] = None
    PHOTO: Optional[str] = None
    LEAD_ID: Optional[str] = None
    TYPE_ID: Optional[str] = None
    SOURCE_ID: Optional[str] = None
    SOURCE_DESCRIPTION: Optional[str] = None
    COMPANY_ID: Optional[str] = None
    BIRTHDATE: Optional[str] = None
    EXPORT: Optional[str] = None
    HAS_PHONE: Optional[str] = None # Y/N
    HAS_EMAIL: Optional[str] = None # Y/N
    HAS_IMOL: Optional[str] = None # Y/N
    DATE_CREATE: Optional[str] = None
    DATE_MODIFY: Optional[str] = None
    ASSIGNED_BY_ID: Optional[str] = None
    CREATED_BY_ID: Optional[str] = None
    MODIFY_BY_ID: Optional[str] = None
    OPENED: Optional[str] = None
    ORIGINATOR_ID: Optional[str] = None
    ORIGIN_ID: Optional[str] = None
    ORIGIN_VERSION: Optional[str] = None
    FACE_ID: Optional[str] = None
    LAST_ACTIVITY_TIME: Optional[str] = None
    ADDRESS: Optional[str] = None
    ADDRESS_2: Optional[str] = None
    ADDRESS_CITY: Optional[str] = None
    ADDRESS_POSTAL_CODE: Optional[str] = None
    ADDRESS_REGION: Optional[str] = None
    ADDRESS_PROVINCE: Optional[str] = None
    ADDRESS_COUNTRY: Optional[str] = None
    ADDRESS_LOC_ADDR_ID: Optional[str] = None
    UTM_SOURCE: Optional[str] = None
    UTM_MEDIUM: Optional[str] = None
    UTM_CAMPAIGN: Optional[str] = None
    UTM_CONTENT: Optional[str] = None
    UTM_TERM: Optional[str] = None
    PARENT_ID_1224: Optional[str] = None
    LAST_ACTIVITY_BY: Optional[str] = None
    UF_CRM_1720697698689: Optional[str] = None

    PHONE: Optional[List[ContactField]] = None
    EMAIL: Optional[List[ContactField]] = None


def get_contact(contact_id: int):
    url = f"{BITRIX_WEBHOOK_URL}crm.contact.get"
    resp = requests.post(url, json={"id": contact_id})
    data = resp.json()
    logger.debug(f'Rest Response: {data}')
    return Contact(**data.get('result', {}))