from django.db import models
from django.utils.translation import gettext_lazy as _

from helpers.base_models import BaseModelTimestamp


class NotificationsModel(BaseModelTimestamp):
    title = models.CharField(verbose_name=_("Título"), max_length=150, null=True, blank=True)
    description = models.TextField(verbose_name=_("Descrição"), null=True, blank=True)
    
    def __str__(self) -> str:
        return self.title if self.title else str(self.id)
    
    class Meta:
        verbose_name = _("Notificação")
        verbose_name_plural = _("Notificações")