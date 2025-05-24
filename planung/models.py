from django.db import models


class PlanungData(models.Model):
    sap_nr = models.BigIntegerField()
    id2 = models.BigIntegerField()
    objekt_name = models.CharField(max_length=255, null=True, blank=True)
    jahr = models.IntegerField()
    monat = models.IntegerField()
    umsatz_art = models.CharField(max_length=255, null=True, blank=True)
    plan = models.IntegerField()

    def __str__(self):
        return f"{self.objekt_name} ({self.sap_nr})"

    class Meta:
        db_table = 'planung'
