from abc import ABC

from sqlalchemy import MetaData, Table, Column, String, PrimaryKeyConstraint, DateTime
from sqlalchemy.ext.declarative import declarative_base

from shared_fields.data_provider import DataProviderBase, DatabaseConfig
from shared_fields.model_navigation_provider import ModelNavigationProvider
from shared_fields.models import ActionLog

Base = declarative_base()


class ActionLogProvider(DataProviderBase, ABC):
    def __init__(self):
        print("Initializing ActionLogProvider")
        super().__init__(DatabaseConfig('dbo'),
                         'test_evar.djange',
                         'action_log',
                         ['user'],
                         ModelNavigationProvider('', '', '', None)
                         )
        metadata = MetaData()
        self._table = Table(self._table_name, metadata,
                            Column('user', String(255), primary_key=True, nullable=True),
                            Column('action', String(50), nullable=False),
                            Column('message', String(1000), nullable=False),
                            Column('created_at', DateTime),
                            PrimaryKeyConstraint('user', name=self._table_name + '_PK', mssql_clustered=True),
                            schema=self._schema_name)
        self._columns = [c[0] for c in self._table.columns.items()]
        self._create_table()

    def _prepare_items_internal(self, data_item):
        return data_item

    def get_data_model(self):
        return ActionLog

    def get_django_instance(self, p_key, instance):
        django_instance = ActionLog(id=instance.id,
                                    user=instance.user_name,
                                    action=instance.action,
                                    message=instance.message,
                                    created_at=instance.created_at)
        return django_instance

    def get_edit_extra_data(self) -> dict:
        return {}


ACTION_LOG_DATA_PROVIDER = ActionLogProvider()
