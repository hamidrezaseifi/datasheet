from typing import List

from django.urls import path


class ModelNavigationProvider:
    _model_title: str = ''
    _base_url: str = ''
    _parent_name: str = ''
    _data_provider: None

    def __init__(self, model_title: str, base_url: str, parent_name: str, data_provider):
        self._model_title = model_title
        self._base_url = base_url
        self._parent_name = parent_name
        self._data_provider = data_provider

    def get_urls(self, form_data, view_create_func, view_list_func, view_delete_func, view_success_func,
                 menu_map) -> List:

        return [
            path('', view_list_func,
                 {'data_provider': self._data_provider, 'menu_map': menu_map, 'base_url': self._base_url}),
            path('list/', view_list_func,
                 {'data_provider': self._data_provider, 'menu_map': menu_map, 'base_url': self._base_url}),
            path('data/', view_create_func,
                 {'data_provider': self._data_provider, 'menu_map': menu_map, 'base_url': self._base_url,
                  'form_class': form_data}),
            path('delete', view_delete_func, {'data_provider': self._data_provider}),
            path('data/<str:primary_key_base64>/', view_create_func,
                 {'data_provider': self._data_provider, 'menu_map': menu_map, 'base_url': self._base_url,
                  'form_class': form_data}),
            path('success', view_success_func,
                 {'model_name': self._model_title, 'menu_map': menu_map,
                  'base_url': self._base_url}),
        ]

    def get_model_title(self):
        return self._model_title

    def get_base_url(self):
        return self._base_url

    def get_parent_name(self):
        return self._parent_name

    def get_data_provider(self):
        return self._data_provider