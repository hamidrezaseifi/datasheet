from django.contrib import admin
from django.urls import path, include

from shared_fields.project_selector_view import project_selector_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('select2/', include('django_select2.urls')),

    path('', project_selector_view, name='home_view'),
    path('planung/', include('planung.urls')),
    path('eingabe/', include('eingabemaske.urls')),
    path('sales/prognose/', include('sales_prognosen_matrix.prognose_urls')),
    path('sales/objekte/', include('sales_prognosen_matrix.objekts_urls')),
]
