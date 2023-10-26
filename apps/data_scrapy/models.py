from django.db import models
from django.utils.translation import gettext_lazy as _

from helpers.base_models import BaseModelTimestamp


class ScrapyQuotesModel(BaseModelTimestamp):
    title = models.CharField(verbose_name=_("Título"), max_length=150, null=True, blank=True)
    author = models.CharField(verbose_name=_("Autor"), max_length=150, null=True, blank=True)
    tags = models.CharField(verbose_name=_("Autor"), max_length=1000, null=True, blank=True)
    description = models.TextField(verbose_name=_("Descrição"), null=True, blank=True)
    
    def __str__(self) -> str:
        return self.title if self.title else str(self.id)
    
    class Meta:
        verbose_name = _("Scrapy Quotes")
        verbose_name_plural = _("Scrapy Quotes")