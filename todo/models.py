from django.db import models
from companies.models import Company


class Todo(models.Model):
    description = models.TextField(max_length=140)
    completed = models.BooleanField(default=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE,
                                related_name='todos')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('completed', '-date_updated')