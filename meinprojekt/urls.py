from django.urls import path, include

from shared_fields.project_selector_view import project_selector_view
from shared_fields.views import home_view

urlpatterns = [
    path('', project_selector_view, name='home_view'),
    path('planung/', include('planung.urls')),
    path('eingabe/', include('eingabemaske.urls')),
    path('sales/', home_view, {'template_name': 'sales_prognosen_matrix/sales_objekts_home.html',
                 'home': 'sales'}),
    path('sales/prognose/', include('sales_prognosen_matrix.prognose_urls')),
    path('sales/objekte/', include('sales_prognosen_matrix.objekts_urls')),
]
