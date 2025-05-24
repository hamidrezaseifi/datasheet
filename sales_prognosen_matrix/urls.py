from django.urls import include, path

from meinprojekt.urls import DATA_PROVIDER_MAP
from sales_prognosen_matrix.forms import SalesObjektForm, SalesPrognoseForm
from sales_prognosen_matrix.models_sqlalchemy import SALES_PROGNOSE_DATA_PROVIDER, SALES_OBJEKT_DATA_PROVIDER
from shared_fields.views import generic_crud_view, generic_list_view, generic_delete_view, success_view

print("imports successful: prognose.urls")



urlpatterns = SALES_PROGNOSE_DATA_PROVIDER.get_nav_provider().get_urls(SalesObjektForm,
                                                                       generic_crud_view,
                                                                       generic_list_view,
                                                                       generic_delete_view,
                                                                       success_view,
                                                                       DATA_PROVIDER_MAP)



#
# # Definiere alle Provider und ihre Formulare
# print("imports successful: prognose.urls")
#
# DATA_PROVIDERS = {
#     'sales_objekt': {'provider': SALES_OBJEKT_DATA_PROVIDER, 'form': SalesObjektForm},
#     'sales_prognose': {'provider': SALES_PROGNOSE_DATA_PROVIDER, 'form': SalesPrognoseForm},
# }
#
# urlpatterns = []
# for name, config in DATA_PROVIDERS.items():
#     print(f"Generating URLs for {name}")
#     try:
#         urls = config['provider'].get_urls(
#             form_data=config['form'],
#             view_create_func=generic_crud_view,
#             view_list_func=generic_list_view,
#             view_delete_func=generic_delete_view,
#             view_success_func=success_view,
#             data_provider_map=DATA_PROVIDER_MAP,
#             #base_url=f'{name}/'  # Trailing slash
#         )
#         print(f"URLs for {name}: {urls}")
#         urlpatterns += urls
#     except Exception as e:
#         print(f"Error generating URLs for {name}: {e}")
#         raise
#
# print(f"Final urlpatterns: {urlpatterns}")
# print(f"imports successful: {__name__}")
