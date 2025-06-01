from meinprojekt.urls import MENU_MAP
from sales_prognosen_matrix.forms import SalesPrognoseForm
from sales_prognosen_matrix.models_sqlalchemy import SALES_PROGNOSE_DATA_PROVIDER
from shared_fields.views import generic_crud_view, generic_list_view, generic_delete_view, success_view

print("imports successful: prognose.urls")

urlpatterns = SALES_PROGNOSE_DATA_PROVIDER.get_nav_provider().get_urls(SalesPrognoseForm,
                                                                       generic_crud_view,
                                                                       generic_list_view,
                                                                       generic_delete_view,
                                                                       success_view,
                                                                       MENU_MAP)

