from datetime import datetime

from django import forms
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

#from shared_fields.fields import SapNrField, ObjektNameField, YearField, MonatField, UmsatzArtField, PlanField
from .models import PlanungData


month_choices = [
        (1, _('Januar')),
        (2, _('Februar')),
        (3, _('März')),
        (4, _('April')),
        (5, _('Mai')),
        (6, _('Juni')),
        (7, _('Juli')),
        (8, _('August')),
        (9, _('September')),
        (10, _('Oktober')),
        (11, _('November')),
        (12, _('Dezember')),
    ]


def get_month_name(m_id) -> str:
    res = [m for m in month_choices if m[0] == m_id]
    if len(res) > 0:
        # Konvertiere den übersetzten String in einen normalen String
        return str(res[0][1])
    return 'Not-Found!'


class PlanungForm(forms.ModelForm):
    # Validator für sap_nr: Nur Zahlen (angenommen, SAP-Nummer ist numerisch)
    sap_nr_validator = RegexValidator(
        regex=r'^\d+$',
        message=_('Nur Zahlen sind erlaubt.')
    )
    id2_validator = RegexValidator(
        regex=r'^\d+$',
        message=_('Nur Zahlen sind erlaubt.')
    )

    # Validator für objekt_name: Buchstaben, Umlaute, Bindestriche, Leerzeichen
    objekt_name_validator = RegexValidator(
        regex=r'^[a-zA-ZäöüÄÖÜß\s-]+$',
        message=_('Nur Buchstaben, Umlaute, Bindestriche und Leerzeichen erlaubt.')
    )

    # Validator für umsatz_art: Buchstaben, Umlaute, Bindestriche, Leerzeichen (anpassbar)
    umsatz_art_validator = RegexValidator(
        regex=r'^[a-zA-ZäöüÄÖÜß\s-]+$',
        message=_('Nur Buchstaben, Umlaute, Bindestriche und Leerzeichen erlaubt.')
    )

    class Meta:
        model = PlanungData
        fields = ['sap_nr', 'id2', 'objekt_name', 'jahr', 'monat', 'umsatz_art', 'plan']
        labels = {
            'sap_nr': _('SAP-Nummer'),
            'id2': _('Second-ID'),
            'objekt_name': _('Objektname'),
            'jahr': _('Jahr'),
            'monat': _('Monat'),
            'umsatz_art': _('Umsatzart'),
            'plan': _('Plan'),
        }
        widgets = {
            'sap_nr': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': _('SAP-Nummer eingeben'),
                'pattern': '\\d+',
                'title': _('Nur Zahlen sind erlaubt.'),
                'required': True,
            }),
            'id2': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': _('Second id'),
                'pattern': '\\d+',
                'title': _('Nur Zahlen sind erlaubt.'),
                'required': True,
            }),
            'objekt_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Objektname eingeben'),
                'pattern': '[a-zA-ZäöüÄÖÜß\\s-]+',
                'title': _('Nur Buchstaben, Umlaute, Bindestriche und Leerzeichen erlaubt.'),
                'required': False,
            }),
            'jahr': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': _('Jahr eingeben'),
                'min': 1900,
                'max': datetime.now().year,  # Bis aktuelles Jahr (2025)
                'title': _('Jahr muss zwischen 1900 und dem aktuellen Jahr liegen.'),
                'required': True,
            }),
            # 'monat': forms.NumberInput(attrs={
            #     'class': 'form-control',
            #     'placeholder': _('Monat eingeben'),
            #     'min': 1,
            #     'max': 12,
            #     'title': _('Monat muss zwischen 1 und 12 liegen.'),
            #     'required': True,
            # }),
            'monat': forms.Select(choices=month_choices, attrs={
                'class': 'form-control',
                'title': _('Wählen Sie einen Monat aus.'),
                'required': True,
            }),
            'umsatz_art': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Umsatzart eingeben'),
                'pattern': '[a-zA-ZäöüÄÖÜß\\s-]+',
                'title': _('Nur Buchstaben, Umlaute, Bindestriche und Leerzeichen erlaubt.'),
                'required': True,
            }),
            'plan': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': _('Plan eingeben'),
                'step': '0.01',  # Erlaubt Gleitkommazahlen
                'title': _('Nur Zahlen oder Gleitkommazahlen sind erlaubt.'),
                'required': True,
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Füge Validatoren hinzu
        self.fields['sap_nr'].validators.append(self.sap_nr_validator)
        self.fields['id2'].validators.append(self.id2_validator)
        self.fields['objekt_name'].validators.append(self.objekt_name_validator)
        self.fields['umsatz_art'].validators.append(self.umsatz_art_validator)
        print(f"PlanungForm fields: {self.fields.keys()}")

    # Monatsauswahl für das Dropdown


    def clean_sap_nr(self):
        sap_nr = self.cleaned_data.get('sap_nr')
        if sap_nr and not str(sap_nr).isdigit():
            raise forms.ValidationError(_('SAP-Nummer muss eine positive Zahl sein.'))
        return sap_nr

    def clean_id2(self):
        id2 = self.cleaned_data.get('id2')
        if id2 and not str(id2).isdigit():
            raise forms.ValidationError(_('id2 muss eine positive Zahl sein.'))
        return id2

    def clean_objekt_name(self):
        objekt_name = self.cleaned_data.get('objekt_name')
        if objekt_name and not objekt_name.strip():
            raise forms.ValidationError(_('Objektname darf nicht nur aus Leerzeichen oder Bindestrichen bestehen.'))
        return objekt_name

    def clean_jahr(self):
        jahr = self.cleaned_data.get('jahr')
        current_year = datetime.now().year
        if jahr and (jahr < 1900 or jahr > current_year):
            raise forms.ValidationError(_(f'Jahr muss zwischen 1900 und {current_year} liegen.'))
        return jahr

    def clean_monat(self):
        monat = self.cleaned_data.get('monat')
        if monat and (monat < 1 or monat > 12):
            raise forms.ValidationError(_('Monat muss zwischen 1 und 12 liegen.'))
        return monat

    def clean_umsatz_art(self):
        umsatz_art = self.cleaned_data.get('umsatz_art')
        if umsatz_art and not umsatz_art.strip():
            raise forms.ValidationError(_('Umsatzart darf nicht nur aus Leerzeichen oder Bindestrichen bestehen.'))
        return umsatz_art

    def clean_plan(self):
        plan = self.cleaned_data.get('plan')
        if plan is not None and plan < 0:
            raise forms.ValidationError(_('Plan darf nicht negativ sein.'))
        return plan

    # def get_month_name(m_id) -> str:
    # res = [m for m in month_choices if m[0] == m_id]
    # if len(res) > 0:
    #     return res[0][1]
    #
    # return 'Not-Found!'

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     base_form = BasePlanungForm()
    #     for field_name in self.fields:
    #         if field_name in base_form.fields:
    #             # feld aus baseplanungform übernehmen (für validierungen, widgets, etc.)
    #             self.fields[field_name] = base_form.fields[field_name]
    #             # label aus Meta.labels verwenden, falls vorhanden
    #             if field_name in self.Meta.labels:
    #                 self.fields[field_name].label = self.Meta.labels[field_name]
    #             else:
    #                 # fallback: label aus baseplanungform in kleinbuchstaben
    #                 self.fields[field_name].label = base_form.fields[field_name].label.lower()
