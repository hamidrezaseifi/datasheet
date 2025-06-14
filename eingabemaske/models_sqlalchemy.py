# eingabemaske/models_sqlalchemy.py
from datetime import datetime
from typing import Dict

from sqlalchemy import Column, String, DateTime
from sqlalchemy import MetaData, Table, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base

from eingabemaske.models import UserData
from shared_fields.data_provider import DataProviderBase, DatabaseConfig, ModelNavigationProvider

Base = declarative_base()


class Eingabe(Base):
    __tablename__ = 'eingabe'
    __table_args__ = {'schema': 'test_evar.djange'}
    email = Column(String(200), primary_key=True, nullable=False)
    name = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=True)


class EingabeDataProvider(DataProviderBase):

    def __init__(self):
        super().__init__(DatabaseConfig('eingabe'),
                         'test_evar.djange',
                         'eingabe',
                         ['email'],
                         ModelNavigationProvider("Eingabe", "eingabe", "Meine Test", self))
        metadata = MetaData()

        self._table = Table(self._table_name, metadata,
                            Column('name', String(100)),
                            Column('email', String(200), nullable=False, primary_key=True),
                            Column('created_at', DateTime),
                            PrimaryKeyConstraint(name=self._table_name + '_PK', mssql_clustered=False),
                            schema=self._schema_name
                            )
        self._columns = [c[0] for c in self._table.columns.items()]

        self._create_table()

    def get_data_model(self):
        return Eingabe

    def get_django_instance(self, p_key, instance):
        django_instance = UserData(name=instance.name, email=instance.email, created_at=instance.created_at)
        return django_instance

    def _prepare_items_internal(self, data_item):
        return data_item

    def get_edit_extra_data(self) -> Dict[str, object]:
        return {}


EINGABE_DATA_PROVIDER = EingabeDataProvider()
