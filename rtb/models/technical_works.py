from django.db import models

class TechnicalWork(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.TextField(null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "technical_work"

class AttentionMessage(models.Model):
    id = models.AutoField(primary_key=True)
    message = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=False)

    class Meta:
        db_table = "attention_message"
