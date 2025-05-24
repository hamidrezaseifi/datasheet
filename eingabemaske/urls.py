# eingabemaske/urls
from django.urls import path

from eingabemaske.forms import UserDataForm
from eingabemaske.models_sqlalchemy import EINGABE_DATA_PROVIDER
from meinprojekt.urls import MENU_MAP
from shared_fields.views import generic_crud_view, generic_list_view, success_view, generic_delete_view

print("imports successful: eingabemaske.urls")

urlpatterns = EINGABE_DATA_PROVIDER.get_nav_provider().get_urls(UserDataForm,
                                                                generic_crud_view,
                                                                generic_list_view,
                                                                generic_delete_view,
                                                                success_view,
                                                                MENU_MAP)

