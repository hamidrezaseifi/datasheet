from django.http import JsonResponse
from django.shortcuts import render

from sales_prognosen_matrix.models_sqlalchemy import SALES_OBJEKT_DATA_PROVIDER
from shared_fields.data_provider import DataProviderBase
from .forms import SalesObjektForm


def sortable_objekt_list_view(request, data_provider: DataProviderBase, base_url, template_name, home: str):
    model_name = SALES_OBJEKT_DATA_PROVIDER.get_model_title()
    base_url = "/" + SALES_OBJEKT_DATA_PROVIDER.get_nav_provider().get_base_url()
    return_url = "/" + SALES_OBJEKT_DATA_PROVIDER.get_nav_provider().get_base_url()

    delete_url = return_url + "/delete_obj"
    add_url = return_url + "/add"
    save_url = return_url + "/save"

    items = _get_sortable_objekt_items()
    object_sort_map = {item['objekt']: item['sort_order'] for item in items}

    form = SalesObjektForm()

    return render(request, 'sales_prognosen_matrix/sortable_objekt.html', {
        'items': items,
        'form': form,
        'model_name': model_name,
        'base_url': base_url,
        'object_sort_map': object_sort_map,
        'return_url': return_url,
        'delete_url': delete_url,
        'add_url': add_url,
        'save_url': save_url,
        'project_home': home
    })


def sortable_objekt_delete_view(request):
    try:
        obj = request.POST['objekt']
        SALES_OBJEKT_DATA_PROVIDER.delete({"objekt": obj}, None)

        return JsonResponse({
            'status': 'success',
            'message': 'Objekt gelöscht',
            'items': []
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Fehler bei löschen : {e}',

        }, status=400)


def sortable_objekt_add_view(request):
    try:
        SALES_OBJEKT_DATA_PROVIDER.add(request.POST)

        return JsonResponse({
            'status': 'success',
            'message': 'Objekt Insert',
            'items': []
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Fehler bei Insert : {e}',

        }, status=400)


def sortable_objekt_save_view(request):
    new_order = request.POST.getlist('order[]')
    if not new_order:
        return JsonResponse({
            'status': 'error',
            'message': 'Keine Order-Daten gesendet'
        }, status=400)
    for index, objekt_id in enumerate(new_order):
        SALES_OBJEKT_DATA_PROVIDER.update(
            p_key={'objekt': objekt_id},
            post_data={'sort_order': index + 1}
        )

    return JsonResponse({
        'status': 'success',
        'message': 'Reihenfolge gespeichert'
    })


def _get_sortable_objekt_items():
    items = SALES_OBJEKT_DATA_PROVIDER.get_all_items()
    items = sorted(items, key=lambda x: x['sort_order'] or 0)
    return items
