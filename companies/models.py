from django.db import models
from django.utils.translation import ugettext_lazy as _


class Company(models.Model):
    name = models.CharField(max_length=40)

    class Meta:
        verbose_name = _('company')
        verbose_name_plural = _('companies')
        ordering = ('name',)

    def __str__(self):
        return self.name
