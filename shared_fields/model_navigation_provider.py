from typing import List

from django.urls import path


class ModelNavigationProvider:
    _model_title: str = ''
    _base_url: str = ''
    _parent_name: str = ''
    _data_provider: None
    _crud_template_name: str = None
    _list_template_name: str = None

    def __init__(self, model_title: str, base_url: str, parent_name: str, data_provider,
                 crud_template_name: str = 'global/form_view.html',
                 list_template_name: str = 'global/list_view.html'):
        self._model_title = model_title
        self._base_url = base_url
        self._parent_name = parent_name
        self._data_provider = data_provider
        self._crud_template_name = crud_template_name
        self._list_template_name = list_template_name

    def get_urls(
            self,
            form_data,
            view_create_func,
            view_list_func,
            view_delete_func,
            view_success_func
    ) -> List:
        crud_urls = [
            path('', view_list_func, {
                'data_provider': self._data_provider, 'base_url': self._base_url,
                'template_name': self._list_template_name
            }),
            path('list/', view_list_func, {
                'data_provider': self._data_provider, 'base_url': self._base_url,
                'template_name': self._list_template_name
            }),
            path('data/', view_create_func, {
                'data_provider': self._data_provider, 'base_url': self._base_url,
                'form_class': form_data, 'template_name': self._crud_template_name
            }),
            path('delete', view_delete_func, {'data_provider': self._data_provider}),
            path('data/<str:primary_key_base64>/', view_create_func, {
                'data_provider': self._data_provider, 'base_url': self._base_url,
                'form_class': form_data, 'template_name': self._crud_template_name
            }),
            path('success', view_success_func, {
                'model_name': self._model_title, 'base_url': self._base_url
            }),
        ]

        return crud_urls

    def get_model_title(self):
        return self._model_title

    def get_base_url(self):
        return self._base_url

    def get_parent_name(self):
        return self._parent_name

    def get_data_provider(self):
        return self._data_provider


class DummyModelNavigationProvider(ModelNavigationProvider):
    def __init__(self):
        super().__init__('Dummy', 'dummy', 'Dummy', None)

    def get_urls(self, *args, **kwargs):
        return []
