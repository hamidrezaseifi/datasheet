from abc import ABC

from sqlalchemy import Column, BigInteger, String, Integer
from sqlalchemy import MetaData, Table, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base

from planung.models import PlanungData
from shared_fields.data_provider import DataProviderBase, DatabaseConfig, ModelNavigationProvider
from planung.forms import get_month_name

#from shared_fields.fields import get_month_name

Base = declarative_base()


class Planung(Base):
    __tablename__ = 'planung'
    __table_args__ = {'schema': 'test_evar.djange'}
    sap_nr = Column(BigInteger, primary_key=True, nullable=False)
    objekt_name = Column(String(255), nullable=True)
    jahr = Column(Integer, nullable=False)
    monat = Column(Integer, nullable=False)
    umsatz_art = Column(String(255), nullable=True)
    plan = Column(Integer, nullable=False)


class PlanungDataProvider(DataProviderBase, ABC):

    def __init__(self):
        super().__init__(DatabaseConfig('planung'),
                         'test_evar.djange',
                         'planung',
                         ['sap_nr'],
                         ModelNavigationProvider("Planung", "planung", "Meine Test", self))
        metadata = MetaData()

        self._table = Table(self._table_name, metadata,
                            Column('sap_nr', BigInteger, nullable=False, primary_key=True),
                            Column('objekt_name', String(255)),
                            Column('jahr', Integer, nullable=False),
                            Column('monat', Integer, nullable=False),
                            Column('umsatz_art', String(255)),
                            Column('plan', Integer, nullable=False),
                            PrimaryKeyConstraint(name=self._table_name + '_PK', mssql_clustered=False),
                            schema=self._schema_name
                            )
        self._columns = [c[0] for c in self._table.columns.items()]

        self._create_table()

    def get_data_model(self):
        return Planung

    def get_django_instance(self, p_key, instance):
        # django_instance = PlanungData.objects.filter(sap_nr=p_key).first()
        django_instance = PlanungData(sap_nr=instance.sap_nr,
                                      objekt_name=instance.objekt_name,
                                      jahr=instance.jahr,
                                      monat=instance.monat,
                                      umsatz_art=instance.umsatz_art,
                                      plan=instance.plan)
        return django_instance

    def _prepare_items_internal(self, data_item):
        data_item['monat'] = get_month_name(data_item['monat'])
        return data_item


PLANUNG_DATA_PROVIDER = PlanungDataProvider()


# y = 2001
# m = 1
# for i in range(201, 501):
#     y += 1
#     if y > 2025:
#         y = 2000
#     m += 1
#     if m > 12:
#         y = 1
#     PLANUNG_DATA_PROVIDER.add({'sap_nr': i,
#                                'id2': 10 + i,
#                                'objekt_name': f'obj-{i}',
#                                'jahr': y,
#                                'monat': m,
#                                'umsatz_art': f'um-{i}',
#                                'plan': i * 3
#                                }
#                               )
