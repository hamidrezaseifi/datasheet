from django.http import JsonResponse
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse
from sales_prognosen_matrix.models_sqlalchemy import SALES_OBJEKT_DATA_PROVIDER
from shared_fields.data_provider import DataProviderBase
from shared_fields.views import get_selected_parent
from meinprojekt.urls import MENU_MAP
from .forms import SalesObjektForm
from sqlalchemy.exc import IntegrityError


def sortable_objekt_list_view(request, data_provider: DataProviderBase, base_url, menu_map, template_name):
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
        'menu_map': MENU_MAP,
        'selected_parent': get_selected_parent(MENU_MAP, request),
        'object_sort_map': object_sort_map,
        'return_url': return_url,
        'delete_url': delete_url,
        'add_url': add_url,
        'save_url': save_url,
    })


def sortable_objekt_delete_view(request):

    try:
        obj = request.POST['objekt'] #{"objekt": obj}
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
    #items = _get_sortable_objekt_items()
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
    items = _get_sortable_objekt_items()

    return JsonResponse({
        'status': 'success',
        'message': 'Objekt hinzugefügt',
        'items': items
    })


def _get_sortable_objekt_items():
    items = SALES_OBJEKT_DATA_PROVIDER.get_all_items()
    items = sorted(items, key=lambda x: x['sort_order'] or 0)
    return items


def sortable_objekt_view1(request):
    base_url = "sales/objekte"
    model_name = SALES_OBJEKT_DATA_PROVIDER.get_model_title()
    return_url = reverse('sales_objekt_sortable')

    if request.method == 'GET':
        try:
            items = SALES_OBJEKT_DATA_PROVIDER.get_all_items()
            items = sorted(items, key=lambda x: x['sort_order'] or 0)
            object_sort_map = {item['objekt']: item['sort_order'] for item in items}

            form = SalesObjektForm()
            return render(request, 'sales_prognosen_matrix/sortable_objekt.html', {
                'items': items,
                'form': form,
                'model_name': model_name,
                'base_url': base_url,
                'menu_map': MENU_MAP,
                'selected_parent': get_selected_parent(MENU_MAP, request),
                'object_sort_map': object_sort_map,
                'return_url': return_url,
            })
        except Exception as e:
            return render(request, 'global/error.html', {
                'message': str(e),
                'base_url': base_url,
                'menu_map': MENU_MAP,
                'selected_parent': get_selected_parent(MENU_MAP, request),
                'return_url': return_url
            })

    if request.method == 'POST':
        try:
            action = request.POST.get('action')
            user = request.user.username if request.user.is_authenticated else 'Anonymous'

            if action == 'add':
                form = SalesObjektForm(request.POST)
                if form.is_valid():
                    objekt = form.cleaned_data['objekt']
                    sort_order = form.cleaned_data['sort_order']
                    # Check if objekt already exists
                    existing_item = SALES_OBJEKT_DATA_PROVIDER.get_instance({'objekt': objekt})
                    if existing_item:
                        return JsonResponse({
                            'status': 'error',
                            'message': 'Objekt bereits vorhanden',
                            'return_url': return_url
                        }, status=400)
                    try:
                        SALES_OBJEKT_DATA_PROVIDER.add({
                            'objekt': objekt,
                            'sort_order': sort_order,
                            'user': user
                        })
                    except IntegrityError:
                        return JsonResponse({
                            'status': 'error',
                            'message': 'Objekt bereits vorhanden',
                            'return_url': return_url
                        }, status=400)
                    items = SALES_OBJEKT_DATA_PROVIDER.get_all_items()
                    items = sorted(items, key=lambda x: x['sort_order'] or 0)
                    return JsonResponse({
                        'status': 'success',
                        'message': 'Objekt hinzugefügt',
                        'items': items
                    })
                return JsonResponse({
                    'status': 'error',
                    'message': form.errors.as_json(),
                    'return_url': return_url
                }, status=400)

            elif action == 'update_order':
                new_order = request.POST.getlist('order[]')
                if not new_order:
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Keine Order-Daten gesendet',
                        'return_url': return_url
                    }, status=400)
                for index, objekt_id in enumerate(new_order):
                    SALES_OBJEKT_DATA_PROVIDER.update(
                        p_key={'objekt': objekt_id},
                        post_data={'sort_order': index + 1}
                    )
                items = SALES_OBJEKT_DATA_PROVIDER.get_all_items()
                items = sorted(items, key=lambda x: x['sort_order'] or 0)
                return JsonResponse({
                    'status': 'success',
                    'message': 'Reihenfolge gespeichert',
                    'items': items
                })

            elif action == 'delete':
                objekt_id = request.POST.get('objekt_id')
                instance = SALES_OBJEKT_DATA_PROVIDER.get_instance({'objekt': objekt_id})
                if instance:
                    SALES_OBJEKT_DATA_PROVIDER.delete({'objekt': objekt_id}, instance)
                    items = SALES_OBJEKT_DATA_PROVIDER.get_all_items()
                    items = sorted(items, key=lambda x: x['sort_order'] or 0)
                    return JsonResponse({
                        'status': 'success',
                        'message': 'Objekt gelöscht',
                        'items': items
                    })
                return JsonResponse({
                    'status': 'error',
                    'message': 'Objekt nicht gefunden',
                    'return_url': return_url
                }, status=404)

            elif action == 'edit':
                objekt_id = request.POST.get('objekt_id')
                form = SalesObjektForm(request.POST)
                if form.is_valid():
                    objekt = form.cleaned_data['objekt']
                    existing_item = SALES_OBJEKT_DATA_PROVIDER.get_instance({'objekt': objekt})
                    if existing_item and existing_item['objekt'] != objekt_id:
                        return JsonResponse({
                            'status': 'error',
                            'message': 'Objekt bereits vorhanden',
                            'return_url': return_url
                        }, status=400)
                    SALES_OBJEKT_DATA_PROVIDER.update(
                        p_key={'objekt': objekt_id},
                        post_data={
                            'objekt': objekt,
                            'sort_order': form.cleaned_data['sort_order']
                        }
                    )
                    items = SALES_OBJEKT_DATA_PROVIDER.get_all_items()
                    items = sorted(items, key=lambda x: x['sort_order'] or 0)
                    return JsonResponse({
                        'status': 'success',
                        'message': 'Objekt aktualisiert',
                        'items': items
                    })
                return JsonResponse({
                    'status': 'error',
                    'message': form.errors.as_json(),
                    'return_url': return_url
                }, status=400)

            return JsonResponse({
                'status': 'error',
                'message': 'Ungültige Aktion',
                'return_url': return_url
            }, status=400)

        except Exception as e:
            messages.error(request, str(e))
            return JsonResponse({
                'status': 'error',
                'message': str(e),
                'return_url': return_url
            }, status=400)
