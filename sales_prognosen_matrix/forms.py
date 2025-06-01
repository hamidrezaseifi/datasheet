# sales_prognosen_matrix/forms.py
from select import select

from django import forms
from django_select2.forms import Select2Widget
from django.core.validators import RegexValidator
from datetime import datetime

from .models import SalesObjektData, SalesPrognoseData
from django.utils.translation import gettext_lazy as _


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
            from sales_prognosen_matrix.models_sqlalchemy import ZVM_OBJEKT_DATA_PROVIDER
            objekte_items = ZVM_OBJEKT_DATA_PROVIDER.get_all_items()
            # print("DEBUG: objekte_items =", objekte_items)
            choices = [('', _('--- Objekt auswählen ---'))] + [
                (item['Kuerzel'], item['Kuerzel']) for item in objekte_items if item.get('Kuerzel')
            ]
            self.fields['objekt'].choices = choices

        except Exception as e:
            print(f"Fehler beim Laden der Objekt-Werte: {e}")
            self.fields['objekt'].choices = [('', '--- Select an Object ---')]
            print("DEBUG: objekt choices set to default")

        if self.instance and self.instance.objekt:
            self.fields['objekt'].initial = self.instance.objekt

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     if self.instance and self.instance.objekt:
    #         self.fields['objekt'].initial = self.instance.objekt
    #     self.fields['objekt'].widget.choices = [
    #         (self.instance.objekt, self.instance.objekt)
    #     ]
    #
    # def clean_objekt(self):
    #     objekt = self.cleaned_data['objekt']
    #     try:
    #         from sales_prognosen_matrix.models_sqlalchemy import ZVM_OBJEKT_DATA_PROVIDER
    #
    #         instance = ZVM_OBJEKT_DATA_PROVIDER.get_instance(p_key={'Kuerzel': objekt})
    #         if not instance:
    #             raise forms.ValidationError(_('Ungültiges Objekt ausgewählt.'))
    #         return objekt
    #     except Exception as e:
    #         raise forms.ValidationError(_('Fehler beim Validieren des Objekts: %s') % str(e))

    def clean_sort_order(self):
        sort_order = self.cleaned_data['sort_order']
        if sort_order < 0:
            raise forms.ValidationError(_("Sortierreihenfolge darf nicht negativ sein."))
        return sort_order


class SalesPrognoseForm(forms.ModelForm):
    prognose_validator = RegexValidator(
        regex=r'^\d+(\.\d{1,2})?$',
        message=_('Nur Zahlen oder Gleitkommazahlen mit bis zu 2 Dezimalstellen sind erlaubt.')
    )
    objekt = forms.ChoiceField(
        label=_('Objekt'),
        choices=[('', '--- wählen Sie ein Objekt ---')],
        widget=forms.Select(attrs={
            'class': 'form-control select2',
            'title': _('Bitte wählen Sie ein Objekt.'),
            'required': True,
        })
    )

    sortierreihen_folge_display = forms.IntegerField(
        label=_('Sortierreihenfolge'),
        required=False,
        widget=forms.NumberInput(attrs={'readonly': 'readonly', 'class': 'form-control'}),
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
        fields = ['objekt', 'sortierreihen_folge', 'jahr', 'monat', 'datum', 'prognose']
        labels = {
            'objekt': _('Objekt'),
            'sortierreihen_folge': _('Sortierreihenfolge'),
            'jahr': _('Jahr'),
            'monat': _('Monat'),
            'prognose': _('Prognose'),
        }
        widgets = {
            'sortierreihen_folge': forms.NumberInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly',
                'disabled': True,
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

        try:
            # Import SQLAlchemy data provider
            from .models_sqlalchemy import SALES_OBJEKT_DATA_PROVIDER

            # Fetch all items from provider
            objekte_items = SALES_OBJEKT_DATA_PROVIDER.get_all_items()
            print("DEBUG: objekte_items =", objekte_items)

            # Create choices for objekt dropdown
            choices = [('', '--- Objekt auswählen ---')] + [
                (item['objekt'], item['objekt'])
                for item in objekte_items if item.get('objekt')
            ]
            print("DEBUG: choices =", choices)
            self.fields['objekt'].choices = choices

        except Exception as e:
            print(f"Fehler beim Laden der Objekt-Werte: {e}")
            self.fields['objekt'].choices = [('', '--- Select an Object ---')]
            self._objekte_items = {}

        # Immer readonly und disabled setzen
        self.fields['sortierreihen_folge'].widget.attrs.update({
            'readonly': 'readonly',
            'disabled': True,
        })
        #**********
        # try:
        #     # SQLAlchemy-Datenprovider importieren
        #     from .models_sqlalchemy import SALES_OBJEKT_DATA_PROVIDER
        #     # Alle Elemente vom Provider holen
        #     objekte_items = SALES_OBJEKT_DATA_PROVIDER.get_all_items()
        #     # Debug: Ausgabe der geholten Elemente
        #     print("DEBUG: objekte_items =", objekte_items)
        #     # Choices für das objekt-Dropdown erstellen, value ist ein Tupel (objekt, sort_order)
        #     choices = [('', '--- Objekt auswählen ---')] + [
        #         ((item['objekt'], item['sort_order']), item['objekt'])
        #         for item in objekte_items if item.get('objekt') and 'sort_order' in item
        #     ]
        #     # Debug: Ausgabe der Choices
        #     print("DEBUG: choices =", choices)
        #     self.fields['objekt'].choices = choices
        #     # Elemente für spätere Verwendung speichern
        #     self._objekte_items = {item['objekt']: item for item in objekte_items}
        #     # Debug: Ausgabe des gespeicherten Dictionaries
        #     print("DEBUG: _objekte_items =", self._objekte_items)
        #
        #     # Objekt für Sortierreihenfolge-Ermittlung initialisieren
        #     objekt = None
        #     sort_order = None
        #
        #     # Bearbeitungs- oder Erstellungsmodus
        #     if self.instance and self.instance.objekt:  # Bearbeitungsmodus
        #         objekt = self.instance.objekt
        #     elif self.data.get('objekt'):  # Erstellungsmodus mit POST-Daten
        #         objekt_data = self.data.get('objekt')
        #         # Objekt_data ist ein Tupel, muss dekodiert werden
        #         try:
        #             objekt, sort_order = eval(objekt_data) if objekt_data else (None, None)
        #         except:
        #             objekt = objekt_data  # Falls kein Tupel, direkt verwenden
        #     elif self.initial.get('objekt'):  # Initiale Daten
        #         objekt = self.initial.get('objekt')
        #
        #     # Sortierreihenfolge initial setzen
        #     if objekt and objekt in self._objekte_items:
        #         sort_order = self._objekte_items[objekt]['sort_order']
        #         self.fields['sortierreihen_folge'].initial = sort_order
        #         # Debug: Ausgabe des gesetzten Werts
        #         print(f"DEBUG: sortierreihen_folge initial set to {sort_order} for objekt {objekt}")
        #
        # except Exception as e:
        #     print(f"Fehler beim Laden der Objekt-Werte: {e}")
        #     self.fields['objekt'].choices = [('', '--- Select an Object ---')]
        #     self._objekte_items = {}
        #
        #     # Sortierreihenfolge-Feld immer deaktivieren
        # self.fields['sortierreihen_folge'].widget.attrs.update({
        #     'readonly': 'readonly',
        #     'disabled': True,
        # })

        # try:
        #     # muss in deser stelle sein
        #     from .models_sqlalchemy import SALES_OBJEKT_DATA_PROVIDER
        #     objekte_items = SALES_OBJEKT_DATA_PROVIDER.get_all_items()
        #     #print("DEBUG: objekte_items =", objekte_items)
        #     choices = [('', _('--- Objekt auswählen ---'))] + [
        #         (item['objekt'], item['objekt']) for item in objekte_items if item.get('objekt')
        #     ]
        #     self.fields['objekt'].choices = choices
        #
        # except Exception as e:
        #     print(f"Fehler beim Laden der Objekt-Werte: {e}")
        #     self.fields['objekt'].choices = [('', '--- Select an Object ---')]
        #     print("DEBUG: objekt choices set to default")

    def clean(self):
        cleaned_data = super().clean()
        jahr = cleaned_data.get('jahr')
        monat = cleaned_data.get('monat')
        objekt = cleaned_data.get('objekt')
        # Set sortierreihen_folge based on objekt
        if objekt and objekt in self._objekte_items:
            cleaned_data['sortierreihen_folge'] = self._objekte_items[objekt]['sort_order']
        else:
            if objekt:
                raise forms.ValidationError('Ungültiges Objekt ausgewählt.')
            cleaned_data['sortierreihen_folge'] = None
        # if objekt:
        #     cleaned_data['sortierreihen_folge'] = objekt.sort_order

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
