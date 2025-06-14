# eingabemaske/urls

from eingabemaske.forms import UserDataForm
from eingabemaske.models_sqlalchemy import EINGABE_DATA_PROVIDER
from shared_fields.menu_provider import PROJECT_MENUS
from shared_fields.views import generic_crud_view, generic_list_view, success_view, generic_delete_view

print("imports successful: eingabemaske.urls")

urlpatterns = EINGABE_DATA_PROVIDER.get_nav_provider().get_urls(UserDataForm,
                                                                generic_crud_view,
                                                                generic_list_view,
                                                                generic_delete_view,
                                                                success_view,
                                                                PROJECT_MENUS)


