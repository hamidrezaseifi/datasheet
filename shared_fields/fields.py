# shared_fields/fields.py
from django import forms
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from django.db import models

# only_letters_validator = RegexValidator(
#     regex=r'^[a-zA-ZäöüÄÖÜß\s-]+$',
#     message=_("Nur Buchstaben, Umlaute, Bindestriche und Leerzeichen erlaubt.")
# )
#
# email_validator = RegexValidator(
#     regex=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
#     message=_("Bitte gib eine gültige E-Mail-Adresse ein.")
# )
#
# month_choices = [
#     (1, 'Januar'),
#     (2, 'Februar'),
#     (3, 'März'),
#     (4, 'April'),
#     (5, 'Mai'),
#     (6, 'Juni'),
#     (7, 'Juli'),
#     (8, 'August'),
#     (9, 'September'),
#     (10, 'Oktober'),
#     (11, 'November'),
#     (12, 'Dezember'),
# ]
#
#
# def get_month_name(m_id) -> str:
#     res = [m for m in month_choices if m[0] == m_id]
#     if len(res) > 0:
#         return res[0][1]
#
#     return 'Not-Found!'

#
# class NameField(forms.CharField):
#     def __init__(self, *args, **kwargs):
#         kwargs.setdefault('label', _('Name'))
#         kwargs.setdefault('max_length', 100)
#         kwargs.setdefault('validators', [only_letters_validator])
#         kwargs.setdefault('widget', forms.TextInput(attrs={
#             'placeholder': _('Enter name'),
#             'class': 'form-control'
#         }))
#         super().__init__(*args, **kwargs)
#
#
# class EmailField(forms.EmailField):
#     def __init__(self, *args, **kwargs):
#         kwargs.setdefault('label', _('Email'))
#         kwargs.setdefault('validators', [email_validator])
#         kwargs.setdefault('widget', forms.EmailInput(attrs={
#             'placeholder': _('Enter your email'),
#             'class': 'form-control'
#         }))
#         super().__init__(*args, **kwargs)
#
#
# class DateField(forms.DateField):
#     def __init__(self, *args, **kwargs):
#         kwargs.setdefault('label', _('Date'))
#         kwargs.setdefault('widget', forms.DateInput(attrs={
#             'type': 'date',
#             'class': 'form-control'
#         }))
#         super().__init__(*args, **kwargs)
#
#
# class TextInputField(forms.CharField):
#     def __init__(self, *args, **kwargs):
#         kwargs.setdefault('label', _('Text'))
#         kwargs.setdefault('widget', forms.TextInput(attrs={
#             'placeholder': _('Enter text'),
#             'class': 'form-control'
#         }))
#         super().__init__(*args, **kwargs)
#
#
# class MessageField(forms.CharField):
#     def __init__(self, *args, **kwargs):
#         kwargs.setdefault('label', _('Message'))
#         kwargs.setdefault('widget', forms.Textarea(attrs={
#             'placeholder': _('Enter your message'),
#             'class': 'form-control',
#             'rows': 4
#         }))
#         super().__init__(*args, **kwargs)
#
#
# class YearField(forms.IntegerField):
#     def __init__(self, *args, **kwargs):
#         kwargs.setdefault('label', _('Year'))
#         kwargs.setdefault('validators', [
#             MinValueValidator(1900),
#             MaxValueValidator(2100)
#         ])
#         kwargs.setdefault('widget', forms.NumberInput(attrs={
#             'placeholder': _('Enter year'),
#             'class': 'form-control'
#         }))
#         super().__init__(*args, **kwargs)
#
#
# class BetragField(forms.DecimalField):
#     def __init__(self, *args, **kwargs):
#         kwargs.setdefault('label', _('Amount'))
#         kwargs.setdefault('max_digits', 10)
#         kwargs.setdefault('decimal_places', 2)
#         kwargs.setdefault('validators', [MinValueValidator(0)])
#         kwargs.setdefault('widget', forms.NumberInput(attrs={
#             'placeholder': _('Enter amount'),
#             'class': 'form-control',
#             'step': '0.01'
#         }))
#         super().__init__(*args, **kwargs)
#
#
# class SapNrField(forms.IntegerField):
#     def __init__(self, *args, **kwargs):
#         kwargs.setdefault('label', _('SAP Number'))
#         kwargs.setdefault('validators', [MinValueValidator(1)])
#         kwargs.setdefault('required', True)
#         kwargs.setdefault('widget', forms.NumberInput(attrs={
#             'placeholder': _('Enter SAP number'),
#             'class': 'form-control'
#         }))
#         super().__init__(*args, **kwargs)
#
#
# class ObjektNameField(forms.CharField):
#     def __init__(self, *args, **kwargs):
#         kwargs.setdefault('label', _('Object Name'))
#         kwargs.setdefault('max_length', 255)
#         kwargs.setdefault('required', False)
#         kwargs.setdefault('widget', forms.TextInput(attrs={
#             'placeholder': _('Enter object name'),
#             'class': 'form-control'
#         }))
#         super().__init__(*args, **kwargs)
#
#
# class MountChoices(models.TextChoices):
#     EUROPE = 'EUROPE', 'EUROPE'
#     AFRICA = 'AFRICA', 'AFRICA'
#     SOUTH_AMERICA = 'SOUTH AMERICA', 'SOUTH AMERICA'
#     NORTH_AMERICA = 'NORTH AMERICA', 'NORTH AMERICA'
#     OCEANIA = 'OCEANIA', 'OCEANIA'
#     ASIA = 'ASIA', 'ASIA'
#
#
# class MonatField(forms.IntegerField):
#     def __init__(self, *args, **kwargs):
#         kwargs.setdefault('label', _('month'))
#         kwargs.setdefault('validators', [
#             MinValueValidator(1),
#             MaxValueValidator(12)
#         ])
#         kwargs.setdefault('required', True)
#         # definiere die auswahlmöglichkeiten für die monate (1 bis 12)
#
#         kwargs.setdefault('widget', forms.Select(
#             attrs={
#                 'class': 'form-control'
#             },
#             choices=month_choices
#         ))
#         super().__init__(*args, **kwargs)
#
#
# class UmsatzArtField(forms.CharField):
#     def __init__(self, *args, **kwargs):
#         kwargs.setdefault('label', _('Revenue Type'))
#         kwargs.setdefault('max_length', 255)
#         kwargs.setdefault('required', False)
#         kwargs.setdefault('widget', forms.TextInput(attrs={
#             'placeholder': _('Enter revenue type'),
#             'class': 'form-control'
#         }))
#         super().__init__(*args, **kwargs)
#
#
# class PlanField(forms.IntegerField):
#     def __init__(self, *args, **kwargs):
#         kwargs.setdefault('label', _('Plan'))
#         kwargs.setdefault('validators', [MinValueValidator(0)])
#         kwargs.setdefault('required', True)
#         kwargs.setdefault('widget', forms.NumberInput(attrs={
#             'placeholder': _('Enter plan amount'),
#             'class': 'form-control'
#         }))
#         super().__init__(*args, **kwargs)
