from meinprojekt.urls import MENU_MAP
from sales_prognosen_matrix.forms import SalesObjektForm
from sales_prognosen_matrix.models_sqlalchemy import SALES_OBJEKT_DATA_PROVIDER
from sales_prognosen_matrix.views import sortable_objekt_list_view, sortable_objekt_delete_view, \
    sortable_objekt_add_view, sortable_objekt_save_view
from shared_fields.views import generic_crud_view, generic_delete_view, success_view


from django.urls import path

print("imports successful: prognose.urls")


extract_urls = [
            path('delete_obj', sortable_objekt_delete_view),
            path('add', sortable_objekt_add_view),
            path('save', sortable_objekt_save_view),
        ]


urlpatterns = (
    SALES_OBJEKT_DATA_PROVIDER.get_nav_provider().get_urls(
        SalesObjektForm,
        generic_crud_view,
        sortable_objekt_list_view,
        generic_delete_view,
        success_view,
        MENU_MAP
    ) + extract_urls

)

print(urlpatterns)
