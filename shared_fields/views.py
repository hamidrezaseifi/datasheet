from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect

from shared_fields.data_provider import DataProviderBase


def generic_crud_view(request, data_provider: DataProviderBase, form_class, base_url, menu_map,
                      primary_key_base64=None):
    selected_parent = get_selected_parent(menu_map, request)

    instance = None
    django_instance = None
    primary_key = None
    if primary_key_base64 and primary_key_base64 not in ['success', 'list']:
        primary_key = data_provider.convert_base64_to_dic(primary_key_base64)

        instance = data_provider.get_instance(primary_key)
        django_instance = data_provider.get_django_instance(primary_key, instance)
        print(f"Loaded instance: {instance}")

    if request.method == 'POST' and 'delete' in request.POST:
        if instance:
            data_provider.delete(primary_key, instance)
            print(f"deleted sqlalchemy: {primary_key}")
        return redirect(f'/{base_url}/list')

    if request.method == 'POST' and 'delete' not in request.POST:
        print(f"POST data in generic_crud_view: {request.POST}")
        form = form_class(request.POST)
        # form.is_valid()

        if instance:
            data_provider.update(primary_key, request.POST)
            print(f"updated sqlalchemy: {instance}")
        else:
            # instance = model_class(**form.cleaned_data)
            # print(f"inserting sqlalchemy: {instance}")
            data_provider.add(request.POST)

        print("redirecting to success")
        # return redirect(f'/{base_url}/success', model_name=data_provider.get_model_title())
        return redirect(f'/{base_url}/success', {
            "model_name": data_provider.get_nav_provider().get_model_title(),
            "selected_parent": selected_parent})

    else:
        form = form_class(instance=django_instance)

    return render(request, 'global/form_view.html',
                  {
                      'menu_map': menu_map,
                      'base_url': base_url,
                      'form': form,
                      'instance': instance,
                      'model_name': data_provider.get_nav_provider().get_model_title(),
                      "selected_parent": selected_parent
                  }
                  )


def generic_delete_view(request, data_provider: DataProviderBase):
    if 'key' not in request.POST:
        return HttpResponseBadRequest("Invalid request. key to delete not found!", content_type="text/plain")

    primary_key_base64 = request.POST['key']

    primary_key = data_provider.convert_base64_to_dic(primary_key_base64)

    data_provider.delete(primary_key, None)

    data = {
        'key-to-delete': primary_key
    }
    return JsonResponse(data)


def generic_list_view(request, data_provider: DataProviderBase, base_url, menu_map):
    max_page_index = 6

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

    columns = data_provider.get_columns()
    total, page_count, data_items = data_provider.get_items(item_count=item_count,
                                                            page=page_index,
                                                            sort_col=sort_col,
                                                            sort_type=sort_type,
                                                            search_col=search_col,
                                                            search_value=search_value)
    if page_index > page_count:
        page_index = page_count
    pk_columns = data_provider.get_primary_key()

    page_index_list = _generate_page_index_list(max_page_index, page_count, page_index)

    selected_parent = get_selected_parent(menu_map, request)

    return render(request, 'global/list_view.html',
                  {'menu_map': menu_map,
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
                   "search_value": search_value
                   }
                  )


def generic_static_view(request, static_html, menu_map, arguments):
    selected_parent = get_selected_parent(menu_map, request)

    return render(request, static_html, {
        'menu_map': menu_map,
        'data': arguments,
        "selected_parent": selected_parent})


def success_view(request, model_name, base_url, menu_map):
    selected_parent = get_selected_parent(menu_map, request)

    return render(request, 'global/success.html',
                  {'menu_map': menu_map,
                   'base_url': base_url,
                   'model_name': model_name,
                   "selected_parent": selected_parent})


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
