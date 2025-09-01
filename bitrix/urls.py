from django.urls import path
from .views import bitrix_webhook


urlpatterns = [
    path("webhook/", bitrix_webhook, name="bitrix_webhook"),
]