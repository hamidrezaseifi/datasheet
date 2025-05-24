# sales_prognosen_matrix/models.py (assumed)
from django.db import models
from django.utils.translation import gettext_lazy as _


class SalesObjektData(models.Model):
    objekt = models.CharField(max_length=255)
    sort_order = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sort_order} - {self.objekt}"

    class Meta:
        db_table = 'sales_objekt'
        managed = False


class SalesPrognoseData(models.Model):
    id = models.BigAutoField(primary_key=True)
    objekt = models.ForeignKey(SalesObjektData, on_delete=models.CASCADE, related_name="sales_data")
    sortierreihen_folge = models.ForeignKey(SalesObjektData, on_delete=models.CASCADE, related_name="sales_data_sort")
    jahr = models.IntegerField()
    monat = models.IntegerField()
    datum = models.DateField()
    prognose = models.FloatField(default=0.0)
    created_at = models.DateField(auto_now_add=True, verbose_name=_("Erstellt am"))

    def __str__(self):
        return f"{self.objekt} ({self.datum}): {self.prognose}"

    class Meta:
        db_table = 'sales_prognose'
        # Django hat kein einfluss in db
        managed = False
