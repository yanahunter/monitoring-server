from django.contrib.postgres.fields import ArrayField
from django.db import models


class Report(models.Model):
    computer_id = models.UUIDField(blank=False, null=False)
    date = models.DateTimeField(auto_now=False, auto_now_add=False, blank=False, null=False)
    cpu_percent = models.FloatField(blank=True, null=True)
    free_ram = models.BigIntegerField(blank=True, null=True)
    free_disk_space = models.BigIntegerField(blank=True, null=True)
    processes_count = models.BigIntegerField(blank=True, null=True)
    users_list = ArrayField(
        models.CharField(max_length=64, blank=False, null=False),
        null=True,
        blank=True
    )
