from typing import List

from django.contrib import admin
from django.urls import path, include
from shared_fields.menu_provider import PROJECT_MENUS

# from eingabemaske.models_sqlalchemy import EINGABE_DATA_PROVIDER
# from planung.models_sqlalchemy import PLANUNG_DATA_PROVIDER
# from sales_prognosen_matrix.models_sqlalchemy import SALES_PROGNOSE_DATA_PROVIDER, SALES_OBJEKT_DATA_PROVIDER
# from shared_fields.data_provider import DataProviderBase
from shared_fields.views import generic_static_view

from shared_fields.project_selector_view import project_selector_view, project_menu_view

# DATA_PROVIDER_LIST: List[DataProviderBase] = [EINGABE_DATA_PROVIDER,
#                                               PLANUNG_DATA_PROVIDER,
#                                               SALES_OBJEKT_DATA_PROVIDER,
#                                               SALES_PROGNOSE_DATA_PROVIDER
#                                               ]
#
# NAV_PROVIDER_LIST = [p.get_nav_provider() for p in DATA_PROVIDER_LIST]
#
# MENU_MAP = {}
# for n in NAV_PROVIDER_LIST:
#     parent_name = n.get_parent_name()
#     if parent_name not in MENU_MAP:
#         MENU_MAP[parent_name] = {}
#     title = n.get_model_title()
#     MENU_MAP[parent_name][title] = "/" + n.get_base_url()
#
# print(f"Parents: {MENU_MAP}")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('select2/', include('django_select2.urls')),

    #path('projects/', project_selector_view, name='project_selector'),
    path('projects/<str:group_name>/', project_menu_view, name='project_menu'),

    path('', project_selector_view, name='home_view'),
    #path('', generic_static_view, {'static_html': 'global/home.html', 'menu_map': PROJECT_MENUS, 'arguments': {}},
    #     name='home_view'),
    path('planung/', include('planung.urls')),
    path('eingabe/', include('eingabemaske.urls')),
    path('sales/prognose/', include('sales_prognosen_matrix.prognose_urls')),
    path('sales/objekte/', include('sales_prognosen_matrix.objekts_urls')),
]
