from typing import List

from django.contrib import admin
from django.urls import path, include

from eingabemaske.models_sqlalchemy import EINGABE_DATA_PROVIDER
from planung.models_sqlalchemy import PLANUNG_DATA_PROVIDER
from sales_prognosen_matrix.models_sqlalchemy import SALES_PROGNOSE_DATA_PROVIDER
from shared_fields.data_provider import DataProviderBase
from shared_fields.views import generic_static_view

print("imports successful: meinprojekt.urls")


DATA_PROVIDER_LIST: List[DataProviderBase] = [PLANUNG_DATA_PROVIDER, EINGABE_DATA_PROVIDER, SALES_PROGNOSE_DATA_PROVIDER]

NAV_PROVIDER_LIST = [p.get_nav_provider() for p in DATA_PROVIDER_LIST]

DATA_PROVIDER_MAP = {d.get_model_title(): "/" + d.get_base_url() for d in NAV_PROVIDER_LIST}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', generic_static_view, {'static_html': 'global/home.html', 'data_providers': DATA_PROVIDER_MAP, 'arguments': {}}, name='home_view'),
    path('planung/', include('planung.urls')),
    path('eingabe/', include('eingabemaske.urls')),
    path('prognose/', include('sales_prognosen_matrix.urls')),
]
