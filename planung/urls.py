from planung.forms import PlanungForm
from planung.models_sqlalchemy import PLANUNG_DATA_PROVIDER
from shared_fields.views import generic_crud_view, generic_list_view, success_view, generic_delete_view

print("imports successful: planung.urls")


urlpatterns = PLANUNG_DATA_PROVIDER.get_nav_provider().get_urls(PlanungForm,
                                                                generic_crud_view,
                                                                generic_list_view,
                                                                generic_delete_view,
                                                                success_view)
