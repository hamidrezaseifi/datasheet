from django.core.exceptions import BadRequest
from django.shortcuts import render, redirect
from django.urls import reverse

from shared_fields.data_provider import DataProviderBase
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest


def generic_crud_view(request, data_provider: DataProviderBase, form_class, base_url, data_providers, primary_key_base64=None):

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
        #form.is_valid()

        if instance:
            data_provider.update(primary_key, request.POST)
            print(f"updated sqlalchemy: {instance}")
        else:
            #instance = model_class(**form.cleaned_data)
            #print(f"inserting sqlalchemy: {instance}")
            data_provider.add(request.POST)

        print("redirecting to success")
        #return redirect(f'/{base_url}/success', model_name=data_provider.get_model_title())
        return redirect(f'/{base_url}/success', model_name=data_provider.get_nav_provider().get_model_title())

    else:
        form = form_class(instance=django_instance)

    return render(request, 'global/form_view.html',
                  {
                      'data_providers': data_providers,
                      'base_url': base_url,
                      'form': form,
                      'instance': instance,
                      'model_name': data_provider.get_nav_provider().get_model_title()
                  }
                  )


def generic_delete_view(request, data_provider: DataProviderBase):

    model_class = data_provider.get_data_model()

    if 'key' not in request.POST:
        return HttpResponseBadRequest("Invalid request. key to delete not found!", content_type="text/plain")

    primary_key_base64 = request.POST['key']

    primary_key = data_provider.convert_base64_to_dic(primary_key_base64)

    data_provider.delete(primary_key, None)

    data = {
        'key-to-delete': primary_key
    }
    return JsonResponse(data)


def generic_list_view(request, data_provider: DataProviderBase, base_url, data_providers):

    max_page_index = 6

    page_index = 1
    item_count = 15
    if request.GET:
        if 'page' in request.GET:
            page_index = int(request.GET['page'])
        if 'count' in request.GET:
            item_count = int(request.GET['count'])

    columns = data_provider.get_columns()
    total, page_count, data_items = data_provider.get_items(item_count=item_count, page=page_index)
    pk_columns = data_provider.get_primary_key()

    page_index_list = _generate_page_index_list(max_page_index, page_count, page_index)

    return render(request, 'global/list_view.html',
                  {'data_providers': data_providers,
                   'total': total,
                   'page_count': page_count,
                   'page_list': page_index_list,
                   'page_index': page_index,
                   'item_count': item_count,
                   'items': data_items,
                   'columns': columns,
                   'model_name': data_provider.get_nav_provider().get_model_title(),
                   'base_url': base_url,
                   'pk_columns': pk_columns
                   }
                  )


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


def generic_static_view(request, static_html, data_providers, arguments):
    print("start generic_static_view for ", static_html)
    return render(request, static_html, {'data_providers': data_providers, 'data': arguments})


def success_view(request, model_name, base_url, data_providers):
    return render(request, 'global/success.html', {'data_providers': data_providers, 'base_url': base_url, 'model_name': model_name})
