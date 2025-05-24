# shared_fields/forms.py
from .fields import NameField, EmailField, YearField, BetragField, SapNrField, ObjektNameField, MonatField, \
    UmsatzArtField, PlanField
from django import forms

#
# class BaseUserForm(forms.Form):
#     name = NameField()
#     email = EmailField()
#
#
# # class BaseFinancialForm(forms.Form):
# #     betrag = BetragField()
# #     year = YearField()
#
#
# class BasePlanungForm(forms.Form):
#     sap_nr = SapNrField()
#     objekt_name = ObjektNameField()
#     jahr = YearField()
#     monat = MonatField()
#     umsatz_art = UmsatzArtField()
#     plan = PlanField()
