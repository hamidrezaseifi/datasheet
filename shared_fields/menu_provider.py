from typing import List, Dict
from eingabemaske.models_sqlalchemy import EINGABE_DATA_PROVIDER
from planung.models_sqlalchemy import PLANUNG_DATA_PROVIDER
from sales_prognosen_matrix.models_sqlalchemy import SALES_PROGNOSE_DATA_PROVIDER, SALES_OBJEKT_DATA_PROVIDER
from shared_fields.data_provider import DataProviderBase

# 1. List of all data providers
DATA_PROVIDER_LIST: List[DataProviderBase] = [
    EINGABE_DATA_PROVIDER,
    PLANUNG_DATA_PROVIDER,
    SALES_OBJEKT_DATA_PROVIDER,
    SALES_PROGNOSE_DATA_PROVIDER
]

# 2. Build nav providers
NAV_PROVIDER_LIST = [p.get_nav_provider() for p in DATA_PROVIDER_LIST]


def get_all_project_groups() -> Dict[str, List[str]]:
    """
    Example output:
    {
        "Meine Test": ["Eingabe", "Planung"]
    }
    """
    groups = {}
    for nav in NAV_PROVIDER_LIST:
        parent = nav.get_parent_name()
        title = nav.get_model_title()

        if parent not in groups:
            groups[parent] = []
        groups[parent].append(title)

    return groups


def get_menu_for_project_group(group_name: str) -> Dict[str, str]:
    """
    Example input: "Meine Test"
    Output:
    {
        "Eingabe": "/eingabe",
        "Planung": "/planung"
    }
    """
    menu = {}
    for nav in NAV_PROVIDER_LIST:
        if nav.get_parent_name() == group_name:
            menu[nav.get_model_title()] = "/" + nav.get_base_url()
    return menu


def generate_project_menus():
    project_menus = {}
    for nav in NAV_PROVIDER_LIST:
        parent = nav.get_parent_name()
        title = nav.get_model_title()
        url = "/" + nav.get_base_url()

        if parent not in project_menus:
            project_menus[parent] = {}

        project_menus[parent][title] = url

    return project_menus


PROJECT_MENUS = generate_project_menus()