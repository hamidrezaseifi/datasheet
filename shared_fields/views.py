from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.urls import reverse

from shared_fields.data_provider import DataProviderBase, DuplicateKeyError


def generic_crud_view(request, data_provider: DataProviderBase, form_class, base_url, menu_map,
                      template_name: str,
                      primary_key_base64=None):
    """
    Generische View für CRUD-Operationen mit DataProviderBase.
    """
    selected_parent = get_selected_parent(menu_map, request)

    # Set return_url dynamically
    return_url = f"/{base_url}/list"  # Default to list view
    #if base_url == 'sales/objekte':
    #    return_url = reverse('sales_objekt_sortable')

    instance = None
    django_instance = None
    primary_key = None
    if primary_key_base64 and primary_key_base64 not in ['success', 'list']:
        primary_key = data_provider.convert_base64_to_dic(primary_key_base64)

        instance = data_provider.get_instance(primary_key)
        django_instance = data_provider.get_django_instance(primary_key, instance)
        print(f"Loaded instance: {instance}")

    if request.method == 'POST' and 'delete' in request.POST:
        """Datensatz löschen."""
        if instance:
            data_provider.delete(primary_key, instance)
            print(f"deleted sqlalchemy: {primary_key}")
        return redirect(return_url)  # Redirect to return_url

    if request.method == 'POST' and 'delete' not in request.POST:
        """Neuen oder bestehenden Datensatz speichern."""
        print(f"POST data in generic_crud_view: {request.POST}")
        form = form_class(request.POST)
        # form.is_valid()

        if instance:
            # If instance exists, update it
            data_provider.update(primary_key, request.POST)
            print(f"updated sqlalchemy: {instance}")
        else:
            # If no instance, try to add a new one
            # instance = model_class(**form.cleaned_data)
            # print(f"inserting sqlalchemy: {instance}")
            try:
                data_provider.add(request.POST)
            except (DuplicateKeyError, ValueError) as e:
                # If a duplicate key error occurs, render error page with message
                # Fehlerseite mit vollständigem Context rendern
                return render(request, "global/error.html", {
                    "message": str(e),
                    "base_url": base_url,
                    "menu_map": menu_map,
                    "selected_parent": selected_parent,
                    "return_url": return_url
                })

        print("redirecting to success")
        return redirect(f'/{base_url}/success', {
            "model_name": data_provider.get_nav_provider().get_model_title(),
            "selected_parent": selected_parent,
            "return_url": return_url
        })

    else:
        """Formular für neue oder bestehende Daten anzeigen."""
        if django_instance and hasattr(django_instance, '_meta'):
            # Wenn das Objekt ein Django ORM-Objekt ist
            form = form_class(instance=django_instance)
        elif django_instance:
            # Wenn das Objekt ein SQLAlchemy-Objekt ist, nutze initial und filtere private Felder heraus
            initial_data = {k: v for k, v in django_instance.__dict__.items() if not k.startswith('_')}
            form = form_class(initial=initial_data)
        else:
            # Wenn kein Objekt vorhanden ist, erstelle ein leeres Formular
            form = form_class()

    return render(request, template_name,
                  {
                      'menu_map': menu_map,
                      'base_url': base_url,
                      'form': form,
                      'instance': instance,
                      'model_name': data_provider.get_nav_provider().get_model_title(),
                      "selected_parent": selected_parent,
                      "extrac_data": data_provider.get_edit_extra_data(),
                      "return_url": return_url
                  })


def generic_delete_view(request, data_provider: DataProviderBase):
    base_url = data_provider.get_nav_provider().get_base_url()
    return_url = f"/{base_url}/list"

    if 'key' not in request.POST:
        #return HttpResponseBadRequest("Invalid request. key to delete not found!", content_type="text/plain")
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid request. Key to delete not found!',
            'return_url': return_url
        }, status=400)

    try:
        primary_key_base64 = request.POST['key']
        primary_key = data_provider.convert_base64_to_dic(primary_key_base64)
        data_provider.delete(primary_key, None)
        return JsonResponse({
            'status': 'success',
            'key-to-delete': primary_key
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e),
            'return_url': return_url
        }, status=400)


def generic_list_view(request, data_provider: DataProviderBase, base_url, menu_map, template_name):
    max_page_index = 6
    return_url = f"/{base_url}/list"
    page_index = 1
    item_count = 15
    sort_col = ''
    sort_type = ''
    search_col = ''
    search_value = ''
    if request.GET:
        if 'page' in request.GET:
            page_index = int(request.GET['page'])
        if 'count' in request.GET:
            item_count = int(request.GET['count'])
        if 'sort_col' in request.GET:
            sort_col = request.GET['sort_col']
        if 'sort_type' in request.GET:
            sort_type = request.GET['sort_type']
        if 'search_col' in request.GET:
            search_col = request.GET['search_col']
        if 'search_value' in request.GET:
            search_value = request.GET['search_value']

    try:
        columns = data_provider.get_columns()
        total, page_count, data_items = data_provider.get_items(
            item_count=item_count,
            page=page_index,
            sort_col=sort_col,
            sort_type=sort_type,
            search_col=search_col,
            search_value=search_value
        )
        if page_index > page_count:
            page_index = page_count
        pk_columns = data_provider.get_primary_key()
        page_index_list = _generate_page_index_list(max_page_index, page_count, page_index)
        selected_parent = get_selected_parent(menu_map, request)

        return render(request, template_name, {
            'menu_map': menu_map,
            'total': total,
            'page_count': page_count,
            'page_list': page_index_list,
            'page_index': page_index,
            'item_count': item_count,
            'items': data_items,
            'columns': columns,
            'model_name': data_provider.get_nav_provider().get_model_title(),
            'base_url': base_url,
            'pk_columns': pk_columns,
            "selected_parent": selected_parent,
            "sort_col": sort_col,
            "sort_type": sort_type,
            "search_col": search_col,
            "search_value": search_value,
            "return_url": return_url
        })
    except Exception as e:
        return render(request, 'global/error.html', {
            'message': str(e),
            'base_url': base_url,
            'menu_map': menu_map,
            'selected_parent': selected_parent,
            'return_url': return_url
        })


def generic_static_view(request, static_html, menu_map, arguments):
    selected_parent = get_selected_parent(menu_map, request)
    return_url = '/'  # Default to home

    try:
        return render(request, static_html, {
            'menu_map': menu_map,
            'data': arguments,
            "selected_parent": selected_parent,
            "return_url": return_url
        })
    except Exception as e:
        return render(request, 'global/error.html', {
            'message': str(e),
            'menu_map': menu_map,
            'selected_parent': selected_parent,
            'return_url': return_url
        })


def success_view(request, model_name, base_url, menu_map):
    selected_parent = get_selected_parent(menu_map, request)
    return_url = f"/{base_url}/list"
    try:
        return render(request, 'global/success.html', {
            'menu_map': menu_map,
            'base_url': base_url,
            'model_name': model_name,
            "selected_parent": selected_parent,
            "return_url": return_url
        })
    except Exception as e:
        return render(request, 'global/error.html', {
            'message': str(e),
            'base_url': base_url,
            'menu_map': menu_map,
            'selected_parent': selected_parent,
            'return_url': return_url
        })


def get_selected_parent(menu_map, request):
    selected_parent = None
    for par in menu_map:
        for proj in menu_map[par]:
            print(f"Search {menu_map[par][proj]} in {request.path}")
            if menu_map[par][proj] in request.path:
                selected_parent = par
                break
    return selected_parent


def _generate_page_index_list(max_page_index, page_count, page_index):
    start = page_index - int(max_page_index / 2)
    end = page_index + int(max_page_index / 2)
    if start < 1:
        end += 1 - start
        start = 1
    if end > page_count + 1:
        end = page_count + 1
    page_index_list = range(start, end)
    return page_index_list
