# sales_prognosen_matrix/forms.py
from django import forms
from django.core.validators import RegexValidator
from datetime import datetime
from .models import SalesObjektData, SalesPrognoseData
from django.utils.translation import gettext_lazy as _
#from .models_sqlalchemy import SalesPrognose, engine


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


class SalesObjektForm(forms.ModelForm):
    objekt_validator = RegexValidator(
        regex=r'^[a-zA-ZäöüÄÖÜß\s-]+$',
        message=_('Nur Buchstaben, Umlaute, Bindestriche und Leerzeichen erlaubt.')
    )

    class Meta:
        model = SalesObjektData
        fields = ['sort_order', 'objekt']
        labels = {
            'sort_order': _('Sortierreihenfolge'),
            'objekt': _('Objekt'),
        }
        widgets = {
            'sort_order': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': _('Sortierreihenfolge eingeben'),
                'pattern': '\\d+',
                'title': _('Nur Zahlen sind erlaubt.'),
                'required': True,
            }),
            'objekt': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Objektname eingeben'),
                'pattern': '[a-zA-ZäöüÄÖÜß\\s-]+',
                'title': _('Nur Buchstaben, Umlaute, Bindestriche und Leerzeichen erlaubt.'),
                'required': True,
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['objekt'].validators.append(self.objekt_validator)

    def clean_sort_order(self):
        sort_order = self.cleaned_data['sort_order']
        if sort_order < 0:
            raise forms.ValidationError(_("Sortierreihenfolge darf nicht negativ sein."))
        return sort_order

    def clean_objekt(self):
        objekt = self.cleaned_data['objekt']
        if objekt and not objekt.strip():
            raise forms.ValidationError(_('Objekt darf nicht nur aus Leerzeichen oder Bindestrichen bestehen.'))
        return objekt


class SalesPrognoseForm(forms.ModelForm):
    prognose_validator = RegexValidator(
        regex=r'^\d+(\.\d{1,2})?$',
        message=_('Nur Zahlen oder Gleitkommazahlen mit bis zu 2 Dezimalstellen sind erlaubt.')
    )

    jahr = forms.IntegerField(
        required=True,
    )
    monat = forms.ChoiceField(
        choices=month_choices,
        required=True,
    )

    class Meta:
        model = SalesPrognoseData
        fields = ['id', 'objekt', 'sortierreihen_folge', 'jahr', 'monat', 'datum', 'prognose']
        labels = {
            'id': _('Id'),
            'objekt': _('Objekt'),
            'sortierreihen_folge': _('Sortierreihenfolge'),
            'jahr': _('Jahr'),
            'monat': _('Monat'),
            'prognose': _('Prognose'),
        }
        widgets = {
            'id': forms.HiddenInput(),
            'objekt': forms.Select(attrs={
                'class': 'form-control',
                'required': True,
            }),
            'sortierreihen_folge': forms.Select(attrs={
                'class': 'form-control',
                'required': True,
            }),
            'jahr': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': _('Jahr eingeben'),
                'min': 1900,
                'max': datetime.now().year,
                'title': _('Jahr muss zwischen 1900 und dem aktuellen Jahr liegen.'),
                'required': True,
            }),
            'monat': forms.Select(attrs={
                'class': 'form-control',
                'title': _('Wählen Sie einen Monat aus.'),
                'required': True,
            }),
            'datum': forms.HiddenInput(),
            'prognose': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': _('Prognose eingeben'),
                'step': '0.01',
                'title': _('Nur Zahlen oder Gleitkommazahlen sind erlaubt.'),
                'required': True,
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['prognose'].validators.append(self.prognose_validator)

    def clean(self):
        cleaned_data = super().clean()
        jahr = cleaned_data.get('jahr')
        monat = cleaned_data.get('monat')
        objekt = cleaned_data.get('objekt')
        sortierreihen_folge = cleaned_data.get('sortierreihen_folge')

        if jahr and monat:
            try:
                cleaned_data['datum'] = datetime(int(jahr), int(monat), 1).date()
            except ValueError:
                raise forms.ValidationError(_("Ungültiges Jahr oder Monat"))

        # if objekt and sortierreihen_folge and 'datum' in cleaned_data:
        #     with Session(engine) as session:
        #         existing = session.query(SalesPrognose).filter(
        #             SalesPrognose.objekt == objekt.objekt,
        #             SalesPrognose.sortierreihen_folge == sortierreihen_folge.sort_order,
        #             SalesPrognose.datum == cleaned_data['datum']
        #         ).first()
        #         if existing and (not self.instance or existing.id != self.instance.id):
        #             raise forms.ValidationError(
        #                 _("Diese Kombination aus Objekt ({})، Sortierreihenfolge ({}) und Datum ({}) existiert bereits.").format(
        #                     objekt.objekt, sortierreihen_folge.sort_order, cleaned_data['datum']
        #                 )
        #             )

        return cleaned_data

    def clean_prognose(self):
        prognose = self.cleaned_data['prognose']
        if prognose < 0:
            raise forms.ValidationError(_("Umsatz darf nicht negativ sein."))
        return prognose

    def clean_jahr(self):
        jahr = self.cleaned_data['jahr']
        current_year = datetime.now().year
        if jahr and (jahr < 1900 or jahr > current_year):
            raise forms.ValidationError(_(f'Jahr muss zwischen 1900 und {current_year} sein.'))
        return jahr

    def clean_monat(self):
        monat = self.cleaned_data['monat']
        if monat and (monat < 1 or monat > 12):
            raise forms.ValidationError(_('Monat muss zwischen 1 und 12 sein.'))
        return monat