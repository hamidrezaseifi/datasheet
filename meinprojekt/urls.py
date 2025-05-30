from typing import List

from django.contrib import admin
from django.urls import path, include

from eingabemaske.models_sqlalchemy import EINGABE_DATA_PROVIDER
from planung.models_sqlalchemy import PLANUNG_DATA_PROVIDER
from sales_prognosen_matrix.models_sqlalchemy import SALES_PROGNOSE_DATA_PROVIDER, SALES_OBJEKT_DATA_PROVIDER
from shared_fields.data_provider import DataProviderBase
from shared_fields.views import generic_static_view

DATA_PROVIDER_LIST: List[DataProviderBase] = [PLANUNG_DATA_PROVIDER,
                                              EINGABE_DATA_PROVIDER,
                                              SALES_PROGNOSE_DATA_PROVIDER,
                                              SALES_OBJEKT_DATA_PROVIDER]

NAV_PROVIDER_LIST = [p.get_nav_provider() for p in DATA_PROVIDER_LIST]

MENU_MAP = {}
for n in NAV_PROVIDER_LIST:
    parent_name = n.get_parent_name()
    if parent_name not in MENU_MAP:
        MENU_MAP[parent_name] = {}
    title = n.get_model_title()
    MENU_MAP[parent_name][title] = "/" + n.get_base_url()

print(f"Parents: {MENU_MAP}")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', generic_static_view, {'static_html': 'global/home.html', 'menu_map': MENU_MAP, 'arguments': {}}, name='home_view'),
    path('planung/', include('planung.urls')),
    path('eingabe/', include('eingabemaske.urls')),
    path('sales/prognose/', include('sales_prognosen_matrix.prognose_urls')),
    path('sales/objekte/', include('sales_prognosen_matrix.objekts_urls')),
]
