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
