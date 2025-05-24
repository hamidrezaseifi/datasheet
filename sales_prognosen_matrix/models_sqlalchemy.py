# sales_prognosen_matrix/models_sqlalchemy.py
from abc import ABC
from datetime import datetime

from sqlalchemy import Column, BigInteger, Integer, String, Float, Date, ForeignKey, MetaData, Table, \
    PrimaryKeyConstraint, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from sales_prognosen_matrix.forms import get_month_name
from shared_fields.data_provider import DataProviderBase, DatabaseConfig, ModelNavigationProvider

Base = declarative_base()


class SalesObjekt(Base):
    __tablename__ = 'sales_objekt'
    __table_args__ = {'schema': 'public'}
    objekt = Column(String(100), nullable=False, primary_key=True, unique=False)
    sort_order = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    sales_data = relationship(
        "SalesPrognose",
        back_populates="sales_objekt",
        foreign_keys="SalesPrognose.objekt"
    )


class SalesObjektProvider(DataProviderBase, ABC):
    def __init__(self):
        print("Initializing SalesObjektProvider")
        super().__init__(DatabaseConfig('SalesObjekt'),
                         'public',
                         'sales_objekt',
                         ['objekt'],
                         ModelNavigationProvider("Sales-Objekt", "sales_objekt", "Sales", self))
        metadata = MetaData()

        self._table = Table(self._table_name, metadata,
                            Column('objekt', String(100), primary_key=True, nullable=False),
                            Column('sort_order', Integer, nullable=False),
                            Column('created_at', DateTime),
                            PrimaryKeyConstraint('objekt', name=self._table_name + '_PK', mssql_clustered=True),
                            schema=self._schema_name
                            )
        self._columns = [c[0] for c in self._table.columns.items()]
        self._create_table()

    def _prepare_items_internal(self, data_item):
        return data_item

    def get_data_model(self):
        return SalesObjekt

    def get_django_instance(self, p_key, instance):
        django_instance = SalesObjekt(objekt=instance.objekt,
                                      sort_order=instance.sort_order,
                                      created_at=instance.created_at)
        return django_instance


SALES_OBJEKT_DATA_PROVIDER = SalesObjektProvider()


class SalesPrognose(Base):
    __tablename__ = 'sales_prognose'
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    objekt = Column(BigInteger, ForeignKey('default.sales_objekt.objekt'), nullable=False)
    sortierreihen_folge = Column(BigInteger, ForeignKey('default.sales_objekt.sort_order'), nullable=False)
    jahr = Column(Integer, nullable=False)
    monat = Column(Integer, nullable=False)
    datum = Column(Date, nullable=False)
    prognose = Column(Float, default=0.0, nullable=False)
    created_at = Column(Date, default=datetime.utcnow, nullable=False)

    sales_objekt = relationship(
        "SalesObjekt",
        back_populates="sales_data",
        foreign_keys=[objekt]
    )


class SalesPrognoseProvider(DataProviderBase, ABC):

    def __init__(self):
        super().__init__(DatabaseConfig('SalesPrognose'),
                         'public',
                         'sales_prognose',
                         ['id'],
                         ModelNavigationProvider("Sales-Prognose", "sales_prognose", "Sales", self))
        metadata = MetaData()

        self._table = Table(self._table_name, metadata,
                            Column('id', BigInteger, nullable=False, primary_key=True),
                            Column('objekt', String(100), nullable=False),
                            Column('sortierreihen_folge', Integer, nullable=False),
                            Column('jahr', Integer, nullable=True),
                            Column('monat', Integer, nullable=True),
                            Column('datum', Date, nullable=True),
                            Column('prognose', Float),
                            Column('created_at', DateTime),
                            PrimaryKeyConstraint('id', name=self._table_name + '_PK', mssql_clustered=False),
                            schema=self._schema_name
                            )
        self._columns = [c[0] for c in self._table.columns.items()]

        self._create_table()

    def get_data_model(self):
        return SalesPrognose

    def get_django_instance(self, p_key, instance):
        # django_instance = PlanungData.objects.filter(sap_nr=p_key).first()
        django_instance = SalesPrognose(id=instance.sap_nr,
                                        objekt=instance.objekt,
                                        sortierreihen_folge=instance.sortierreihen_folge,
                                        jahr=instance.jahr,
                                        monat=instance.monat,
                                        datum=instance.datum,
                                        prognose=instance.prognose
                                        )
        return django_instance

    def _prepare_items_internal(self, data_item):
        data_item['monat'] = get_month_name(data_item['monat'])
        return data_item



SALES_PROGNOSE_DATA_PROVIDER = SalesPrognoseProvider()

