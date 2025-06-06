# sales_prognosen_matrix/forms.py

from datetime import datetime

from django import forms
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from shared_fields.fields import month_choices, get_month_name
from shared_fields.forms import DataSheetChoiceInput
from .models import SalesObjektData, SalesPrognoseData


class SalesObjektForm(forms.ModelForm):
    objekt = forms.ChoiceField(
        label=_('Objekt'),
        choices=[('', '--- wählen Sie ein Objekt ---')],
        widget=forms.Select(attrs={
            'class': 'form-control select2',
            'title': _('Bitte wählen Sie ein Objekt.'),
            'required': True,
        })
    )

    class Meta:
        model = SalesObjektData
        fields = ['objekt', 'sort_order']
        labels = {
            'objekt': _('Objekt'),
            'sort_order': _('Sortierreihenfolge'),
        }
        widgets = {
            'sort_order': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': _('Sortierreihenfolge eingeben'),
                'pattern': '\\d+',
                'title': _('Nur Zahlen sind erlaubt.'),
                'required': True,
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            # muss in deser stelle sein
            from sales_prognosen_matrix.models_sqlalchemy import ZVM_OBJEKT_DATA_PROVIDER, SALES_OBJEKT_DATA_PROVIDER

            objekte_items = ZVM_OBJEKT_DATA_PROVIDER.get_all_items()
            # print("DEBUG: objekte_items =", objekte_items)
            filtered_items = [
                item for item in objekte_items
                if item['Vertriebsweg'] and item['Vertriebsweg'].lower() != "not"
            ]
            sales_objekte_items = SALES_OBJEKT_DATA_PROVIDER.get_all_items()
            sales_objekte_items = [
                item['objekt']
                for item in sales_objekte_items
            ]

            filtered_items = [
                item for item in filtered_items
                if item['Kuerzel'] not in sales_objekte_items
            ]

            # print("DEBUG: filtered_items =", filtered_items)
            choices = [('', _('--- Objekt auswählen ---'))] + [(item['Kuerzel'], item['Kuerzel']) for item in
                                                               filtered_items]
            self.fields['objekt'].choices = choices

            items = SALES_OBJEKT_DATA_PROVIDER.get_all_items()
            max_order = 1
            if items:
                max_order = max(item['sort_order'] or 0 for item in items) + 1
            self.fields['sort_order'].initial = max_order


        except Exception as e:
            print(f"Fehler beim Laden der Objekt-Werte: {e}")
            self.fields['objekt'].choices = [('', '--- Select an Object ---')]
            print("DEBUG: objekt choices set to default")

        if self.instance and self.instance.objekt:
            self.fields['objekt'].initial = self.instance.objekt

    def clean_sort_order(self):
        sort_order = self.cleaned_data['sort_order']
        if sort_order < 0:
            raise forms.ValidationError(_("Sortierreihenfolge darf nicht negativ sein."))
        return sort_order

    def clean_objekt(self):
        objekt = self.cleaned_data['objekt']
        # Lazy Import
        from sales_prognosen_matrix.models_sqlalchemy import SALES_OBJEKT_DATA_PROVIDER
        if SALES_OBJEKT_DATA_PROVIDER.check_duplicate_by_pk_dict({'objekt': objekt}):
            raise forms.ValidationError(_("Dieses Objekt existiert bereits."))
        return objekt


class SalesPrognoseForm(forms.ModelForm):
    prognose_validator = RegexValidator(
        regex=r'^\d+(\.\d{1,2})?$',
        message=_('Nur Zahlen oder Gleitkommazahlen mit bis zu 2 Dezimalstellen sind erlaubt.')
    )
    objekt = forms.ChoiceField(
        label=_('Objekt'),
        choices=[],
        widget=DataSheetChoiceInput(attrs={
            'class': 'form-control',
            'choices': [],
            'item_name': 'Objekt',
            'type': 'file',
            'on_change': 'objekt_changed();'  # use if needed
        })
    )

    jahr = forms.IntegerField(
        required=True,
        min_value=1900,
        max_value=datetime.now().year,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': _('Jahr eingeben'),
            'title': _('Jahr muss zwischen 1900 und dem aktuellen Jahr liegen.'),
        })
    )
    monat = forms.ChoiceField(
        choices=month_choices,
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'title': _('Wählen Sie einen Monat aus.'),
        })
    )

    class Meta:
        model = SalesPrognoseData
        fields = ['objekt', 'jahr', 'monat', 'prognose']
        labels = {
            'objekt': _('Objekt'),
            'jahr': _('Jahr'),
            'monat': _('Monat'),
            'prognose': _('Prognose'),
        }
        widgets = {
            'jahr': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': _('Jahr eingeben'),
                'min': 2020,
                'max': datetime.now().year,
                'title': _('Jahr muss zwischen 2020 und dem aktuellen Jahr liegen.'),
                'required': True,
            }),
            'monat': forms.Select(attrs={
                'class': 'form-control',
                'title': _('Wählen Sie einen Monat aus.'),
                'required': True,
            }),

            'prognose': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': _('Prognose eingeben'),
                'title': _('Nur Zahlen oder Gleitkommazahlen sind erlaubt.'),
                'required': True,
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['jahr'].initial = datetime.now().year
        self.fields['prognose'].initial = None
        self.fields['prognose'].validators.append(self.prognose_validator)

        try:
            # Import SQLAlchemy data provider
            from .models_sqlalchemy import SALES_OBJEKT_DATA_PROVIDER

            # Fetch all items from provider
            objekte_items = SALES_OBJEKT_DATA_PROVIDER.get_all_items()
            print("DEBUG: objekte_items =", objekte_items)

            # Create choices for objekt dropdown
            choices = [
                (item['objekt'], item['objekt'])
                for item in objekte_items if item.get('objekt')
            ]
            self.fields['objekt'].choices = choices

        except Exception as e:
            print(f"Fehler beim Laden der Objekt-Werte: {e}")
            self.fields['objekt'].choices = [('', '--- Select an Object ---')]
            self._objekte_items = {}

    def clean(self):
        cleaned_data = super().clean()
        jahr = cleaned_data.get('jahr')
        monat = cleaned_data.get('monat')
        objekt = cleaned_data.get('objekt')
        # Set sortierreihen_folge based on objekt
        # if objekt and objekt in self._objekte_items:
        #     cleaned_data['sortierreihen_folge'] = self._objekte_items[objekt]['sort_order']
        # else:
        #     if objekt:
        #         raise forms.ValidationError('Ungültiges Objekt ausgewählt.')
        #     cleaned_data['sortierreihen_folge'] = None

        if jahr and monat:
            try:
                cleaned_data['datum'] = datetime(int(jahr), int(monat), 1).date()
            except ValueError:
                raise forms.ValidationError(_("Ungültiges Jahr oder Monat"))

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
