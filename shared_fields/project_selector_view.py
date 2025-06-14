from django.http import Http404
from django.shortcuts import render, redirect
from shared_fields.menu_provider import get_all_project_groups, get_menu_for_project_group, PROJECT_MENUS


def project_selector_view(request):
    # Manuelle Liste der Gruppen für die Hauptseite
    groups = [
        {'group_name': 'MeineTest'},
        {'group_name': 'Sales'},
    ]
    return render(request, "global/project_selector.html", {
        "groups": groups,
        "menu_map": PROJECT_MENUS  # Für den Sidebar in anderen Seiten
    })


def normalize_group_name(name: str) -> str:
    return name.replace(" ", "").lower()


def project_menu_view(request, group_name):
    normalized_input = normalize_group_name(group_name)
    normalized_keys = {normalize_group_name(k): k for k in PROJECT_MENUS.keys()}

    if normalized_input not in normalized_keys:
        raise Http404("Group not found")

    actual_key = normalized_keys[normalized_input]
    menu = PROJECT_MENUS[actual_key]
    first_url = next(iter(menu.values()))
    return redirect(first_url)

# def project_menu_view(request, group_name):
#     normalized_input = group_name.replace(" ", "").lower()
#     normalized_keys = {k.replace(" ", "").lower(): k for k in PROJECT_MENUS.keys()}
#
#     if normalized_input not in normalized_keys:
#         raise Http404("Group not found")
#
#     actual_key = normalized_keys[normalized_input]
#     menu = PROJECT_MENUS[actual_key]
#
#     context = {
#         'menu_map': PROJECT_MENUS,
#         'selected_parent': actual_key,
#         'menu': menu,
#     }
#     return render(request, 'project_menu_template.html', context)


def sidebar_menu_view(request, group_name):
    normalized_input = group_name.replace(" ", "").lower()
    normalized_keys = {k.replace(" ", "").lower(): k for k in PROJECT_MENUS.keys()}

    if normalized_input not in normalized_keys:
        raise Http404("Group not found")

    actual_key = normalized_keys[normalized_input]
    menu = PROJECT_MENUS[actual_key]

    return render(request, 'sidebar_menu.html', {
        'group_name': actual_key,
        'menu': menu
    })


# def project_menu_view(request, group_name):
#     menu = get_menu_for_project_group(group_name)
#     return render(request, "global/project_menu.html", {
#         "group_name": group_name,
#         "menu": menu,
#         "selected_parent": group_name  # Für aktiven Zustand im Sidebar
#     })

# def project_selector_view(request):
#     menu_map = get_all_project_groups()
#     return render(request, "global/project_selector.html", {
#         "menu_map": menu_map
#     })
#
#
# def project_menu_view(request, group_name):
#     menu = get_menu_for_project_group(group_name)
#     return render(request, "global/project_menu.html", {
#         "group_name": group_name,
#         "menu": menu
#     })
