from __future__ import unicode_literals
from django.db import models


class DomainList(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField(null=True, blank=True)
    advertiser = models.ForeignKey("rtb.Advertiser", null=True, blank=True, db_constraint=False, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = "domain_list"

