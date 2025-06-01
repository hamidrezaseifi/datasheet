# shared_fields/forms.py
import os
from pathlib import Path

from django import forms
from django.template import loader
from django.utils.safestring import mark_safe

BASE_DIR = Path(__file__).resolve().parent.parent
template_path = os.path.join(BASE_DIR, 'shared_templates', 'templates', 'global', 'd_sh_choice.html')


class DataSheetChoiceInput(forms.widgets.Widget):
    template_name = 'widgets/d_sh_choice.html'
    input_type = 'url'

    def render(self, request=None, name= None, value=None, attrs=None, renderer=None):
        """Rendering widgets does not use the context processor, manually add (hackish)"""
        attrs['choices'] = self.choices
        context = super(DataSheetChoiceInput, self).get_context(name, value, attrs)
        template = loader.get_template(self.template_name).render(context)
        return mark_safe(template)


