from django.db import models
from .api import Api


class WorkerInvoice(models.Model):
    id = models.BigIntegerField(primary_key=True)
    worker = models.ForeignKey('oauth.User', models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def data(self):
        api = Api()
        response = api.get_order(self.id)
        if not response.ok:
            return {"id": self.id, "error": response.text}
        return response.json()
