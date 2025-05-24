# eingabemaske/forms.py
from django import forms
from django.core.validators import RegexValidator

from .models import UserData
from django.utils.translation import gettext_lazy as _


class UserDataForm(forms.ModelForm):
    # Validator für das name-Feld: Nur Buchstaben, Umlaute, ß und Leerzeichen
    name_validator = RegexValidator(
        regex=r'^[A-Za-zäöüÄÖÜß\s]+$',
        message=_('Nur Buchstaben, Umlaute und Leerzeichen sind erlaubt.')
    )

    # Validator für das email-Feld: Gültige E-Mail-Adressen
    email_validator = RegexValidator(
        regex=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
        message=_('Bitte gib eine gültige E-Mail-Adresse ein.')
    )

    class Meta:
        model = UserData
        fields = ['name', 'email']
        labels = {
            'name': _('Name'),
            'email': _('E-Mail'),
        }

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Name eingeben'),
                'pattern': '[A-Za-zäöüÄÖÜß\\s]+',  # HTML5-Validierung für Browser
                'title': _('Nur Buchstaben, Umlaute und Leerzeichen sind erlaubt.')
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': _('E-Mail eingeben'),
                'type': 'email',
                'title': _('Bitte gib eine gültige E-Mail-Adresse ein.')
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].validators.append(self.name_validator)
        self.fields['email'].validators.append(self.email_validator)
        self.fields['name'].required = False
        self.fields['email'].required = True  # muss insert werden weil  pk is
        print(f"UserDataForm fields: {self.fields.keys()}")

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name and not name.strip():
            raise forms.ValidationError(_('Der Name darf nicht nur aus Leerzeichen bestehen.'))
        return name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and '@example.com' in email:
            raise forms.ValidationError(_('E-Mail-Adressen von example.com sind nicht erlaubt.'))
        return email
