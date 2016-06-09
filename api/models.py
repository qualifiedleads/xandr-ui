import datetime

from django.db import models


class NetworkAnalyticsRaw(models.Model):
    json = models.TextField(null=True, blank=True)
    csv = models.TextField(null=True, blank=True)
    report_type = models.CharField(max_length=50, null=True, blank=True)
    report_id = models.CharField(max_length=100, null=True, blank=True)
    last_updated = models.DateTimeField(default=datetime.datetime.now)

    class Meta:
        db_table="NetworkAnalyticsRaw"

    def __unicode__(self):
        return self.id
