# eingabemaske/models_sqlalchemy.py
from typing import Dict

from sqlalchemy import Column, String, Integer
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base

from shared_fields.data_provider import DataProviderBase, DatabaseConfig

Base = declarative_base()


class Navigation(Base):
    __tablename__ = 'navigation'
    __table_args__ = {'schema': 'test_evar.djange'}
    id = Column(Integer, primary_key=True, nullable=False)
    parent = Column(Integer, primary_key=True, nullable=False)
    nav_name = Column(String(255), nullable=False)
    start_page = Column(Integer, primary_key=True, nullable=False)
    url = Column(String(255), nullable=False)


class NavigationDataProvider(DataProviderBase):

    def __init__(self):
        super().__init__(DatabaseConfig('navigation'),
                         'djange',
                         'navigation',
                         ['id'],
                         None)
        metadata = MetaData()

        self._table = None
        self._columns = ["id", "parent", "nav_name", "url", "start_page"]

    def get_data_model(self):
        return Navigation

    def get_django_instance(self, p_key, instance):
        return None

    def _prepare_items_internal(self, data_item):
        return data_item

    def get_edit_extra_data(self) -> Dict[str, object]:
        return {}


NAVIGATION_DATA_PROVIDER = NavigationDataProvider()
