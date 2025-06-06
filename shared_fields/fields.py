# shared_fields/fields.py

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
        return str(res[0][1])  # Konvertiere den übersetzten String in einen normalen String
    return 'Not-Found!'
