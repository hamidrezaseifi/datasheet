from django.shortcuts import render

from meinprojekt.navigation import NAVIGATION_DATA


def project_selector_view(request):
    # Manuelle Liste der Gruppen für die Hauptseite
    groups = [
        {'group_name': 'MeineTest'},
        {'group_name': 'Sales'},
    ]
    return render(request, "global/project_selector.html", {
        "groups": groups,
        'navigations': NAVIGATION_DATA,
    })


def normalize_group_name(name: str) -> str:
    return name.replace(" ", "").lower()

