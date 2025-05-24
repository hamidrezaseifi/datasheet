

import re  # RegEx für Validierung importieren

# Dictionary mit Feldkonfigurationen
# Beschreibung: Definition der standardisierten Felder mit Validierungsregeln, Eingabetypen und Fehlermeldungen
FIELD_CONFIGS = {
    'name': {
        # Validierungsfunktion für das Feld 'name'
        # Beschreibung: Prüft, ob nur Buchstaben, Umlaute, Leerzeichen und Bindestriche eingegeben wurden
        'validate': lambda value: ValueError('Nur Buchstaben, Umlaute, Bindestriche und Leerzeichen erlaubt.') if value and not re.match(r'^[a-zA-ZäöüÄÖÜß\s-]+$', value) else None,
        'required': False,  # Feld ist optional, da es in Eingabe nullable=True ist
        'type': 'text',    # HTML-Eingabetyp für Textfelder
        'error_message': 'Nur Buchstaben, Umlaute, Bindestriche und Leerzeichen erlaubt.'
    },
    'email': {
        # Validierungsfunktion für das Feld 'email'
        # Beschreibung: Prüft, ob eine gültige E-Mail-Adresse eingegeben wurde
        'validate': lambda value: ValueError('Ungültige E-Mail-Adresse.') if value and not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value) else None,
        'required': True,   # Feld ist erforderlich, da es in Eingabe nullable=False und Primärschlüssel ist
        'type': 'email',   # HTML-Eingabetyp für E-Mail-Felder
        'error_message': 'Ungültige E-Mail-Adresse.'
    },
    'objekt_name': {
        'validate': lambda value: ValueError('Nur Buchstaben, Umlaute, Bindestriche und Leerzeichen erlaubt.') if value and not re.match(r'^[a-zA-ZäöüÄÖÜß\s-]+$', value) else None,
        'required': False,
        'type': 'text',
        'error_message': 'Nur Buchstaben, Umlaute, Bindestriche und Leerzeichen erlaubt.'
    }
}
